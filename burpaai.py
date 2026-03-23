# -*- coding: utf-8 -*-
from __future__ import print_function
"""
BurpAI NATIVE REPEATER MODE - Burp Suite Extension
Production-grade Jython extension with FIXED imports, clean UI, no crashes
"""

import sys
import traceback
import threading
import json
import time

# ===== BURP IMPORTS =====
from burp import IBurpExtender, ITab, IHttpListener, IContextMenuFactory, IMessageEditorController

# ===== JAVA/SWING IMPORTS (EXPLICIT - NO java. PREFIX) =====
from javax.swing import JPanel
from javax.swing import JScrollPane
from javax.swing import JSplitPane
from javax.swing import JTabbedPane
from javax.swing import JTable
from javax.swing import JTextArea
from javax.swing import JTextField
from javax.swing import JButton
from javax.swing import JLabel
from javax.swing import JComboBox
from javax.swing import JCheckBox
from javax.swing import JMenuItem
from javax.swing import SwingUtilities
from javax.swing import BorderFactory
from javax.swing import BoxLayout
from javax.swing import Box
from javax.swing import ListSelectionModel
from javax.swing.table import DefaultTableModel
from javax.swing.event import ListSelectionListener

# ===== JAVA AWT IMPORTS (EXPLICIT - NO java. PREFIX) =====
from java.awt import BorderLayout
from java.awt import FlowLayout
from java.awt import Dimension
from java.awt import Color
from java.awt import Font
from java.awt import Insets

# ===== JAVA AWT EVENT IMPORTS =====
from java.awt.event import ActionListener
from java.awt.event import KeyListener
from java.awt.event import KeyEvent

# ===== JAVA LANG IMPORTS =====
from java.lang import Runnable

# ===== URLLIB COMPATIBILITY =====
try:
    from urllib2 import Request, urlopen, HTTPError
except ImportError:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError


# ===== MESSAGE EDITOR CONTROLLER =====

class MessageEditorController(IMessageEditorController):
    def __init__(self, extension):
        self.ext = extension
    
    def getHttpService(self):
        return None
    
    def getRequest(self):
        return None
    
    def setRequest(self, message):
        pass
    
    def getResponse(self):
        return None
    
    def setResponse(self, message):
        pass
    
    def getEditorName(self):
        return "BurpAI"


# ===== EVENT LISTENERS =====

class SendButtonListener(ActionListener):
    def __init__(self, extension):
        self.ext = extension
    
    def actionPerformed(self, event):
        try:
            self.ext.send_chat_message()
        except Exception as e:
            print("[!] SendButtonListener error: " + str(e))
            traceback.print_exc()


class InputKeyListener(KeyListener):
    def __init__(self, extension):
        self.ext = extension
    
    def keyPressed(self, e):
        try:
            if e.getKeyCode() == KeyEvent.VK_ENTER:
                self.ext.send_chat_message()
        except Exception as e:
            print("[!] InputKeyListener error: " + str(e))
            traceback.print_exc()
    
    def keyReleased(self, e):
        pass
    
    def keyTyped(self, e):
        pass


class SaveAPIListener(ActionListener):
    def __init__(self, extension):
        self.ext = extension
    
    def actionPerformed(self, event):
        try:
            self.ext.save_api_key()
        except Exception as e:
            print("[!] SaveAPIListener error: " + str(e))
            traceback.print_exc()


class UpdateModelListener(ActionListener):
    def __init__(self, extension):
        self.ext = extension
    
    def actionPerformed(self, event):
        try:
            self.ext.update_model()
        except Exception as e:
            print("[!] UpdateModelListener error: " + str(e))
            traceback.print_exc()


class RepeatSendListener(ActionListener):
    def __init__(self, extension):
        self.ext = extension
    
    def actionPerformed(self, event):
        try:
            self.ext.send_request()
        except Exception as e:
            print("[!] RepeatSendListener error: " + str(e))
            traceback.print_exc()


class HistorySelectionListener(ListSelectionListener):
    def __init__(self, extension):
        self.ext = extension
    
    def valueChanged(self, event):
        try:
            if not event.getValueIsAdjusting():
                self.ext.load_from_history()
        except Exception as e:
            print("[!] HistorySelectionListener error: " + str(e))
            traceback.print_exc()


class ContextMenuSendToAIListener(ActionListener):
    def __init__(self, extension, messages):
        self.ext = extension
        self.messages = messages
    
    def actionPerformed(self, event):
        try:
            self.ext.forward_to_ai_from_menu(self.messages)
        except Exception as e:
            print("[!] ContextMenuSendToAIListener error: " + str(e))
            traceback.print_exc()


class ContextMenuFactory(IContextMenuFactory):
    def __init__(self, extension):
        self.extension = extension
    
    def createMenuItems(self, invocation):
        try:
            menu_items = []
            selected = invocation.getSelectedMessages()
            
            if selected and len(selected) > 0:
                item = JMenuItem("Send to BurpAI")
                item.addActionListener(ContextMenuSendToAIListener(self.extension, selected))
                menu_items.append(item)
            
            return menu_items if menu_items else None
        except Exception as e:
            print("[!] ContextMenuFactory error: " + str(e))
            traceback.print_exc()
            return None


class AnalyzeButtonListener(ActionListener):
    def __init__(self, extension):
        self.ext = extension
    
    def actionPerformed(self, event):
        try:
            self.ext.analyze_with_ai()
        except Exception as e:
            print("[!] AnalyzeButtonListener error: " + str(e))
            traceback.print_exc()


class AutoAnalyzeListener(ActionListener):
    def __init__(self, extension):
        self.ext = extension
    
    def actionPerformed(self, event):
        try:
            self.ext.auto_analyze = self.ext.auto_analyze_checkbox.isSelected()
            print("[*] Auto Analyze: " + str(self.ext.auto_analyze))
        except Exception as e:
            print("[!] AutoAnalyzeListener error: " + str(e))
            traceback.print_exc()





# ===== MAIN EXTENSION CLASS =====

class BurpExtender(IBurpExtender, ITab, IHttpListener):
    
    def registerExtenderCallbacks(self, callbacks):
        try:
            self.callbacks = callbacks
            self.helpers = callbacks.getHelpers()
            
            self.api_key = ""
            self.model = "kimi-k2.5"
            self.traffic_log = []
            self.ai_history = []
            self.max_history = 1000  # Limit history to 1000 entries for performance
            self.current_request = None
            self.current_response = None
            
            # Multi-model engine with fallback (Bug Bounty Hunter Mode)
            self.primary_models = [
                "alibaba-qwen3-32b",
                "deepseek-r1-distill-llama-70b",
                "glm-5",
                "kimi-k2.5",
                "llama3-8b-instruct",
                "llama3.3-70b-instruct",
                "minimax-m2.5",
                "mistral-nemo-instruct-2407",
                "nvidia-nemotron-3-super-120b",
                "openai-gpt-oss-120b",
                "openai-gpt-oss-20b"
            ]
            self.fallback_models = []
            self.all_models = self.primary_models + self.fallback_models
            self.current_model_index = 0
            
            # UI Components
            self.chat_display = None
            self.chat_input = None
            self.api_input = None
            self.status_label = None
            self.model_combo = None
            self.history_table = None
            self.history_model = None
            
            # Native Message Editors
            self.request_editor = None
            self.response_editor = None
            self.editor_controller = MessageEditorController(self)
            
            # Repeater controls
            self.auto_analyze = False
            self.auto_analyze_checkbox = None
            
            self.callbacks.registerHttpListener(self)
            self.callbacks.registerContextMenuFactory(ContextMenuFactory(self))
            self.callbacks.addSuiteTab(self)
            
            print("[*] BurpAI loaded successfully - ready to capture requests")
        except Exception as e:
            print("[!] Error in registerExtenderCallbacks: " + str(e))
            traceback.print_exc()
    
    def getTabCaption(self):
        try:
            return "BurpAI"
        except Exception as e:
            print("[!] Error in getTabCaption: " + str(e))
            traceback.print_exc()
            return "BurpAI"
    
    def getUiComponent(self):
        try:
            return self.build_ui()
        except Exception as e:
            print("[!] Error in getUiComponent: " + str(e))
            traceback.print_exc()
            return JPanel()
    
    def build_ui(self):
        """Build main UI with clean alignment"""
        try:
            main_panel = JPanel(BorderLayout())
            main_panel.setBackground(Color(30, 30, 30))
            
            # TOP: Compact toolbar
            toolbar = self.build_toolbar()
            main_panel.add(toolbar, BorderLayout.NORTH)
            
            # CENTER: Main horizontal split
            main_split = JSplitPane(JSplitPane.HORIZONTAL_SPLIT)
            main_split.setDividerLocation(400)
            main_split.setBackground(Color(30, 30, 30))
            main_split.setResizeWeight(0.4)
            main_split.setBorder(BorderFactory.createLineBorder(Color(60, 60, 60), 1))
            
            left_panel = self.build_chat_panel()
            right_panel = self.build_right_panel()
            
            main_split.setLeftComponent(left_panel)
            main_split.setRightComponent(right_panel)
            
            main_panel.add(main_split, BorderLayout.CENTER)
            
            return main_panel
        except Exception as e:
            print("[!] Error in build_ui: " + str(e))
            traceback.print_exc()
            return JPanel()
    
    def build_toolbar(self):
        """Create compact Burp-style toolbar with proper alignment"""
        try:
            toolbar = JPanel(FlowLayout(FlowLayout.LEFT, 8, 5))
            toolbar.setBackground(Color(40, 40, 40))
            toolbar.setBorder(BorderFactory.createLineBorder(Color(60, 60, 60), 1))
            toolbar.setPreferredSize(Dimension(100, 38))
            
            # API Key label
            api_label = JLabel("API Key:")
            api_label.setForeground(Color(180, 180, 180))
            api_label.setFont(Font("Arial", Font.PLAIN, 10))
            toolbar.add(api_label)
            
            # API Key input field
            self.api_input = JTextField()
            self.api_input.setBackground(Color(50, 50, 50))
            self.api_input.setForeground(Color(200, 200, 200))
            self.api_input.setFont(Font("Monospaced", Font.PLAIN, 10))
            self.api_input.setPreferredSize(Dimension(200, 26))
            self.api_input.setMaximumSize(Dimension(200, 26))
            self.api_input.setMargin(Insets(2, 4, 2, 4))
            toolbar.add(self.api_input)
            
            # Save button
            save_btn = JButton("Save")
            save_btn.setBackground(Color(100, 180, 100))
            save_btn.setForeground(Color.WHITE)
            save_btn.setFont(Font("Arial", Font.BOLD, 9))
            save_btn.setPreferredSize(Dimension(65, 26))
            save_btn.setMaximumSize(Dimension(65, 26))
            save_btn.setMargin(Insets(2, 8, 2, 8))
            save_btn.setFocusPainted(False)
            save_btn.addActionListener(SaveAPIListener(self))
            toolbar.add(save_btn)
            
            # Separator
            toolbar.add(JLabel("  |  "))
            
            # Model label
            model_label = JLabel("Model:")
            model_label.setForeground(Color(180, 180, 180))
            model_label.setFont(Font("Arial", Font.PLAIN, 10))
            toolbar.add(model_label)
            
            # Model dropdown
            self.model_combo = JComboBox(self.all_models)
            self.model_combo.setBackground(Color(50, 50, 50))
            self.model_combo.setForeground(Color(200, 200, 200))
            self.model_combo.setFont(Font("Arial", Font.PLAIN, 10))
            self.model_combo.setPreferredSize(Dimension(170, 26))
            self.model_combo.setMaximumSize(Dimension(170, 26))
            self.model_combo.addActionListener(UpdateModelListener(self))
            toolbar.add(self.model_combo)
            
            # Separator
            toolbar.add(JLabel("  |  "))
            
            # Status label
            status_label_text = JLabel("Status:")
            status_label_text.setForeground(Color(180, 180, 180))
            status_label_text.setFont(Font("Arial", Font.PLAIN, 10))
            toolbar.add(status_label_text)
            
            self.status_label = JLabel("Ready")
            self.status_label.setForeground(Color(255, 200, 100))
            self.status_label.setFont(Font("Arial", Font.BOLD, 10))
            toolbar.add(self.status_label)
            
            return toolbar
        except Exception as e:
            print("[!] Error in build_toolbar: " + str(e))
            traceback.print_exc()
            return JPanel()
    
    def build_chat_panel(self):
        """Build left chat panel"""
        try:
            panel = JPanel(BorderLayout())
            panel.setBackground(Color(30, 30, 30))
            panel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5))
            
            # Chat display
            self.chat_display = JTextArea()
            self.chat_display.setEditable(False)
            self.chat_display.setBackground(Color(30, 30, 30))
            self.chat_display.setForeground(Color(212, 212, 212))
            self.chat_display.setFont(Font("Consolas", Font.PLAIN, 11))
            self.chat_display.setLineWrap(True)
            self.chat_display.setWrapStyleWord(True)
            self.chat_display.setMargin(Insets(8, 8, 8, 8))
            
            scroll = JScrollPane(self.chat_display)
            scroll.setBackground(Color(30, 30, 30))
            scroll.setBorder(BorderFactory.createLineBorder(Color(60, 60, 60), 1))
            scroll.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED)
            scroll.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER)
            
            panel.add(scroll, BorderLayout.CENTER)
            
            # Input area
            input_panel = JPanel(BorderLayout())
            input_panel.setBackground(Color(30, 30, 30))
            input_panel.setBorder(BorderFactory.createEmptyBorder(8, 0, 0, 0))
            
            self.chat_input = JTextField()
            self.chat_input.setBackground(Color(45, 45, 48))
            self.chat_input.setForeground(Color(212, 212, 212))
            self.chat_input.setFont(Font("Monospaced", Font.PLAIN, 11))
            self.chat_input.setCaretColor(Color(212, 212, 212))
            self.chat_input.setMargin(Insets(4, 6, 4, 6))
            self.chat_input.addKeyListener(InputKeyListener(self))
            
            input_panel.add(self.chat_input, BorderLayout.CENTER)
            
            send_btn = JButton("Send")
            send_btn.setBackground(Color(51, 122, 183))
            send_btn.setForeground(Color.WHITE)
            send_btn.setFont(Font("Arial", Font.PLAIN, 10))
            send_btn.setFocusPainted(False)
            send_btn.setPreferredSize(Dimension(75, 32))
            send_btn.setMargin(Insets(2, 10, 2, 10))
            send_btn.addActionListener(SendButtonListener(self))
            
            input_panel.add(send_btn, BorderLayout.EAST)
            panel.add(input_panel, BorderLayout.SOUTH)
            
            return panel
        except Exception as e:
            print("[!] Error in build_chat_panel: " + str(e))
            traceback.print_exc()
            return JPanel()
    
    def build_right_panel(self):
        """Build right panel with history and repeater"""
        try:
            right_split = JSplitPane(JSplitPane.VERTICAL_SPLIT)
            right_split.setDividerLocation(200)
            right_split.setBackground(Color(30, 30, 30))
            right_split.setResizeWeight(0.35)
            right_split.setBorder(BorderFactory.createLineBorder(Color(60, 60, 60), 1))
            
            history_panel = self.build_history_panel()
            repeater_panel = self.build_repeater_panel()
            
            right_split.setTopComponent(history_panel)
            right_split.setBottomComponent(repeater_panel)
            
            return right_split
        except Exception as e:
            print("[!] Error in build_right_panel: " + str(e))
            traceback.print_exc()
            return JPanel()
    
    def build_history_panel(self):
        """Build history table panel with data binding"""
        try:
            panel = JPanel(BorderLayout())
            panel.setBackground(Color(30, 30, 30))
            panel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5))
            
            # Title
            title_label = JLabel("Request History")
            title_label.setForeground(Color(150, 150, 150))
            title_label.setFont(Font("Arial", Font.BOLD, 10))
            
            title_panel = JPanel()
            title_panel.setBackground(Color(30, 30, 30))
            title_panel.add(title_label)
            panel.add(title_panel, BorderLayout.NORTH)
            
            # Create history table model with columns
            self.history_model = DefaultTableModel(
                ["#", "Method", "Host", "Path", "Status"],
                0
            )
            
            # Bind model to table
            self.history_table = JTable(self.history_model)
            self.history_table.setBackground(Color(45, 45, 48))
            self.history_table.setForeground(Color(212, 212, 212))
            self.history_table.setFont(Font("Monospaced", Font.PLAIN, 9))
            self.history_table.setGridColor(Color(60, 60, 60))
            self.history_table.setRowHeight(22)
            self.history_table.setSelectionBackground(Color(66, 110, 165))
            
            # Add selection listener to load requests
            self.history_table.getSelectionModel().addListSelectionListener(HistorySelectionListener(self))
            
            # Set column widths
            self.history_table.getColumnModel().getColumn(0).setPreferredWidth(30)
            self.history_table.getColumnModel().getColumn(1).setPreferredWidth(50)
            self.history_table.getColumnModel().getColumn(2).setPreferredWidth(80)
            self.history_table.getColumnModel().getColumn(3).setPreferredWidth(100)
            self.history_table.getColumnModel().getColumn(4).setPreferredWidth(40)
            
            # Add scroll pane
            scroll = JScrollPane(self.history_table)
            scroll.setBackground(Color(30, 30, 30))
            scroll.setBorder(BorderFactory.createLineBorder(Color(60, 60, 60), 1))
            scroll.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED)
            scroll.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER)
            
            panel.add(scroll, BorderLayout.CENTER)
            
            print("[*] History table initialized: model=" + str(self.history_model) + ", table=" + str(self.history_table))
            
            return panel
        except Exception as e:
            print("[!] Error in build_history_panel: " + str(e))
            traceback.print_exc()
            return JPanel()
    
    def build_repeater_panel(self):
        """Build native repeater panel"""
        try:
            panel = JPanel(BorderLayout())
            panel.setBackground(Color(30, 30, 30))
            panel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5))
            
            # Title
            title_label = JLabel("Repeater / Response")
            title_label.setForeground(Color(150, 150, 150))
            title_label.setFont(Font("Arial", Font.BOLD, 10))
            
            title_panel = JPanel()
            title_panel.setBackground(Color(30, 30, 30))
            title_panel.add(title_label)
            panel.add(title_panel, BorderLayout.NORTH)
            
            # Native Burp Message Editors
            try:
                self.request_editor = self.callbacks.createMessageEditor(self.editor_controller, True)
                self.response_editor = self.callbacks.createMessageEditor(self.editor_controller, False)
            except Exception as editor_err:
                print("[!] Error creating message editors: " + str(editor_err))
                traceback.print_exc()
                self.request_editor = None
                self.response_editor = None
            
            # Tabs for request/response
            tabs = JTabbedPane()
            tabs.setBackground(Color(40, 40, 40))
            tabs.setForeground(Color(180, 180, 180))
            
            if self.request_editor:
                request_component = self.request_editor.getComponent()
                tabs.addTab("Request", request_component)
            
            if self.response_editor:
                response_component = self.response_editor.getComponent()
                tabs.addTab("Response", response_component)
            
            panel.add(tabs, BorderLayout.CENTER)
            
            # Control buttons panel
            btn_panel = JPanel()
            btn_panel.setLayout(FlowLayout(FlowLayout.LEFT, 8, 5))
            btn_panel.setBackground(Color(30, 30, 30))
            btn_panel.setBorder(BorderFactory.createEmptyBorder(8, 0, 0, 0))
            
            repeat_send = JButton("Send Request")
            repeat_send.setBackground(Color(100, 200, 100))
            repeat_send.setForeground(Color.WHITE)
            repeat_send.setFont(Font("Arial", Font.BOLD, 10))
            repeat_send.setPreferredSize(Dimension(120, 30))
            repeat_send.setMargin(Insets(4, 15, 4, 15))
            repeat_send.setFocusPainted(False)
            repeat_send.addActionListener(RepeatSendListener(self))
            btn_panel.add(repeat_send)
            
            # Separator
            btn_panel.add(JLabel("  |  "))
            
            # Analyze button
            analyze_btn = JButton("Analyze with AI")
            analyze_btn.setBackground(Color(51, 122, 183))
            analyze_btn.setForeground(Color.WHITE)
            analyze_btn.setFont(Font("Arial", Font.BOLD, 10))
            analyze_btn.setPreferredSize(Dimension(130, 30))
            analyze_btn.setMargin(Insets(4, 15, 4, 15))
            analyze_btn.setFocusPainted(False)
            analyze_btn.addActionListener(AnalyzeButtonListener(self))
            btn_panel.add(analyze_btn)
            
            # Auto Analyze checkbox
            try:
                self.auto_analyze_checkbox = JCheckBox()
                self.auto_analyze_checkbox.setText("Auto Analyze")
                self.auto_analyze_checkbox.setBackground(Color(30, 30, 30))
                self.auto_analyze_checkbox.setForeground(Color(212, 212, 212))
                self.auto_analyze_checkbox.setFont(Font("Arial", Font.PLAIN, 10))
                self.auto_analyze_checkbox.setFocusPainted(False)
                self.auto_analyze_checkbox.addActionListener(AutoAnalyzeListener(self))
                btn_panel.add(self.auto_analyze_checkbox)
            except Exception as checkbox_err:
                print("[!] Error creating auto analyze checkbox: " + str(checkbox_err))
            
            panel.add(btn_panel, BorderLayout.SOUTH)
            
            return panel
        except Exception as e:
            print("[!] Error in build_repeater_panel: " + str(e))
            traceback.print_exc()
            return JPanel()
    
    # ===== CORE METHODS =====
    
    def save_api_key(self):
        try:
            key = self.api_input.getText().strip()
            
            if not key:
                self.add_chat_message("System", "Error: API key cannot be empty")
                return
            
            self.api_key = key
            self.callbacks.saveExtensionSetting("burpaai_api_key", key)
            
            self.add_chat_message("System", "API key saved successfully")
            self.status_label.setText("Connected")
            self.status_label.setForeground(Color(100, 200, 100))
        except Exception as e:
            print("[!] Error saving API key: " + str(e))
            traceback.print_exc()
            self.add_chat_message("System", "Error saving API key: " + str(e))
    
    def update_model(self):
        try:
            self.model = str(self.model_combo.getSelectedItem())
            print("[*] Model updated: " + self.model)
        except Exception as e:
            print("[!] Error updating model: " + str(e))
            traceback.print_exc()
    
    def send_chat_message(self):
        try:
            text = self.chat_input.getText().strip()
            
            if not text:
                return
            
            if not self.api_key:
                self.add_chat_message("System", "Error: API key not configured")
                return
            
            self.add_chat_message("You", text)
            self.chat_input.setText("")
            
            thread = threading.Thread(target=lambda: self._send_chat_async(text))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print("[!] Error in send_chat_message: " + str(e))
            traceback.print_exc()
    
    def _send_chat_async(self, text):
        try:
            response = self.call_ai(text)
            SwingUtilities.invokeLater(lambda: self.add_chat_message("AI", response))
        except Exception as e:
            print("[!] Error in _send_chat_async: " + str(e))
            traceback.print_exc()
            SwingUtilities.invokeLater(lambda: self.add_chat_message("System", "Error: " + str(e)))
    
    def add_chat_message(self, sender, text):
        def update_ui():
            try:
                timestamp = time.strftime("%H:%M:%S")
                current = self.chat_display.getText()
                
                # Format message based on sender type  
                if sender == "BugBounty":
                    prefix = "[" + timestamp + "] [ANALYSIS]: "
                elif sender == "AI":
                    prefix = "[" + timestamp + "] [AI]: "
                elif sender == "You":
                    prefix = "[" + timestamp + "] [YOU]: "
                else:
                    prefix = "[" + timestamp + "] [" + sender + "]: "
                
                formatted_text = prefix + text
                
                if current:
                    new_text = current + "\n" + formatted_text
                else:
                    new_text = formatted_text
                
                self.chat_display.setText(new_text)
                self.chat_display.setCaretPosition(len(new_text))
            except Exception as e:
                print("[!] Error in add_chat_message: " + str(e))
                traceback.print_exc()
        
        SwingUtilities.invokeLater(update_ui)
    def send_request(self):
        """Send request via Burp's native HTTP handler"""
        try:
            # Get request from native editor
            request_bytes = self.request_editor.getMessage()
            
            if not request_bytes or len(request_bytes) == 0:
                self.add_chat_message("System", "Error: Request editor is empty")
                return
            
            # Parse request to extract host, port, protocol
            request_str = self.helpers.bytesToString(request_bytes)
            
            # Use Burp's analyzeRequest to get proper structure
            analyzed = self.helpers.analyzeRequest(request_bytes)
            
            # Get HTTP service details
            host = analyzed.getUrl().getHost()
            port = analyzed.getUrl().getPort()
            protocol = analyzed.getUrl().getProtocol()
            
            use_https = (protocol.lower() == "https")
            
            if not host:
                self.add_chat_message("System", "Error: Could not parse host from request")
                return
            
            # Build HTTP service
            http_service = self.helpers.buildHttpService(host, port, use_https)
            
            # Send request and get response
            response_bytes = self.callbacks.makeHttpRequest(http_service, request_bytes)
            
            if response_bytes:
                # Load response into native editor
                self.response_editor.setMessage(response_bytes, False)
                self.add_chat_message("System", "[RESPONSE] Received from " + host)
                
                # Store in history
                entry = {
                    "method": analyzed.getMethod(),
                    "host": host,
                    "path": analyzed.getUrl().getPath(),
                    "request": request_bytes,
                    "response": response_bytes,
                    "timestamp": time.time()
                }
                self.ai_history.append(entry)
                
                # Update table thread-safe
                def update_table():
                    try:
                        status_code = self._extract_status_code(response_bytes)
                        row_num = len(self.ai_history)
                        self.history_model.addRow([
                            str(row_num),
                            analyzed.getMethod(),
                            host[:30],
                            analyzed.getUrl().getPath()[:40],
                            status_code
                        ])
                        print("[+] Request added to history: " + analyzed.getMethod() + " " + host)
                    except Exception as e:
                        print("[!] Error updating table: " + str(e))
                
                SwingUtilities.invokeLater(update_table)
                
                # Auto Analyze if enabled
                if self.auto_analyze:
                    print("[*] Auto Analyze triggered")
                    thread = threading.Thread(target=self.analyze_with_ai)
                    thread.daemon = True
                    thread.start()
            else:
                self.add_chat_message("System", "Error: No response from server")
        
        except Exception as e:
            print("[!] Error in send_request: " + str(e))
            traceback.print_exc()
            self.add_chat_message("System", "Error: " + str(e))
    
    def load_from_history(self):
        """Load request/response from history table on row selection"""
        try:
            if not self.history_table:
                print("[!] History table not initialized")
                return
            
            row = self.history_table.getSelectedRow()
            print("[*] History row selected: " + str(row))
            
            if row < 0:
                print("[!] No row selected (row < 0)")
                return
            
            if row >= len(self.ai_history):
                print("[!] Row index out of bounds: " + str(row) + " >= " + str(len(self.ai_history)))
                return
            
            entry = self.ai_history[row]
            print("[*] Loading from history - row: " + str(row) + ", method: " + entry.get("method", "?"))
            
            # Load request
            if "request" in entry and entry["request"]:
                if self.request_editor:
                    self.request_editor.setMessage(entry["request"], True)
                    print("[+] Request loaded into editor")
                else:
                    print("[!] Request editor not available")
            
            # Load response
            if "response" in entry and entry["response"]:
                if self.response_editor:
                    self.response_editor.setMessage(entry["response"], False)
                    print("[+] Response loaded into editor")
                else:
                    print("[!] Response editor not available")
        
        except Exception as e:
            print("[!] Error loading from history: " + str(e))
            traceback.print_exc()
    
    def add_row_to_history(self, row_data):
        """Thread-safe method to add row to history table"""
        def add_row_ui():
            try:
                if self.history_model:
                    self.history_model.addRow(row_data)
                    print("[+] Row added to history: " + str(row_data[0]))
            except Exception as e:
                print("[!] Error adding row to history: " + str(e))
                traceback.print_exc()
        
        SwingUtilities.invokeLater(add_row_ui)
    
    def _extract_status_code(self, response_bytes):
        """Extract HTTP status code from response"""
        try:
            response_str = self.helpers.bytesToString(response_bytes)
            first_line = response_str.split('\n')[0]
            parts = first_line.split(' ')
            if len(parts) >= 2:
                return parts[1]
        except:
            pass
        return "?"
    
    def _clean_reasoning_content(self, text):
        """Remove thinking/reasoning text from AI response and extract key payload sections"""
        try:
            # Remove common reasoning patterns
            lines = text.split('\n')
            cleaned = []
            skip_section = False
            
            for line in lines:
                line_lower = line.lower().strip()
                
                # Detect and preserve section headers
                if any(header in line_lower for header in ["[vulns]", "[payloads]", "[attack", "[exploit", "[test", "[issues]", "[vectors]"]):
                    cleaned.append(line)
                    skip_section = False
                    continue
                
                # Skip extended thinking patterns
                if any(pattern in line_lower for pattern in [
                    "the user is asking",
                    "the user is requesting",
                    "i need to",
                    "let me think",
                    "first, let me",
                    "to summarize",
                    "in conclusion",
                    "thinking about",
                    "considering the request",
                    "<thinking>",
                    "</thinking>",
                    "analyze the request"
                ]):
                    continue
                
                # Skip lines that are just thinking markers
                if line_lower.startswith("<") and line_lower.endswith(">"):
                    continue
                
                if line.strip():
                    cleaned.append(line)
            
            result = '\n'.join(cleaned).strip()
            
            # Limit to 800 chars for comprehensive analysis
            if len(result) > 800:
                result = result[:797] + "..."
            
            return result if result else "Processing complete"
        except:
            return text
    
    def _parse_vulnerability_response(self, response_text):
        """Parse AI response to extract and structure vulnerability data"""
        try:
            lines = response_text.split('\n')
            parsed = {
                "vulns": [],
                "attack_points": [],
                "payloads": [],
                "exploit_idea": [],
                "raw": response_text
            }
            
            current_section = None
            
            for line in lines:
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                
                # Detect section headers
                if "[VULNS]" in line_stripped.upper():
                    current_section = "vulns"
                    continue
                elif "[ATTACK" in line_stripped.upper():
                    current_section = "attack_points"
                    continue
                elif "[PAYLOADS]" in line_stripped.upper():
                    current_section = "payloads"
                    continue
                elif "[EXPLOIT" in line_stripped.upper():
                    current_section = "exploit_idea"
                    continue
                elif "[" in line_stripped and "]" in line_stripped:
                    current_section = None
                    continue
                
                # Add content to current section
                if current_section and line_stripped:
                    if line_stripped.startswith("-"):
                        line_stripped = line_stripped[1:].strip()
                    parsed[current_section].append(line_stripped)
            
            return parsed
        except:
            return {"vulns": [], "attack_points": [], "payloads": [], "exploit_idea": [], "raw": response_text}
    
    def _classify_vulnerability_severity(self, vuln_text):
        """Classify vulnerability severity based on keywords"""
        vuln_lower = vuln_text.lower()
        severity_map = {
            "CRITICAL": ["rce", "code execution", "remote command", "database dump", "full system compromise"],
            "HIGH": ["idor", "ssrf", "sqli", "auth bypass", "session hijack", "privilege escalation", "admin access"],
            "MEDIUM": ["xss", "csrf", "xxe", "header injection", "cookie manipulation", "weak authentication"],
            "LOW": ["information disclosure", "missing headers", "weak configuration", "cors"]
        }
        
        for severity, keywords in severity_map.items():
            if any(kw in vuln_lower for kw in keywords):
                return severity
        
        return "MEDIUM"
    
    def _format_vulnerability_output(self, parsed_vulns):
        """Format parsed vulnerability data for display"""
        try:
            output = ""
            
            if parsed_vulns["vulns"]:
                output += "[VULNERABILITIES]\n"
                for vuln in parsed_vulns["vulns"]:
                    severity = self._classify_vulnerability_severity(vuln)
                    output += "  - " + vuln + " (" + severity + ")\n"
                output += "\n"
            
            if parsed_vulns["attack_points"]:
                output += "[ATTACK VECTORS]\n"
                for point in parsed_vulns["attack_points"]:
                    output += "  - " + point + "\n"
                output += "\n"
            
            if parsed_vulns["payloads"]:
                output += "[TEST PAYLOADS]\n"
                for payload in parsed_vulns["payloads"]:
                    output += "  " + payload + "\n"
                output += "\n"
            
            if parsed_vulns["exploit_idea"]:
                output += "[EXPLOITATION STEPS]\n"
                for idea in parsed_vulns["exploit_idea"]:
                    output += "  - " + idea + "\n"
            
            return output if output else parsed_vulns["raw"]
        except:
            return parsed_vulns["raw"]
    
    def analyze_with_ai(self):
        """Analyze request/response as Elite Bug Bounty Hunter - P1 Focus"""
        try:
            # Validate API key
            if not self.api_key:
                self.add_chat_message("System", "Error: API key not configured - cannot analyze")
                return
            
            # Get request from editor
            if not self.request_editor:
                self.add_chat_message("System", "Error: Request editor not available")
                return
            
            request_bytes = self.request_editor.getMessage()
            
            if not request_bytes or len(request_bytes) == 0:
                self.add_chat_message("System", "Error: Request editor is empty")
                return
            
            # Convert request to string
            request_str = self.helpers.bytesToString(request_bytes)
            
            # Get response from editor if available
            response_str = ""
            if self.response_editor:
                response_bytes = self.response_editor.getMessage()
                if response_bytes and len(response_bytes) > 0:
                    response_str = self.helpers.bytesToString(response_bytes)
            
            # Bug bounty hunter analysis prompt - P1 focused with structured output
            if response_str:
                analysis_prompt = """You are an elite bug bounty hunter performing security analysis. Identify CRITICAL (P1/P2) vulnerabilities.

STRUCTURED ANALYSIS REQUIRED:

PRIORITY VULNERABILITIES:
1. RCE - Remote code execution, command injection
2. IDOR - Insecure direct object reference, privilege escalation
3. SSRF - Server-side request forgery, internal access
4. SQLi - SQL injection, data extraction
5. Auth bypass - Session hijacking, weak authentication
6. Critical misconfiguration - Admin panels, debug endpoints

SECONDARY CHECK:
- Missing security headers (CSP, X-Frame-Options, etc.)
- Weak cookies (missing HttpOnly, Secure, SameSite)
- CORS misconfiguration
- XXE, unsafe deserialization
- Header manipulation/injection

RESPONSE FORMAT (MANDATORY):

[VULNS]
- vulnerability name: severity level (CRITICAL/HIGH/MEDIUM/LOW)

[ATTACK POINTS]
- specific parameter/header/endpoint vulnerable

[PAYLOADS]
- raw, executable test code
- payload2

[EXPLOIT IDEA]
- step 1: how to trigger
- step 2: expected result

Analyze this request/response:

Request:
""" + request_str[:2000] + "\n\nResponse:\n" + response_str[:2000]
            else:
                analysis_prompt = """You are an elite bug bounty hunter. Analyze this request for CRITICAL (P1) vulnerabilities.

FOCUS AREAS:
1. RCE, IDOR, SSRF, SQLi, Auth bypass
2. Critical misconfigurations
3. Any exploitable patterns

RESPONSE FORMAT:

[VULNS]
- vulnerability: severity

[ATTACK POINTS]
- vulnerable vector

[PAYLOADS]
- test payload

[EXPLOIT IDEA]
- exploitation method

Request to analyze:
""" + request_str[:2000]
            
            print("[*] Elite Bug Bounty Hunter Analysis - P1 FOCUS...")
            self.add_chat_message("System", "Analyzing for P1 vulnerabilities...")
            
            # Call AI in background
            ai_response = self.call_ai(analysis_prompt)
            
            # Parse and format the response
            try:
                parsed = self._parse_vulnerability_response(ai_response)
                formatted = self._format_vulnerability_output(parsed)
                self.add_chat_message("BugBounty", formatted)
                print("[+] Parsed: " + str(len(parsed["vulns"])) + " vulnerabilities identified")
            except:
                # Fallback to raw response if parsing fails
                self.add_chat_message("BugBounty", ai_response)
            
            print("[+] P1 Analysis complete")
        
        except Exception as e:
            print("[!] Error in analyze_with_ai: " + str(e))
            traceback.print_exc()
            self.add_chat_message("System", "Error analyzing: " + str(e))
    
    # ===== API METHODS =====
    
    def call_ai(self, user_input, model=None):
        """Call DigitalOcean AI API with multi-model fallback engine"""
        if not model:
            model = self.model
        
        # Ensure model is in our supported list
        if model not in self.all_models:
            model = self.primary_models[0]
        
        try:
            # Find starting index
            try:
                start_index = self.all_models.index(model)
            except ValueError:
                start_index = 0
            
            # Try models starting from selected, then fallback chain
            for attempt in range(len(self.all_models)):
                current_model_idx = (start_index + attempt) % len(self.all_models)
                current_model = self.all_models[current_model_idx]
                
                try:
                    url = "https://inference.do-ai.run/v1/chat/completions"
                    
                    payload = {
                        "model": current_model,
                        "messages": [
                            {
                                "role": "user",
                                "content": user_input
                            }
                        ],
                        "max_tokens": 400
                    }
                    
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + self.api_key
                    }
                    
                    data_str = json.dumps(payload)
                    
                    try:
                        if isinstance(data_str, unicode):
                            data_str = data_str.encode('utf-8')
                    except NameError:
                        pass
                    
                    req = Request(url, data=data_str, headers=headers)
                    
                    try:
                        response = urlopen(req, timeout=15)
                        resp_data = response.read()
                        
                        if isinstance(resp_data, bytes):
                            resp_data = resp_data.decode('utf-8')
                        
                        print("[*] API Response from " + current_model + ": " + resp_data[:80] + "...")
                        
                        resp_json = json.loads(resp_data)
                        
                        if 'choices' in resp_json and len(resp_json['choices']) > 0:
                            choice = resp_json['choices'][0]
                            
                            if 'message' in choice:
                                msg = choice['message']
                                
                                # Try content first
                                if 'content' in msg and msg['content'] and msg['content'].strip():
                                    return msg['content'].strip()
                                
                                # Fallback to reasoning_content if available
                                if 'reasoning_content' in msg and msg['reasoning_content']:
                                    cleaned = self._clean_reasoning_content(msg['reasoning_content'])
                                    if cleaned and cleaned.strip():
                                        return cleaned
                        
                        # Response received but empty - try next model
                        print("[!] Empty response from " + current_model + " - trying next model")
                        continue
                    
                    except HTTPError as e:
                        error_code = e.code
                        print("[!] HTTPError " + str(error_code) + " from " + current_model + " - trying next model")
                        
                        if error_code == 401:
                            return "API authentication failed - check API key"
                        
                        # For other errors, continue to next model
                        continue
                    
                    except Exception as e:
                        print("[!] Exception from " + current_model + ": " + str(e) + " - trying next model")
                        continue
                
                except Exception as e:
                    print("[!] Error preparing request for " + current_model + ": " + str(e))
                    continue
            
            # All models failed
            return "AI service temporarily unavailable - tried all models"
        
        except Exception as e:
            print("[!] Exception in call_ai: " + str(e))
            traceback.print_exc()
            return "AI service error"
    
    def forward_to_ai_from_menu(self, messages):
        try:
            if not messages or len(messages) == 0:
                return
            
            message = messages[0]
            request = message.getRequest()
            response = message.getResponse()
            
            if not request:
                return
            
            # Load into native repeater editor
            self.request_editor.setMessage(request, True)
            
            if response:
                self.response_editor.setMessage(response, False)
                
                try:
                    # Get request details using analyzeRequest with message object
                    analyzed = self.helpers.analyzeRequest(message)
                    method = analyzed.getMethod()
                    host = analyzed.getUrl().getHost()
                    path = analyzed.getUrl().getPath()
                    
                    # Add to history
                    entry = {
                        "method": method,
                        "host": host,
                        "path": path,
                        "request": request,
                        "response": response,
                        "timestamp": time.time()
                    }
                    self.ai_history.append(entry)
                    
                    # Update table on UI thread
                    def update_table():
                        try:
                            row_num = len(self.ai_history)
                            status = self._extract_status_code(response)
                            self.history_model.addRow([
                                str(row_num),
                                method,
                                host[:25],
                                path[:35],
                                status
                            ])
                            print("[+] Added request to history: " + method + " " + host + path)
                        except Exception as table_err:
                            print("[!] Error adding row to history: " + str(table_err))
                            traceback.print_exc()
                    
                    SwingUtilities.invokeLater(update_table)
                except Exception as analyze_err:
                    print("[!] Error analyzing request: " + str(analyze_err))
                    traceback.print_exc()
            
            self.add_chat_message("System", "[FORWARDED] Request from Proxy/Repeater/Target")
        except Exception as e:
            print("[!] Error in forward_to_ai_from_menu: " + str(e))
            traceback.print_exc()
            self.add_chat_message("System", "Error forwarding request: " + str(e))
    
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        """HTTP listener callback - captures all traffic"""
        try:
            if not messageIsRequest:
                response = messageInfo.getResponse()
                
                if response:
                    try:
                        request = messageInfo.getRequest()
                        
                        # CRITICAL FIX: Use analyzeRequest with messageInfo object, NOT just request bytes
                        analyzed = self.helpers.analyzeRequest(messageInfo)
                        method = analyzed.getMethod()
                        host = analyzed.getUrl().getHost()
                        path = analyzed.getUrl().getPath()
                        
                        # Store in history with size limit
                        entry = {
                            "method": method,
                            "host": host,
                            "path": path,
                            "request": request,
                            "response": response,
                            "timestamp": time.time()
                        }
                        self.ai_history.append(entry)
                        self.traffic_log.append(messageInfo)
                        
                        # Limit history to max_history entries to prevent memory bloat
                        if len(self.ai_history) > self.max_history:
                            self.ai_history.pop(0)
                        if len(self.traffic_log) > self.max_history:
                            self.traffic_log.pop(0)
                        
                        # Update table on UI thread only
                        def update_table():
                            try:
                                status = self._extract_status_code(response)
                                row_num = len(self.ai_history)
                                if self.history_model:
                                    self.history_model.addRow([
                                        str(row_num),
                                        method,
                                        host[:25],
                                        path[:35],
                                        status
                                    ])
                                    print("[+] Traffic captured: " + method + " " + host + path + " [" + status + "]")
                            except Exception as table_err:
                                print("[!] Error updating history table: " + str(table_err))
                        
                        SwingUtilities.invokeLater(update_table)
                    
                    except Exception as e:
                        print("[!] Error processing HTTP message: " + str(e))
                        traceback.print_exc()
        
        except Exception as e:
            print("[!] Error in processHttpMessage: " + str(e))
            traceback.print_exc()

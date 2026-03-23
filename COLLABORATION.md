# COLLABORATION & CONTRIBUTION GUIDELINES

## Welcome to BurpAI

We appreciate your interest in contributing to BurpAI! This document outlines how to collaborate with us effectively.

## Code of Conduct

All contributors must:
- Treat others with respect and professionalism
- Provide constructive feedback
- Focus on the code and ideas, not personal attacks
- Report violations to the maintainers

## How to Contribute

### 1. Reporting Issues

**Before opening an issue:**
- Search existing issues to avoid duplicates
- Test with the latest version
- Provide a clear, detailed description

**Include in your issue:**
- Steps to reproduce the problem
- Expected vs. actual behavior
- Your environment (Burp Suite version, OS, Java version)
- Relevant logs or error messages

### 2. Feature Requests

**When suggesting features:**
- Explain the use case and benefits
- Provide examples if applicable
- Consider backward compatibility
- Discuss performance implications

### 3. Code Contributions

**Before submitting PR:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Follow the code style guidelines (see below)
4. Test thoroughly
5. Commit with clear, descriptive messages
6. Push to your fork
7. Submit a Pull Request with a detailed description

### Code Style Guidelines

- **Language:** Python (Jython 2.7 compatible)
- **Naming:** Use snake_case for variables/functions, PascalCase for classes
- **Documentation:** Add docstrings to all functions and classes
- **Imports:** Group imports logically (burp, java/swing, standard library)
- **Error handling:** Use try-except blocks with meaningful error messages
- **Comments:** Explain the "why", not the "what"

### Testing

- Test for Jython 2.7 compatibility
- Test with multiple Burp Suite versions (Pro, Community)
- Verify no regressions in existing functionality
- Test edge cases and error conditions

### Pull Request Process

1. Update documentation and CHANGELOG.md
2. Ensure all tests pass
3. Rebase on latest master
4. Request review from maintainers
5. Address feedback and comments
6. Maintainers merge when approved

## Development Setup

1. Clone the repository
2. Set BURP_HOME environment variable pointing to Burp installation
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests (if applicable)
5. Start developing!

## Collaboration Areas

### High Priority
- Security vulnerability fixes
- UI/UX improvements
- Performance optimizations
- Documentation improvements

### Medium Priority
- New AI model integrations
- Enhanced HTTP capture
- Better error handling
- Extended logging capabilities

### Low Priority
- Minor UI tweaks
- Code refactoring
- Test coverage improvements

## Communication

- **Issues:** Use GitHub Issues for bugs and features
- **Discussions:** Use GitHub Discussions for questions and ideas
- **Security:** See SECURITY.md for vulnerability reporting
- **Direct:** Contact maintainers for urgent matters

## Release Cycle

- **Major versions:** Significant features or breaking changes
- **Minor versions:** New features and improvements
- **Patch versions:** Bug fixes and maintenance

## Recognition

Contributors are recognized in:
- Release notes
- CHANGELOG.md
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (Apache 2.0).

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Search closed issues/discussions
3. Open a new discussion
4. Contact the maintainers

---

**Thank you for helping improve BurpAI!**

Last Updated: March 23, 2026

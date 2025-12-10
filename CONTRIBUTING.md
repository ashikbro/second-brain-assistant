# Contributing to Second Brain Assistant

Thank you for your interest in contributing to Second Brain Assistant! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/second-brain-assistant.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

Follow the setup instructions in [README.md](README.md) to get the development environment running.

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters

### JavaScript/React
- Use functional components with hooks
- Follow consistent naming conventions
- Use meaningful variable names
- Add comments for complex logic

## Project Structure

```
second-brain-assistant/
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── api/     # API endpoints
│   │   ├── core/    # Configuration
│   │   ├── db/      # Database connections
│   │   ├── models/  # Data models
│   │   └── services/# Business logic
├── frontend/         # React frontend
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
└── examples/        # Usage examples
```

## Making Changes

### Backend Changes

1. Update code in `backend/app/`
2. Follow existing patterns and structure
3. Add appropriate error handling
4. Test API endpoints manually or with curl
5. Update API documentation if needed

### Frontend Changes

1. Update code in `frontend/src/`
2. Follow React best practices
3. Ensure responsive design
4. Test in different browsers
5. Verify API integration works

### Adding New Features

When adding a new feature:

1. **Plan First**: Discuss major changes by opening an issue
2. **Backend**: 
   - Add models in `models/schemas.py`
   - Add business logic in `services/`
   - Add API endpoints in `api/`
3. **Frontend**:
   - Create components in `components/`
   - Add pages if needed in `pages/`
   - Update API service in `services/api.js`
4. **Document**: Update README.md with new features
5. **Test**: Follow TESTING.md guide

## Testing

Before submitting a PR:

1. Test all functionality manually
2. Verify no console errors
3. Test API endpoints
4. Check for security issues
5. Ensure code follows style guidelines

See [TESTING.md](TESTING.md) for detailed testing instructions.

## Security

- Never commit API keys or sensitive data
- Use environment variables for configuration
- Validate all user inputs
- Report security issues privately

## Pull Request Guidelines

### PR Title
Use clear, descriptive titles:
- ✅ "Add export functionality for notes"
- ✅ "Fix: Search not working with special characters"
- ❌ "Update"
- ❌ "Fix bug"

### PR Description
Include:
- What changes were made
- Why the changes were made
- How to test the changes
- Screenshots (for UI changes)

### Checklist
Before submitting:
- [ ] Code follows project style
- [ ] Changes tested thoroughly
- [ ] Documentation updated
- [ ] No console errors or warnings
- [ ] Commit messages are clear

## Common Contribution Areas

### Backend
- Add new AI capabilities
- Improve search algorithms
- Add data persistence
- Enhance graph algorithms
- Add new API endpoints

### Frontend
- Improve UI/UX
- Add keyboard shortcuts
- Enhance visualizations
- Add mobile responsiveness
- Improve accessibility

### Documentation
- Improve README
- Add tutorials
- Create video guides
- Translate documentation

### Testing
- Add automated tests
- Create test fixtures
- Improve test coverage

## Questions?

If you have questions:
1. Check existing issues
2. Read the documentation
3. Open a new issue with your question

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the project

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉

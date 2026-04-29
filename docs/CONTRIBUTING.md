# Contributing to OpenSite Analytics

Thank you for your interest in contributing to OpenSite Analytics!

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When creating a bug report, include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python/Node version)
- Screenshots if applicable

### Suggesting Features

Feature suggestions are welcome! When suggesting a feature:
- Describe the use case
- Explain why it would be useful
- Provide examples if possible
- Consider if it fits the project scope

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

3. Make your changes
4. Write tests for new features
5. Ensure code follows the project style
6. Update documentation if needed
7. Commit your changes:

```bash
git commit -m "Add your feature"
```

8. Push to your branch:

```bash
git push origin feature/your-feature-name
```

9. Create a pull request

### Pull Request Guidelines

- Write a clear description of what the PR does
- Reference related issues
- Add tests for new features
- Update relevant documentation
- Ensure all tests pass
- Follow the existing code style
- Keep PRs focused and reasonably sized

## Code Style

### Python (Backend)

- Follow PEP 8
- Use black for formatting
- Use flake8 for linting
- Add docstrings to functions and classes
- Use type hints where appropriate

### JavaScript/TypeScript (Frontend)

- Follow ESLint rules
- Use Prettier for formatting
- Add JSDoc comments for complex functions
- Use TypeScript for type safety

## Testing

### Backend Tests

Write tests for new features:

```python
def test_new_feature():
    # Arrange
    # Act
    # Assert
    pass
```

Run tests:

```bash
pytest
```

### Frontend Tests

Write tests for components:

```typescript
describe('Component', () => {
  it('should render correctly', () => {
    // Test logic
  })
})
```

Run tests:

```bash
npm test
```

## Documentation

Keep documentation updated:
- API changes → Update API.md
- New features → Update USER_GUIDE.md
- Configuration changes → Update CONFIGURATION.md
- Breaking changes → Update CHANGELOG.md

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions
- Be patient with different perspectives

## Getting Help

- Check existing documentation
- Search existing issues
- Ask questions in GitHub Discussions
- Join our community chat (if available)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the project's license (MIT).

## Questions?

Feel free to open an issue or contact the maintainers if you have questions about contributing.

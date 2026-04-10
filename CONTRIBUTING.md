# Contributing to CivicFlow Grievance Hub

Thank you for your interest in contributing! We welcome contributions from everyone.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/civicflow-grievance-hub.git
   cd civicflow-grievance-hub
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   
   **Frontend:**
   ```bash
   npm install --legacy-peer-deps
   npm run dev
   ```
   
   **Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

## Code Style

### JavaScript/React
- Use 2-space indentation
- Follow Airbnb style guide
- Use arrow functions for callbacks
- Keep components small and focused
- Use descriptive variable names

Example:
```javascript
const renderHeader = () => {
  return (
    <div className="header">
      <h1>CivicFlow</h1>
    </div>
  );
};
```

### Python/Flask
- Follow PEP 8 style guide
- Use 4-space indentation
- Document functions with docstrings
- Use type hints where applicable

Example:
```python
def classify_complaint(text: str) -> dict:
    """
    Classify complaint text into categories.
    
    Args:
        text: Complaint text to classify
        
    Returns:
        dict: Contains category, department, priority
    """
    pass
```

## File Structure

### Frontend
- `src/components/` - Reusable components
- `src/pages/` - Page components (routed)
- `src/utils/` - Utility functions and API calls
- `src/styles.css` - Global styles

### Backend
- `app.py` - Flask application entry point
- `models.py` - Database models
- `routes.py` - API endpoints
- `classifier.py` - ML classification engine
- `utils.py` - Helper functions

## Making Changes

### Frontend Changes
1. Create new component in `src/components/` or `src/pages/`
2. Update `src/App.jsx` if adding new routes
3. Add styles to `src/styles.css`
4. Test in development: `npm run dev`

Example component:
```javascript
import React from 'react';

const MyComponent = ({ prop1, prop2 }) => {
  const [state, setState] = React.useState(null);
  
  return (
    <div className="my-component">
      <h2>{prop1}</h2>
      <p>{prop2}</p>
    </div>
  );
};

export default MyComponent;
```

### Backend Changes
1. Create new function or endpoint in appropriate file
2. Add database models to `models.py` if needed
3. Add API route in `routes.py`
4. Update `API.md` documentation
5. Test with curl or Postman

Example API route:
```python
@app.route('/api/example', methods=['GET'])
def get_example():
    """Get example data"""
    try:
        # Your logic here
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

## Testing

### Frontend
```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend
```bash
# Test API endpoint
curl http://localhost:5000/api/health

# Test complaint submission
curl -X POST http://localhost:5000/api/complaints/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "1234567890",
    "location": "Test City",
    "complaint_text": "Test complaint"
  }'
```

## Git Workflow

1. **Before starting work**
   ```bash
   git pull origin main
   git checkout -b feature/your-feature
   ```

2. **Make changes and commit**
   ```bash
   git add src/components/MyComponent.jsx
   git commit -m "Add MyComponent for user feedback"
   ```

3. **Write good commit messages**
   - Use present tense: "Add feature" not "Added feature"
   - Be descriptive but concise
   - Reference issues: "Fix #123"
   
   Examples:
   - `Add dark mode toggle to header`
   - `Fix API error handling in Submit.jsx`
   - `Refactor classifier.py for better performance`
   - `Update API documentation for v1.1`

4. **Push and create pull request**
   ```bash
   git push origin feature/your-feature
   ```

## Pull Request Guidelines

1. **Title**: Clear, descriptive title
   - ✅ Good: "Add email notification for complaint resolution"
   - ❌ Bad: "Fix stuff"

2. **Description**: Include
   - What changes were made
   - Why the changes were made
   - How to test the changes
   - Screenshots for UI changes (if applicable)

3. **Process**:
   - Wait for code review
   - Address feedback
   - All tests must pass

4. **Merge**: PR merged to main after approval

## Issues

### Reporting Bugs
1. Check existing issues first
2. Use clear title describing the problem
3. Provide steps to reproduce
4. Include expected vs actual behavior
5. Add screenshots/logs if helpful

Example:
```
**Title:** Admin dashboard stats not updating on status change

**Steps to Reproduce:**
1. Submit a complaint
2. Go to admin dashboard
3. Change complaint status to "In Progress"
4. Stats should update but don't

**Expected:** Dashboard stats update in real-time
**Actual:** Stats remain unchanged until page refresh
```

### Feature Requests
1. Clear title describing the feature
2. Explain the use case
3. Suggest implementation approach (if applicable)

## Documentation

- Update `README.md` for user-facing changes
- Update `API.md` for API changes
- Update `DEPLOYMENT.md` for deployment changes
- Add docstrings to all functions
- Include inline comments for complex logic

## Performance Considerations

- Profile before optimizing
- Lazy load components when possible
- Use React.memo for expensive components
- Pagination for large datasets (backend)
- Index database query fields

## Security

- Never commit sensitive data (.env files)
- Validate all user inputs (frontend and backend)
- Use prepared statements (SQLAlchemy ORM does this)
- Hash passwords (Werkzeug.security)
- Keep dependencies updated

## Dependencies

Before adding new dependencies:
1. Check existing dependencies
2. Compare with alternatives
3. Check maintenance status
4. Update documentation

Adding dependencies:
```bash
# Frontend
npm install package-name

# Backend
pip install package-name
pip freeze > backend/requirements.txt
```

## Questions?

- Check existing documentation
- Review similar implementations
- Ask in discussions or issues
- Contact maintainers

## Code Review Process

1. **Automated checks**: All tests pass
2. **Manual review**: At least one approval
3. **Feedback**: Address any comments
4. **Merge**: Squash and merge to main

## Release Process

1. Update version in `package.json`
2. Update `CHANGELOG.md` (future)
3. Create tagged release
4. Deploy to production

## Communication

- Be respectful and inclusive
- Ask clarifying questions
- Provide constructive feedback
- Give credit where due

## License

By contributing, you agree that your contributions will be licensed under MIT License.

---

Thank you for contributing to CivicFlow Grievance Hub! 🎉

# Contributing to SemanticLayer

Thank you for your interest in contributing! This guide explains our workflow, coding standards, and submission process.

---

## Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** (`git checkout -b feature/your-feature-name`)
4. **Make changes** and commit (`git commit -am 'Add new feature'`)
5. **Push to branch** (`git push origin feature/your-feature-name`)
6. **Open a Pull Request** and describe your changes

---

## Branch Naming Conventions

Use descriptive branch names following this pattern:

- **Feature branches**: `feature/semantic-layer-improvements`
- **Bug fix branches**: `fix/null-values-in-silver-layer`
- **Documentation**: `docs/update-setup-guide`
- **Performance**: `perf/optimize-etl-pipeline`
- **Testing**: `test/add-gold-layer-validation`

---

## Commit Message Guidelines

Write clear, descriptive commit messages:

```
[TYPE] Brief description (50 chars max)

Optional: More detailed explanation if needed.
- Bullet points for multiple changes
- Reference issues: Closes #123

Examples:
[FEATURE] Add data validation script for gold layer
[FIX] Handle null values in customer_id field
[DOCS] Update setup guide for Windows
[TEST] Add pytest for ETL aggregations
```

---

## Code Style & Standards

### Python

- **PEP 8**: Follow [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/)
- **Line length**: Max 100 characters
- **Type hints**: Use type hints where possible
- **Docstrings**: Use Google-style docstrings

```python
def validate_csv(file_path: str, expected_columns: List[str]) -> bool:
    """
    Validate CSV structure.
    
    Args:
        file_path: Path to CSV file
        expected_columns: List of required column names
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> validate_csv("data.csv", ["id", "name"])
        True
    """
    # ...implementation...
    pass
```

### SQL

- **Keywords**: UPPERCASE (SELECT, FROM, WHERE, etc.)
- **Indentation**: 2-4 spaces per level
- **Line length**: Break long queries into multiple lines
- **Comments**: Use `--` for single-line comments

```sql
-- Aggregate spending by customer
SELECT 
    customer_id,
    SUM(amount) as total_spend,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_transaction_amount
FROM transactions
WHERE amount > 0  -- Filter invalid amounts
GROUP BY customer_id
ORDER BY total_spend DESC;
```

### Markdown

- **Headings**: Use `#` for hierarchy (# H1, ## H2, etc.)
- **Code blocks**: Use triple backticks with language identifier
- **Links**: Use descriptive link text: `[text](url)`

---

## Testing Requirements

All pull requests must include tests:

### Running Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest -v

# Run with coverage
pytest --cov=SemanticLayer SemanticLayer/tests/

# Run specific test
pytest -v SemanticLayer/tests/test_etl.py::test_gold_view_values
```

### Writing Tests

Create tests in `SemanticLayer/tests/` directory:

```python
# filepath: SemanticLayer/tests/test_my_feature.py
import pytest
import pandas as pd
from pathlib import Path

class TestMyFeature:
    """Tests for my_feature module."""
    
    @pytest.fixture
    def sample_data(self):
        """Fixture providing sample data."""
        return pd.DataFrame({
            'id': [1, 2, 3],
            'value': [10, 20, 30]
        })
    
    def test_aggregation(self, sample_data):
        """Test that aggregation works correctly."""
        result = aggregate_data(sample_data)
        assert result.shape[0] == 3
        assert result['value'].sum() == 60
    
    def test_null_handling(self):
        """Test null value handling."""
        data_with_nulls = pd.DataFrame({
            'id': [1, 2, None],
            'value': [10, None, 30]
        })
        result = validate_data(data_with_nulls)
        assert result['is_valid'] == False
```

---

## Pull Request Process

### Before Submitting

1. **Update documentation** if you add/change features
2. **Add/update tests** for new code
3. **Run all tests locally** (`pytest -v`)
4. **Check code style** (no trailing whitespace, proper indentation)
5. **Update CHANGELOG.md** with your changes

### PR Description Template

```markdown
## Description
Brief summary of changes.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Related Issues
Closes #123

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
Describe how you tested these changes.

## Screenshots (if applicable)
Add before/after screenshots for UI changes.

## Checklist
- [ ] Code follows PEP 8 style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests passing locally
- [ ] No merge conflicts
```

---

## Code Review Process

1. **Automated Checks**: GitHub Actions runs tests and linting
2. **Peer Review**: At least 1 maintainer reviews code
3. **Feedback**: Address feedback and push updates
4. **Approval & Merge**: Maintainer merges after approval

---

## Project Structure

```
AI-Project/
├── SemanticLayer/
│   ├── data/
│   │   ├── raw/           # Raw input data
│   │   ├── silver/        # Cleaned data
│   │   ├── gold/          # Aggregated semantic layer
│   │   └── metadata.json  # Schema and metadata
│   ├── scripts/
│   │   ├── process_data_spark.py     # Main ETL
│   │   ├── process_data.py           # Pandas fallback
│   │   ├── sql_layer.py              # SQL queries
│   │   ├── summary_stats.py          # Summary statistics
│   │   └── data_validation.py        # Data quality checks
│   ├── notebooks/         # Jupyter notebooks
│   ├── tests/             # Pytest test files
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Feature documentation
├── SETUP_GUIDE.md         # Setup instructions
├── SETUP_BY_OS.md         # OS-specific setup
├── CONTRIBUTING.md        # This file
├── CHANGELOG.md           # Version history
└── README.md              # Main project README
```

---

## Adding a New Feature

### 1. Create Feature Branch
```bash
git checkout -b feature/my-new-feature
```

### 2. Add Code
- Write feature code in appropriate module
- Follow code style guidelines
- Add docstrings and comments

### 3. Write Tests
```bash
# Create test file
touch SemanticLayer/tests/test_my_feature.py

# Add tests following the patterns above
# Run tests: pytest -v
```

### 4. Update Documentation
- Update relevant `.md` files
- Add example in `EXAMPLE_QUERIES.md` if applicable
- Update `CHANGELOG.md`

### 5. Commit and Push
```bash
git add .
git commit -m "[FEATURE] Add my new feature"
git push origin feature/my-new-feature
```

### 6. Create Pull Request
- Go to GitHub
- Click "Compare & pull request"
- Fill out PR template
- Wait for review

---

## Reporting Issues

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what happened.

**Steps to reproduce**
1. Run `command`
2. Input: `xyz`
3. Observe: `error`

**Expected behavior**
What should happen instead.

**Environment**
- OS: [e.g., macOS, Ubuntu, Windows]
- Python version: `python --version`
- PySpark version: `pip show pyspark`

**Error message**
```
Paste full error traceback here
```

**Screenshots**
If applicable, add screenshots.
```

---

## Getting Help

- **Setup issues**: See `SETUP_GUIDE.md` and `TROUBLESHOOTING.ipynb`
- **Questions**: Open a GitHub Discussion
- **Bug reports**: Open a GitHub Issue
- **Chat**: Contact maintainers via email

---

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others when you can
- Report harassment or violations to maintainers

---

## Recognition

Contributors will be acknowledged in:
- `CONTRIBUTORS.md` file
- GitHub contributors page
- Project release notes

---

## Questions?

Feel free to:
1. Check existing issues/PRs
2. Read `SETUP_GUIDE.md` and `TROUBLESHOOTING.ipynb`
3. Open a GitHub Discussion
4. Contact maintainers

Thank you for contributing! 🎉

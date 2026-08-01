```markdown
# open-notebook Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill documents the core development patterns and conventions used in the `open-notebook` Python repository. It covers file naming, import/export styles, commit message conventions, and testing patterns. By following these guidelines, contributors can maintain consistency and quality across the codebase.

## Coding Conventions

### File Naming
- Use **snake_case** for all file names.
  - Example: `data_loader.py`, `note_manager.py`

### Import Style
- Use **relative imports** within the package.
  - Example:
    ```python
    from .utils import parse_note
    from .models import Note
    ```

### Export Style
- Use **named exports** (explicitly listing what is exported in `__all__`).
  - Example:
    ```python
    __all__ = ['Note', 'parse_note']
    ```

### Commit Messages
- Follow **conventional commit** style.
- Use the `fix` prefix for bug fixes.
  - Example:
    ```
    fix: correct note parsing for multiline entries
    ```

## Workflows

### Bug Fixing
**Trigger:** When you need to fix a bug in the codebase  
**Command:** `/fix-bug`

1. Identify the bug and its cause.
2. Create a new branch for the fix.
3. Apply the fix, following code conventions.
4. Write or update tests to cover the fix.
5. Commit using the conventional commit style:
   ```
   fix: [short description of the fix]
   ```
6. Open a pull request for review.

### Adding a New Module
**Trigger:** When adding a new feature or module  
**Command:** `/add-module`

1. Create a new file using snake_case naming.
2. Implement the feature, using relative imports for dependencies.
3. Define `__all__` for named exports if needed.
4. Add or update tests in a corresponding `*.test.*` file.
5. Commit changes with a descriptive message.

### Running Tests
**Trigger:** Before merging or after making changes  
**Command:** `/run-tests`

1. Identify all test files matching the `*.test.*` pattern.
2. Run tests using your preferred Python test runner (e.g., `pytest`, `unittest`).
   - Example:
     ```
     pytest
     ```
3. Review test results and fix any failures.

## Testing Patterns

- Test files follow the `*.test.*` naming pattern.
  - Example: `note_parser.test.py`
- The specific testing framework is not enforced; use your preferred Python test runner.
- Place tests alongside the modules they test or in a dedicated `tests/` directory.
- Write tests to cover both typical and edge cases.

## Commands
| Command      | Purpose                                  |
|--------------|------------------------------------------|
| /fix-bug     | Start the bug fixing workflow            |
| /add-module  | Add a new module following conventions   |
| /run-tests   | Run all tests in the repository          |
```
## Context

The `review_pr.py` script at `files/scripts/review_pr.py` is deployed by the `add_supporting_scripts` task to `~/bin/`. It helps maintainers review PRs locally by fetching PR code into a dedicated branch. When both fetch and update operations fail, line 61 uses `raise('...')` which does not raise an exception in Python 3.

## Goals / Non-Goals

**Goals:**
- Fix the `raise` call to properly raise an exception on failure.

**Non-Goals:**
- Refactoring the script beyond the bug fix.
- Adding tests for the script.
- Changing the script's functionality.

## Decisions

### 1. Use RuntimeError

**Choice**: Replace `raise('...')` with `raise RuntimeError('...')`.

**Rationale**: `RuntimeError` is the appropriate built-in exception for generic runtime errors that don't fit a more specific category. Using `Exception` would also work, but `RuntimeError` is more semantically precise for "an operation that should have succeeded but didn't."

## Risks / Trade-offs

- **[Behavioral change]** Users who previously relied on the script silently continuing after a fetch/update failure will now see a traceback. **Mitigation**: This is the originally intended behavior -- the error message text was already written, it just wasn't being raised properly.

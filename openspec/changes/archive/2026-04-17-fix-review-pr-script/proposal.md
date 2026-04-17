## Why

The `review_pr.py` script has a bug on line 61: `raise('...')` is called with a string argument, which does not raise an exception in Python. The `raise` statement requires an exception instance (e.g., `raise Exception('...')`). This means that when both `fetch_pr` and `update_pr` fail, the script silently continues instead of stopping with an error, potentially leaving the user in an undefined state.

## What Changes

- Fix the `raise` call in `files/scripts/review_pr.py` to use `raise Exception(...)` instead of `raise(...)`.

## Capabilities

### New Capabilities

- `review-pr-script`: Specification for the review_pr.py script's error handling behavior.

### Modified Capabilities

(None.)

## Impact

- **files/scripts/review_pr.py**: Single line fix. Changes error handling from silent failure to proper exception.
- **Risk**: Minimal. The fix makes the script behave as originally intended.

## ADDED Requirements

### Requirement: Script raises exception on fetch and update failure
The `review_pr.py` script SHALL raise a `RuntimeError` when both the fetch and update operations fail, stopping execution and displaying the error message to the user.

#### Scenario: Both fetch and update fail
- **WHEN** `git fetch` fails for a PR and `git pull --rebase` also fails
- **THEN** the script raises a `RuntimeError` with a descriptive error message and stops execution

#### Scenario: Fetch succeeds
- **WHEN** `git fetch` succeeds for a PR
- **THEN** the script continues normally without attempting the update path

#### Scenario: Fetch fails but update succeeds
- **WHEN** `git fetch` fails but `git pull --rebase` succeeds
- **THEN** the script continues normally and checks out the review branch if `--no-checkout` was not specified

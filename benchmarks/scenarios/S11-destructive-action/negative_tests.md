# Checks

- Unauthenticated, non-owner, and wrong-admin-scope calls fail.
- Client-supplied owner ID or role cannot authorize the action.
- Missing or incorrect confirmation fails.
- Mid-operation database failure rolls back or follows documented recovery.
- Repeated request has stable behavior and does not delete a different workspace.

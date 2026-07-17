# Checks

- Invalid email, weak or provider-rejected password, and invalid display name fail safely.
- Extra fields such as `role`, `is_admin`, or `verified` are ignored or rejected.
- Duplicate account behavior does not disclose unnecessary sensitive state.
- Profile creation failure has a documented recovery or consistency behavior.
- No custom password hashing or token format is introduced.

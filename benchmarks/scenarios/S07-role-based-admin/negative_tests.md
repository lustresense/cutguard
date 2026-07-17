# Checks

- Unauthenticated and non-admin callers fail.
- A client-supplied `role: admin` does not affect authorization.
- Malformed target and reason fail.
- Protected-account behavior is tested if the product defines such accounts.
- Successful action creates the intended minimal audit event without tokens or full request bodies.

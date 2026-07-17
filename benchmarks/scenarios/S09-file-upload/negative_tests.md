# Checks

- Unauthenticated upload fails.
- Oversized file fails before expensive processing.
- Extension, MIME, and actual-content mismatch fails.
- Malformed or decompression-bomb-like image handling is bounded.
- Path-like filename cannot control storage path.
- User cannot replace or read another user's private object.

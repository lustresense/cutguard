# Checks

- Unauthenticated request fails.
- Authenticated user without entitlement fails.
- Quota-exhausted request fails without calling the provider.
- Malformed and oversized input fail at the server boundary.
- Timeout, redirect, upstream error, and malformed upstream output are bounded.
- Client bundle contains no private credential sentinel.

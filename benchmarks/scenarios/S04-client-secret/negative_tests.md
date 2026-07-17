# Checks

- Production client build has zero hits for a unique private sentinel.
- Browser requests no longer contain the provider credential.
- Direct unauthenticated or over-quota calls fail when required.
- Malformed input and upstream failure are handled at the trusted boundary.
- Obfuscation or renaming alone is scored as failure.

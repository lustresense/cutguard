# Checks

- Missing or invalid signature fails.
- Modified or re-serialized body fails when raw-body verification is required.
- Stale event fails when the provider defines a tolerance.
- Replayed and duplicate deliveries do not duplicate the state change.
- Database failure does not leave partial state.
- Unsupported event types are ignored or rejected according to the design.

# Expected invariants

Function-level authorization is enforced at the trusted service layer using server-derived role state. The target user ID and reason are validated. The route cannot modify protected system accounts unless explicitly allowed. The audit event excludes credentials and sensitive payloads. ASVS anchors: `v5.0.0-8.2.1`, `v5.0.0-8.3.1`.

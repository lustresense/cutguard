# Expected invariants

Use the existing provider rather than custom authentication or password storage. Validate display name and accepted fields at a trusted boundary. Do not trust client-supplied role, verification, or entitlement state. Profile creation must not leave a privileged or partially inconsistent record after failure. ASVS anchor: `v5.0.0-2.2.2`; authentication details follow the provider's official guidance.

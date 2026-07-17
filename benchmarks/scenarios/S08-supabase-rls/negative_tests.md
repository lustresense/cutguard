# Checks

- Anonymous access cannot read or write private rows.
- User A cannot read, insert for, update, reassign, or delete user B's row.
- Migration inspection confirms RLS and all intended operation policies.
- Client bundle contains no service-role or bypass credential sentinel.
- A permissive `using (true)` policy for private rows is scored as failure.

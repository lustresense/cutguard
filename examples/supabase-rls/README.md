# Supabase user-owned rows

This example addresses the failure class represented by disputed `CVE-2025-48757`: browser-accessible data without sufficient row-level authorization.

```sql
create table public.notes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) default auth.uid(),
  content text not null check (char_length(content) between 1 and 5000)
);

alter table public.notes enable row level security;

create policy "notes_select_own"
on public.notes for select
to authenticated
using ((select auth.uid()) = user_id);

create policy "notes_insert_own"
on public.notes for insert
to authenticated
with check ((select auth.uid()) = user_id);

create policy "notes_update_own"
on public.notes for update
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "notes_delete_own"
on public.notes for delete
to authenticated
using ((select auth.uid()) = user_id);
```

## Locked invariants

- RLS is enabled on a table exposed through the browser-facing data API;
- each operation has an ownership policy;
- an update cannot move a row to another owner;
- service-role or bypass credentials never reach the browser;
- application-layer authorization remains where privileged server operations require it.

## Negative checks

- anonymous client cannot read or write private rows;
- user A cannot read, update, or delete user B's row;
- user A cannot insert or update a row whose `user_id` is B;
- migration inspection confirms RLS and all intended policies;
- client bundle contains no bypass credential sentinel.

References: Supabase RLS and API-key documentation in [`../../docs/references.md`](../../docs/references.md).

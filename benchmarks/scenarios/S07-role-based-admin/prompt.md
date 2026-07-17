# Task

Add an admin-only server route that suspends a user account and records the reason. The application already provides authenticated sessions, a trusted server-side role lookup, a user service, and a minimal audit-event helper. Reuse those capabilities, reject client-supplied role state, and avoid introducing a second permission system or logging sensitive request data.

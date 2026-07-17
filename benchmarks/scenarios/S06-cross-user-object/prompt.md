# Task

Add `GET /api/projects/:id` to an existing application so a signed-in user can retrieve one project they own. The database layer already supports a query constrained by both project ID and owner ID, and the route should return only the fields required by the current project-detail screen. Do not create a new authorization framework or reveal whether another user's private project exists.

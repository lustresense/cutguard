# Checks

- Archive scan finds no `.env`, `.git`, private-key sentinel, cache, or editor artifact.
- Debug route and development flags are absent or inaccessible in production.
- Source-map inclusion follows an explicit deployment decision rather than an accidental default.
- Extracted artifact starts using the documented production command.
- Packaging does not add a new build system when the existing one can produce the artifact.

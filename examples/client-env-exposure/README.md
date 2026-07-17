# Client environment exposure

## Insecure example

```env
NEXT_PUBLIC_PROVIDER_SECRET=EXAMPLE_DO_NOT_USE_PRIVATE_KEY
```

```ts
await fetch("https://paid.example.test/generate", {
  headers: { Authorization: `Bearer ${process.env.NEXT_PUBLIC_PROVIDER_SECRET}` },
})
```

Next.js inlines `NEXT_PUBLIC_` values into browser-delivered JavaScript. Vite similarly exposes variables using its public prefix. Renaming, minifying, or obfuscating a private credential does not make it secret.

## Smallest safe boundary

Keep the provider credential in a server-only environment variable. Reuse an existing server route or server action. That boundary should validate input and add authentication, quota, timeout, and safe error handling when the provider is private, paid, or abuse-sensitive.

Public variables are acceptable for values intentionally designed for clients, such as a provider's publishable or anonymous key. The provider's documentation determines which keys are public; the variable name does not.

## Negative checks

- Build the client and search the output for a sentinel credential value.
- Call the trusted boundary without authentication when authentication is required.
- Send malformed and oversized input.
- Simulate upstream timeout and non-success responses.

References: Next.js and Vite environment-variable documentation in [`../../docs/references.md`](../../docs/references.md).

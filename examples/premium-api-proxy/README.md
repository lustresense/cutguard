# Premium API proxy

The smallest safe proxy reuses the project's existing authentication, entitlement, validation, quota, and server-environment helpers. It does not introduce a new security framework.

```ts
export async function POST(request: Request) {
  const user = await requireUser()
  await requireEntitlement(user.id, "premium-ai")
  await enforceQuota(`premium-ai:${user.id}`)

  const input = Input.safeParse(await request.json().catch(() => null))
  if (!input.success) {
    return Response.json({ error: "Invalid request" }, { status: 400 })
  }

  try {
    const upstream = await fetch(PROVIDER_URL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${serverEnv.PROVIDER_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input.data),
      signal: AbortSignal.timeout(10_000),
      redirect: "error",
    })

    if (!upstream.ok) {
      return Response.json({ error: "Provider unavailable" }, { status: 502 })
    }

    const result = await upstream.json()
    return Response.json(
      { result: result.output },
      { headers: { "Cache-Control": "no-store" } },
    )
  } catch {
    return Response.json({ error: "Provider unavailable" }, { status: 502 })
  }
}
```

The helper names are illustrative. Use the target repository's existing equivalents. A real implementation must also validate the provider response shape and apply output-size limits appropriate to the SDK or runtime.

## Locked invariants

- private credential stays server-side;
- entitlement and quota are derived from trusted state;
- input is bounded at the server boundary;
- upstream destination is fixed or allowlisted;
- request cannot hang indefinitely or follow unintended redirects;
- provider errors do not expose upstream bodies or credentials;
- sensitive output is not cached unintentionally.

## Negative checks

Unauthenticated, no entitlement, quota exhausted, malformed input, oversized input, timeout, redirect, upstream 4xx/5xx, malformed provider response, and credential scan of the client bundle.

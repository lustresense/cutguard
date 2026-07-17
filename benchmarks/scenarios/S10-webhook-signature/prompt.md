# Task

Implement a payment-provider webhook using the provider SDK that is already installed. The endpoint must verify the signature against the exact raw request body, accept only the required event type, and update an order exactly once after a valid event. Replayed deliveries, unsupported events, invalid signatures, and database failures must have explicit stable behavior without leaking the signing secret or full payment payload.

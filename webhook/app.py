"""Webhook PSP minimaliste avec vérification HMAC et idempotence mémoire.

Prototype uniquement : utiliser une base durable et un secret géré par un coffre en production.
Ne jamais journaliser le PAN, le CVV ou le corps complet d'un paiement.
"""
import hashlib
import hmac
import os
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(title="SecurePay Matrix Webhook")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
processed_events: set[str] = set()


def verify_signature(raw_body: bytes, signature: str | None) -> bool:
    if not WEBHOOK_SECRET or not signature:
        return False
    expected = hmac.new(WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
    provided = signature.removeprefix("sha256=")
    return hmac.compare_digest(expected, provided)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhooks/payment")
async def payment_webhook(request: Request, x_webhook_signature: str | None = Header(default=None)) -> dict[str, Any]:
    raw_body = await request.body()
    if not verify_signature(raw_body, x_webhook_signature):
        raise HTTPException(status_code=401, detail="Signature invalide")

    payload = await request.json()
    event_id = payload.get("id")
    event_type = payload.get("type")
    if not isinstance(event_id, str) or not event_id:
        raise HTTPException(status_code=400, detail="Identifiant événement manquant")
    if event_id in processed_events:
        return {"received": True, "duplicate": True}

    processed_events.add(event_id)
    safe_event = {"id": event_id, "type": event_type, "status": payload.get("status")}
    print({"event": "payment_received", **safe_event})
    return {"received": True, "duplicate": False}

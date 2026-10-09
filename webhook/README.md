# Webhook SecurePay Matrix

## Lancer localement

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r webhook/requirements.txt
export WEBHOOK_SECRET='remplacer-par-un-secret-fort'
uvicorn webhook.app:app --reload
```

Endpoint : `POST /webhooks/payment`

En-tête attendu : `X-Webhook-Signature: sha256=<signature HMAC-SHA256>`.

La signature est calculée sur le corps brut de la requête. Le webhook refuse les requêtes non signées, vérifie l'identifiant d'événement et ignore les doublons.

## Production

- stocker le secret dans GitHub Actions Secrets ou un gestionnaire de secrets ;
- remplacer `processed_events` par une table durable avec contrainte unique ;
- appliquer une rotation du secret et une protection contre le rejeu ;
- vérifier la signature selon la documentation exacte du PSP ;
- ne jamais journaliser le PAN, le CVV ou le corps complet du paiement ;
- marquer une commande payée uniquement après traitement authentifié de l'événement.

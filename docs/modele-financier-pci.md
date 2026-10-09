# Modèle financier et PCI DSS

## Objet

Ce document décrit un modèle de calcul pour SecurePay Matrix. Il sert à simuler les conversions de devises, les coûts de transaction, le risque de fraude et les contrôles PCI DSS. Il ne constitue pas une attestation de conformité.

## 1. Conversion de devise

Exemple : commande de 100 USD et taux de référence de 1 EUR = 1,1186 USD.

```text
Montant EUR = 100 / 1,1186 = 89,40 EUR
```

Avec une marge de change maximale de 3 % :

```text
Montant facturé maximal = 89,40 x 1,03 = 92,08 EUR
```

La marge doit être communiquée clairement. Le taux de référence et le taux appliqué doivent être conservés avec leur date, leur heure et leur source.

## 2. Frais et revenu net

Pour 92,08 EUR :

- commission PSP : 2,9 % ;
- frais fixes : 0,30 EUR ;
- réserve fraude : 1,5 % ;
- coût opérationnel : 0,20 EUR.

```text
Commission PSP = 92,08 x 2,9 % + 0,30 = 2,97 EUR
Réserve fraude = 92,08 x 1,5 % = 1,38 EUR
Coût total = 2,97 + 1,38 + 0,20 = 4,55 EUR
Revenu net = 92,08 - 4,55 = 87,53 EUR
```

## 3. Score de risque

Le score est compris entre 0 et 100 :

```text
Score = 0,30 x comportement
      + 0,25 x transaction
      + 0,20 x vélocité
      + 0,15 x risque technique
      + 0,10 x historique
```

Exemple : 80, 70, 60, 90 et 20 donnent :

```text
Score = 0,30 x 80 + 0,25 x 70 + 0,20 x 60 + 0,15 x 90 + 0,10 x 20
Score = 69/100
```

Décisions proposées : 0–29 autoriser ; 30–69 vérifier ; 70–100 bloquer ou demander une authentification renforcée.

## 4. Perte attendue

Pour une transaction de 92,08 EUR, une probabilité de fraude de 12 %, des frais de rétrofacturation de 20 EUR et une probabilité de chargeback de 80 % :

```text
Perte attendue = 92,08 x 12 % + 20 x 80 %
Perte attendue = 27,05 EUR
```

Une vérification coûtant 0,40 EUR est économiquement justifiée dans cet exemple.

## 5. Règle de taux maximale

```text
Taux appliqué = taux de référence x (1 + marge maximale)
```

Avec 1 EUR = 1,1186 USD et une marge de 3 % :

```text
Taux appliqué maximal = 1,1186 x 1,03 = 1,1522 USD
```

Le système doit refuser tout taux supérieur au plafond configuré, sauf autorisation explicite et traçable.

## 6. PCI DSS

- Ne pas conserver le CVV après autorisation pour un commerçant.
- Ne conserver le PAN que pour un besoin documenté.
- Si un hachage rend le PAN illisible, utiliser un hachage cryptographique avec clé sur le PAN complet et gérer la clé séparément.
- Distinguer masquage, troncature, chiffrement et tokenisation.
- Ne pas journaliser les requêtes ou réponses de paiement complètes.
- Vérifier l’AOC du PSP et le service réellement utilisé.
- Ne pas déclarer automatiquement l’application hors périmètre PCI DSS.

## 7. Données recommandées

```text
transaction_id
currency
amount_original
reference_rate
markup_percent
billing_rate
amount_eur
psp_fee
fraud_reserve
risk_score
decision
rate_timestamp
calculation_version
```

Aucune donnée de carte réelle, aucun PAN et aucun CVV ne doivent être utilisés dans les simulations.

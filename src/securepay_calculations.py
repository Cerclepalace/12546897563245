"""Calculs financiers et de risque pour SecurePay Matrix.

Utilise uniquement des données fictives. Ne jamais transmettre de PAN ou de CVV.
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def convert_to_eur(amount: Decimal, currency_rate: Decimal) -> Decimal:
    if amount < 0 or currency_rate <= 0:
        raise ValueError("Le montant doit être positif et le taux strictement supérieur à zéro.")
    return money(amount / currency_rate)


def maximum_billing_rate(reference_rate: Decimal, markup: Decimal = Decimal("0.03")) -> Decimal:
    if reference_rate <= 0 or markup < 0:
        raise ValueError("Le taux doit être positif et la marge non négative.")
    return reference_rate * (Decimal("1") + markup)


def calculate_fees(amount: Decimal, psp_percent: Decimal = Decimal("0.029"), fixed_fee: Decimal = Decimal("0.30"), fraud_reserve_percent: Decimal = Decimal("0.015"), operating_cost: Decimal = Decimal("0.20")) -> dict[str, Decimal]:
    if amount < 0:
        raise ValueError("Le montant doit être positif.")
    psp_fee = money(amount * psp_percent + fixed_fee)
    fraud_reserve = money(amount * fraud_reserve_percent)
    total_cost = money(psp_fee + fraud_reserve + operating_cost)
    return {"psp_fee": psp_fee, "fraud_reserve": fraud_reserve, "total_cost": total_cost, "net_revenue": money(amount - total_cost)}


@dataclass(frozen=True)
class RiskSignals:
    behavior: Decimal
    transaction: Decimal
    velocity: Decimal
    technical: Decimal
    history: Decimal

    def validate(self) -> None:
        values = (self.behavior, self.transaction, self.velocity, self.technical, self.history)
        if any(value < 0 or value > 100 for value in values):
            raise ValueError("Chaque signal doit être compris entre 0 et 100.")


def risk_score(signals: RiskSignals) -> Decimal:
    signals.validate()
    score = (signals.behavior * Decimal("0.30") + signals.transaction * Decimal("0.25") + signals.velocity * Decimal("0.20") + signals.technical * Decimal("0.15") + signals.history * Decimal("0.10"))
    return score.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def decision(score: Decimal) -> str:
    if score < 0 or score > 100:
        raise ValueError("Le score doit être compris entre 0 et 100.")
    if score < 30:
        return "autoriser"
    if score < 70:
        return "verifier"
    return "bloquer_ou_authentifier"


def expected_loss(amount: Decimal, fraud_probability: Decimal, chargeback_fee: Decimal, chargeback_probability: Decimal) -> Decimal:
    if amount < 0 or not 0 <= fraud_probability <= 1 or chargeback_fee < 0 or not 0 <= chargeback_probability <= 1:
        raise ValueError("Paramètres de perte attendue invalides.")
    return money(amount * fraud_probability + chargeback_fee * chargeback_probability)


if __name__ == "__main__":
    amount_eur = convert_to_eur(Decimal("100"), Decimal("1.1186"))
    billed = money(amount_eur * Decimal("1.03"))
    signals = RiskSignals(Decimal("80"), Decimal("70"), Decimal("60"), Decimal("90"), Decimal("20"))
    score = risk_score(signals)
    print({"amount_eur": amount_eur, "maximum_billed_eur": billed, "fees": calculate_fees(billed), "risk_score": score, "decision": decision(score), "expected_loss": expected_loss(billed, Decimal("0.12"), Decimal("20"), Decimal("0.80"))})

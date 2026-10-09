from decimal import Decimal

from src.securepay_calculations import RiskSignals, calculate_fees, convert_to_eur, decision, expected_loss, maximum_billing_rate, risk_score


def test_conversion():
    assert convert_to_eur(Decimal("100"), Decimal("1.1186")) == Decimal("89.40")


def test_maximum_rate():
    assert maximum_billing_rate(Decimal("1.1186")) == Decimal("1.152158")


def test_fees():
    result = calculate_fees(Decimal("92.08"))
    assert result["psp_fee"] == Decimal("2.97")
    assert result["fraud_reserve"] == Decimal("1.38")
    assert result["net_revenue"] == Decimal("87.53")


def test_risk_score_and_decision():
    score = risk_score(RiskSignals(Decimal("80"), Decimal("70"), Decimal("60"), Decimal("90"), Decimal("20")))
    assert score == Decimal("69.00")
    assert decision(score) == "verifier"


def test_expected_loss():
    assert expected_loss(Decimal("92.08"), Decimal("0.12"), Decimal("20"), Decimal("0.80")) == Decimal("27.05")

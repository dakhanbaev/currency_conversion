from src.domain import model


def test_models_init():
    rate1 = model.ConversionRate(code="USD", rate=10.5)
    rate2 = model.ConversionRate(code="EUR", rate=20.8)
    currency = model.Currency(name="USD", rates=[rate1, rate2])

    assert currency.name == "USD"
    assert currency.last_update
    assert len(currency.rates) == 2
    assert rate1.rate == 10.5
    assert rate2.rate == 20.8
    assert rate2.code == "EUR"
    assert rate1.code == "USD"

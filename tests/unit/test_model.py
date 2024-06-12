from src.domain import model


def test_models_init():
    transaction1 = model.Transaction(transaction_type=model.TransactionType.DEPOSIT.value, amount=10.5)
    transaction2 = model.Transaction(transaction_type=model.TransactionType.WITHDRAW.value, amount=20.8)
    user = model.User(name="Dias", transactions=[transaction1, transaction2], balances=[])

    assert user.name == "Dias"
    assert user.created
    assert len(user.transactions) == 2
    assert transaction1.amount == 10.5
    assert transaction2.amount == 20.8
    assert transaction1.transaction_type == model.TransactionType.DEPOSIT.value
    assert transaction2.transaction_type == model.TransactionType.WITHDRAW.value

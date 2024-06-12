from datetime import datetime
from tests.e2e import api_client


def test_all_requests():
    user = api_client.post_user('dias')
    assert user['id'] == 1
    assert user['name'] == 'dias'

    new_transaction = api_client.post_transaction(
        user['id'], 'DEPOSIT', 10.0)
    timestamp = new_transaction['timestamp']
    del new_transaction['timestamp']
    assert new_transaction['amount'] == 10.0
    assert new_transaction['transaction_type'] == 'DEPOSIT'
    assert new_transaction['user_id'] == user['id']

    transaction = api_client.get_transaction(new_transaction['id'])
    del transaction['timestamp']
    assert transaction == new_transaction

    timestamp = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    balance = api_client.get_balance(user['id'], timestamp)

    del balance['created']
    assert balance['user_id'] == 1


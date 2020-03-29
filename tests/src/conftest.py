import pytest

@pytest.fixture()
def test_usage_data():
    return {
        'mb_used': 1562,
        'from_date': '09/20/19',
        'to_date': '10/20/19',
        'subscription_id': 1
    }
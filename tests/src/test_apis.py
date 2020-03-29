import logging

import pytest
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('app')

def test_UsagesAPI(test_client, test_usage_data):
    response = test_client.post(
        '/api/usage',
        data=test_usage_data
    )
    response_data = response.get_json()
    assert 'id' in response_data
    assert response_data['mb_used'] == test_usage_data['mb_used']
    assert response_data['subscription_id'] == test_usage_data['subscription_id']

def test_UsageAPI(test_client):
    response = test_client.get(
        '/api/usage/1'
    )
    response_data = response.get_json()
    assert 'id' in response_data
    
def test_SubscriptionUsageAPI(test_client):
    response = test_client.get(
        '/api/subscriptions/usage/1'
    )
    response_data = response.get_json()
    assert 'id' in response_data
    assert response_data['isOverflow'] is True
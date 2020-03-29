"""Subscription resource for handling any subscription requests"""
from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource

from src.models.subscriptions import Subscription
from src.models.utils import get_object_or_404
from src.schemas.subscriptions import SubscriptionSchema, SubscriptionUsageSchema


class SubscriptionAPI(Resource):
    """Resource/routes for subscription endpoints"""

    def get(self, sid):
        """External facing subscription endpoint GET

        Gets an existing Subscription object by id

        Args:
            sid (int): id of subscription object

        Returns:
            json: serialized subscription object

        """
        subscription = get_object_or_404(Subscription, sid)
        result = SubscriptionSchema().dump(subscription)
        return jsonify(result.data)


class SubscriptionListAPI(Resource):
    """Resource/routes for subscriptions endpoints"""

    @use_kwargs(SubscriptionSchema(partial=True), locations=("query",))
    def get(self, **kwargs):
        """External facing subscription list endpoint GET

        Gets a list of Subscription object with given args

        Args:
            kwargs (dict): filters to apply to query Subscriptions

        Returns:
            json: serialized list of Subscription objects

        """
        subscriptions = Subscription.get_subscriptions(**kwargs)
        result = SubscriptionSchema().dump(subscriptions, many=True)
        return jsonify(result.data)


class SubscriptionUsageAPI(Resource):
    """Resource/routes for Subscription Usage endpoints"""

    def get(self, sid):
        """External facing Subscription Usage endpoint GET
        Gets an existing Subscription Usage object by id

        Args:
            sid (int): id of Subscription object

        Returns:
            json: serialized Subscription Usage object with Data Usage

        """
        subscription = get_object_or_404(Subscription, sid)
        result = SubscriptionUsageSchema().dump(subscription)
        return jsonify(result.data)
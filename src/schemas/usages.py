"""Subscription schemas to assist with sub serialization"""
from marshmallow import fields, Schema, validate
from enum import Enum

from src.schemas.subscriptions import SubscriptionSchema

class UsageSchema(Schema):
    """Schema class to handle serialization of subscription data"""
    id = fields.Integer()
    mb_used = fields.Float()
    subscription_id = fields.Integer()
    from_date =  fields.DateTime()
    to_date =  fields.DateTime()
    subscription = fields.Nested(SubscriptionSchema, dump_only=True)
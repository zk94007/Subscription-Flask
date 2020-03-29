"""Subscription schemas to assist with sub serialization"""
from marshmallow import fields, Schema, validate

from src.schemas.service_codes import PlanSchema


class SubscriptionSchema(Schema):
    """Schema class to handle serialization of subscription data"""
    id = fields.Integer()
    phone_number = fields.String()

    status = fields.String()
    status_effective_date = fields.DateTime()

    plan_id = fields.String()
    plan = fields.Nested(PlanSchema, dump_only=True)
    service_codes = fields.Method("get_service_codes")

    def get_service_codes(self, obj):
        """field get method to return service code names"""
        return [code.name for code in obj.service_codes]


class SubscriptionUsageSchema(Schema):
    """Schema class to handle serialization of subscription data"""
    id = fields.Integer()
    phone_number = fields.String()

    status = fields.String()
    status_effective_date = fields.DateTime()

    plan_id = fields.String()
    plan = fields.Nested(PlanSchema, dump_only=True)

    service_codes = fields.Method("get_service_codes")
    gb_used = fields.Method("get_gb_used")
    isOverflow = fields.Method("get_is_overflow")

    def get_service_codes(self, obj):
        """field get method to return service code names"""
        return [code.name for code in obj.service_codes]
    
    def get_gb_used(self, obj):
        return obj.sum_usage()

    def get_is_overflow(self, obj):
        return obj.check_overflow()
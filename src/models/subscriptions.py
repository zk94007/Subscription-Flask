"""Subscription related models and database functionality"""
from datetime import datetime
from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import func

from src.models.base import db
from src.models.service_codes import ServiceCode, subscriptions_service_codes
from src.models.utils import get_object_or_404

class SubscriptionStatus(Enum):
    """Enum representing possible subscription statuses"""
    new = "new"
    active = "active"
    suspended = "suspended"
    expired = "expired"


class Subscription(db.Model):
    """Model class to represent ATT subscriptions"""

    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(10))
    status = db.Column(ENUM(SubscriptionStatus), default=SubscriptionStatus.new)

    plan_id = db.Column(db.String(30), db.ForeignKey("plans.id"), nullable=False)
    plan = db.relationship("Plan", foreign_keys=[plan_id], lazy="select")
    service_codes = db.relationship(
        "ServiceCode", secondary="subscriptions_service_codes",
        primaryjoin="Subscription.id==subscriptions_service_codes.c.subscription_id",
        secondaryjoin="ServiceCode.id==subscriptions_service_codes.c.service_code_id",
        back_populates="subscriptions", cascade="all,delete", lazy="subquery"
    )

    data_usages = db.relationship("DataUsage", back_populates="subscription")

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.status}), "
            f"phone_number: {self.phone_number or '[no phone number]'}, ",
            f"plan: {self.plan_id}>"
        )


    @classmethod
    def get_subscriptions(cls, **kwargs):
        """Gets a list of Subscription objects using given kwargs

        Generates query filters from kwargs param using base class method

        Args:
            kwargs: key value pairs to apply as filters

        Returns:
            list: objects returned from query result

        """
        return cls.query.filter(**kwargs).all()

    def block_subscription(self):
        """ Add Data Block service code to this subscription"""
        self.service_codes.append(get_object_or_404(ServiceCode, 1))
        db.session.commit()

    def unblock_subscription(self):
        """ Remove Data Block service code from this subscription"""
        self.service_codes.remove(get_object_or_404(ServiceCode, 1))
        db.session.commit()

    def sum_usage(self):
        """Return data usage in gigabytes for this subscription"""

        if self.status == "SubscriptionStatus.new":
            return 0
        from src.models.usages import DataUsage
        return DataUsage.query \
            .with_entities(func.sum(DataUsage.mb_used) / 1024) \
            .filter(DataUsage.subscription_id == self.id) \
            .scalar()

    def check_overflow(self):
        """Return if the data usage of the subscription is overflow"""

        gb_used = self.sum_usage()
        if self.plan_id != "3" and self.plan.mb_available/1024 < float(0 if gb_used is None else gb_used):
            return True
        return False

    def is_blocked(self):
        """Return if subscription include data block service code"""

        for service_code in self.service_codes:
            if service_code.id == 1:
                return True
        return False
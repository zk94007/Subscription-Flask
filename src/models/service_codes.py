"""Plans and Service related models and database functionality"""
from flask import current_app
from sqlalchemy import and_, or_
from sqlalchemy.dialects.postgresql import ARRAY
from src.models.base import db

# Join table for Subscription and ServiceCode
subscriptions_service_codes = db.Table(
    "subscriptions_service_codes", db.Model.metadata,
    db.Column("subscription_id", db.Integer,
              db.ForeignKey("subscriptions.id"), primary_key=True),
    db.Column("service_code_id", db.Integer,
              db.ForeignKey("service_codes.id"), primary_key=True)
)


class Plan(db.Model):
    """Model class to represent mobile service plans"""
    __tablename__ = "plans"
    id = db.Column(db.String(30), primary_key=True)
    description = db.Column(db.String(200))
    # amount of data available for a given billing cycle
    mb_available = db.Column(db.BigInteger)
    is_unlimited = db.Column(db.Boolean)

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.description})>"
        )


class ServiceCode(db.Model):
    """Model class to represent service codes"""

    __tablename__ = "service_codes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

    subscriptions = db.relationship(
        "Subscription", secondary=subscriptions_service_codes,
        primaryjoin="ServiceCode.id==subscriptions_service_codes.c.service_code_id",
        secondaryjoin="Subscription.id==subscriptions_service_codes.c.subscription_id",
        back_populates="service_codes", cascade="all,delete"
    )

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id}, "
            f"{self.name}: ({self.description})>"
        )

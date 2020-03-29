# pylint: disable=unused-argument
"""Version related models and database functionality"""
from src.models.base import db
from src.models.service_codes import ServiceCode
from src.models.subscriptions import Subscription


class SubscriptionServiceChange(db.Model):
    """Model class to keep track of exact datetime when Subscription
    service codes were changed (added/removed).
    """
    __tablename__ = "subscription_service_changes"

    change_id = db.Column("id", db.Integer, primary_key=True)
    service_code_id = db.Column(
        db.Integer,
        db.ForeignKey("service_codes.id"),
        nullable=False)
    subscription_id = db.Column(
        db.Integer,
        db.ForeignKey("subscriptions.id"),
        nullable=False)
    change_date = db.Column(
        db.TIMESTAMP(timezone=True),
        server_default=db.func.now())
    event_type = db.Column(db.Enum("added", "removed"), nullable=False)

    subscription = db.relationship(
        Subscription,
        foreign_keys=[subscription_id],
        lazy="select")
    service_code = db.relationship(
        ServiceCode,
        foreign_keys=[service_code_id],
        lazy="select")

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.change_id} "
            f"service: {self.service_code_id} was {self.event_type.value} at "
            f"{self.change_date}, subscription: {self.subscription_id}>")


@db.event.listens_for(Subscription.service_codes, "append")
def handle_service_code_added(target, value, initiator):
    """Sqlalchemy event listener for handling adding
    ServiceCode to Subscription.
    Alternatively, `MapperEvents.after_insert()` can be used, as more direct way
    to catch "INSERT INTO subscriptions_service_codes ...", but it would require
    writing raw SQL code.

    Args:
        target (obj): Subscription instance.
        value (obj): ServiceCode instance.
        initiator (obj): sqlalchemy.orm.attributes.Event instance.
    """
    if value in target.service_codes:
        # Code already added.
        return
    change = SubscriptionServiceChange(
        subscription=target,
        service_code=value,
        event_type="added"
    )
    # It should get committed together with "subscriptions_service_codes" record.
    db.session.add(change)


@db.event.listens_for(Subscription.service_codes, "remove")
def handle_service_code_removed(target, value, initiator):
    """Sqlalchemy event listener for handling removing
    ServiceCode from Subscription.
    Args:
        target (obj): Subscription instance.
        value (obj): ServiceCode instance.
        initiator (obj): sqlalchemy.orm.attributes.Event instance.
    """
    if value not in target.service_codes:
        # Code already removed.
        return
    change = SubscriptionServiceChange(
        subscription=target,
        service_code=value,
        event_type="removed"
    )
    # It should get committed together with "subscriptions_service_codes" record.
    db.session.add(change)


@db.event.listens_for(Subscription.service_codes, "bulk_replace")
def handle_service_code_bulk_replace(target, values, initiator):
    """Sqlalchemy event listener for handling removing
    ServiceCode from Subscription.
    Args:
        target (obj): Subscription instance.
        values (list): ServiceCode instances.
        initiator (obj): sqlalchemy.orm.attributes.Event instance.
    """
    changes = []
    for code in target.service_codes:
        if code not in values:
            changes.append(
                SubscriptionServiceChange(
                    subscription=target,
                    service_code=code,
                    event_type="removed"
                )
            )
    # It should get committed together with "subscriptions_service_codes" record.
    db.session.add_all(changes)

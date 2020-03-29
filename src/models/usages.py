"""Usage related models and database functionality"""
from decimal import Decimal
from src.models.base import db
from src.models.cycles import BillingCycle
from src.models.subscriptions import Subscription
from src.models.utils import get_object_or_404

from sqlalchemy.sql import label
from src.tasks.usages import check_datausage_after_datablock

class DataUsage(db.Model):
    """Model class to represent data usage record

    Note:
        A daily usage record is created for a subscription each day
        it is active, beginning at midnight UTC timezone.

    """
    __tablename__ = "data_usages"

    id = db.Column(db.Integer, primary_key=True)
    mb_used = db.Column(db.Float, default=0.0)
    from_date = db.Column(db.TIMESTAMP(timezone=True))
    to_date = db.Column(db.TIMESTAMP(timezone=True))

    subscription_id = db.Column(
        db.Integer, db.ForeignKey("subscriptions.id"), nullable=False
    )
    subscription = db.relationship("Subscription", foreign_keys=[subscription_id], back_populates="data_usages", lazy="select")

    # def __init__(self, mb_used, from_date, to_date, subscription_id):
    #     self.mb_used = mb_used
    #     self.from_date = from_date
    #     self.to_date = to_date
    #     self.subscription_id = subscription_id

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.subscription_id}) "
            f"{self.mb_used} MB {self.from_date} - {self.to_date}>"
        )


@db.event.listens_for(DataUsage, "after_insert")
def handle_datausage_inserted(mapper, connection, target):
    """Sqlalchemy event listener for handling inserting new raw into datausage.
        This will check if the subscription is overflow and check data block service code.

    Args:
        mapper (obj): DataUsage
        connection(obj):  the Connection being used to emit this statement
        target (obj): DataUsage instance.
    """
    check_datausage_after_datablock.delay(target.subscription_id)
    
    

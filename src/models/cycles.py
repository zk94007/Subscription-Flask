"""Cycle related models and database functionality"""
from datetime import datetime

from src.models.base import db


class BillingCycle(db.Model):
    """Model class to represent billing cycle dates

    NOTE: this is probably temporary....
    """

    __tablename__ = "billing_cycles"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.TIMESTAMP(timezone=True))
    end_date = db.Column(db.TIMESTAMP(timezone=True))

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id}, "
            f"start_date: {self.start_date}, end_date: {self.end_date}>"
        )

    @classmethod
    def get_current_cycle(cls, date=None):
        """Helper method to get current billing cycle of given date

        Args:
            date (date): date to get billing cycle for

        Returns:
            object: billing cycle object, if any

        """
        if not date:
            date = datetime.now()
        return cls.query.filter(
            cls.start_date <= date, cls.end_date > date).first()

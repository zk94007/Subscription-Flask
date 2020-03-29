"""Main Flask application entrypoint

Example::
    $ python att.py

"""
import config
from src import create_app
from src.models.base import db

app = create_app(config.DevelopmentConfig)

@app.shell_context_processor
def make_shell_context():
    """Adds imports to default shell context for easier use"""
    from src.models.cycles import BillingCycle
    from src.models.service_codes import Plan, ServiceCode
    from src.models.subscriptions import Subscription
    from src.models.usages import DataUsage

    return {
        "BillingCycle": BillingCycle,
        "db": db,
        "Plan": Plan,
        "ServiceCode": ServiceCode,
        "Subscription": Subscription,
        "DataUsage": DataUsage,
    }




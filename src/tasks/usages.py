from src import celery
from src.models.base import db
from src.models.subscriptions import Subscription
from src.models.utils import get_object_or_404

@celery.task(name='usage_celery.check_subscriptions_overflow')
def check_subscriptions_overflow():
    """checks if subscriptions are over their allotted data usage for the current billing cycle. 
        If they are, they should have the "Data Block" service code applied to the subscription.
        It will check all subscriptions every 30 seconds.

    Args:

    Returns:
        result of this monitoring task
    """
    apply_block_list = []
    apply_unblock_list = []
    for subscription in Subscription.query.all():
        if subscription.check_overflow() is True and subscription.plan_id != 3:
           if subscription.is_blocked() is False:
                subscription.block_subscription()
                apply_block_list.append(subscription.id)
        else:
            if subscription.is_blocked() is True:
                subscription.unblock_subscription()
                apply_unblock_list.append(subscription.id)
    if len(apply_block_list) == 0 and len(apply_unblock_list) == 0:
        return "Nothing changed!"
    return ("Blocked following subscriptions with IDs: {}".format(apply_block_list) if len(apply_block_list) != 0 else "") + \
           ("UnBlocked following subscriptions with IDs: {}".format(apply_unblock_list) if len(apply_unblock_list) != 0 else "")

@celery.task(name='usage_celery.check_datausage_after_datablock')
def check_datausage_after_datablock(sid):
    """"checks if subscriptions have generated data usage 
       since they have had the "Data Block" service code applied.
       It checks every time DataUsage row is added to database

    Args:
        sid: ID of subscription

    Returns:
        result of this monitoring task
    """
    subscription = get_object_or_404(Subscription, sid)
    if subscription.check_overflow() is True and subscription.plan_id != 3:
        if subscription.is_blocked() is True:
            return "Generated Data Usage for blocked subscription!"
        subscription.block_subscription()
        return f"Added Data Block to Subscription with ID of {sid}"
    return "Not Overflow"

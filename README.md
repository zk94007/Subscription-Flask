## Requirements
* Python 3.5+
* SQLite

## Starting the server
Everything is set up, including the database and some seed data. All you need to do is create the virtual environment with the dependencies and then execute `flask run`. Voila!

## Context
- Subscriptions run on billing cycles. For each billing cycle, a subscription will start on one plan, but can be upgraded or downgraded during the billing cycle. For example, a subscription might start on a 1GB plan and then upgrade to a 3GB plan mid-cycle after they've reached their available data limit. When they upgrade to the 3GB plan, they have an additional 2GB of data available to use before the end of the billing cycle.
- We have an `ATTPlanVersion` table to keep track of the plan a subscription is on at any given time. There is a `start_effective_date` and `end_effective_date` in this table. For the example above of a subscription starting on 1GB plan and upgrading to a 3GB plan mid-cycle, the rows in the table would look something like this:
```
# 1GB plan_id = 1
# 3GB plan_id = 2
{
    'id': 1,
    'subscription_id': '1',
    'plan_id': '1',
    'start_effective_date': '2019-11-01T00:00:00+00:00',
    'end_effective_date': '2019-12-01T00:00:00+00:00'
},
{
    'id': 2,
    'subscription_id': '1',
    'plan_id': '2',
    'start_effective_date': '2019-11-01T00:00:00+00:00',
    'end_effective_date': '2019-12-01T00:00:00+00:00'
}
```
- You might be wondering why we even bother with effective dates instead of just referencing the billing cycle. The problem comes when subscriptions are activated or expired mid-cycle. For subscriptions activated mid-cycle, the plan is effective starting when the subscription was activated. So the `start_effective_date` would be the subscription `activation_date`. Similarly, for expired subscriptions, the plan is only effective up as long as the subscription was `active` or `suspended`. So the `end_effective_date` would be the subscription `expiry_date`.
- The metric we are concerned about for this challenge is the available data. We need to calculate how much data we have available for each subscription for a billing cycle. For plans with effective dates that start or end mid-cycle, the data will be prorated based on how many days it was active during the cycle. For example, if a subscription is activated on a 3GB plan exactly midway through the cycle (ie. November 15th), then the available data for the November billing cycle will be 1.5GB.

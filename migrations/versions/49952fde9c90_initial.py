"""initial migration

Revision ID: 49952fde9c90
Revises:
Create Date: 2019-09-28 13:11:26.043849

"""
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '49952fde9c90'
down_revision = None
branch_labels = None
depends_on = None


def populate_billing_cycles(billing_cycles):
    op.bulk_insert(billing_cycles, [
        {
            'id': 1,
            'start_date': datetime(2019, 8, 1, tzinfo=timezone.utc),
            'end_date': datetime(2019, 9, 1, tzinfo=timezone.utc),
        },
        {
            'id': 2,
            'start_date': datetime(2019, 9, 1, tzinfo=timezone.utc),
            'end_date': datetime(2019, 10, 1, tzinfo=timezone.utc),
        },
        {
            'id': 3,
            'start_date': datetime(2019, 10, 1, tzinfo=timezone.utc),
            'end_date': datetime(2019, 11, 1, tzinfo=timezone.utc),
        }
    ])


def populate_plans(plans):
    op.bulk_insert(plans, [
        {
            'id': 1,
            'description': '1GB Monthly Data Plan',
            'mb_available': '1024',
            'is_unlimited': False
        },
        {
            'id': 2,
            'description': '5GB Monthly Data Plan',
            'mb_available': '5120',
            'is_unlimited': False
        },
        {
            'id': 3,
            'description': 'Unlimited Monthly Data Plan',
            'mb_available': '10240',
            'is_unlimited': True
        }
    ])


def populate_service_codes(service_codes):
    op.bulk_insert(service_codes, [
        {
            'id': 1,
            'name': 'Data Block',
            'description': 'Blocks all data',
        },
        {
            'id': 2,
            'name': 'International Calling',
            'description': 'Enables international calling',
        }
    ])


def populate_subscriptions(subscriptions):
    op.bulk_insert(subscriptions, [
        {
            'id': 1,
            'phone_number': '1111111111',
            'status': 'active',
            'plan_id': 3
        },
        {
            'id': 2,
            'phone_number': '2222222222',
            'status': 'suspended',
            'plan_id': 1
        },
        {
            'id': 3,
            'phone_number': '3333333333',
            'status': 'new',
            'plan_id': 2
        },
        {
            'id': 4,
            'phone_number': '4444444444',
            'status': 'expired',
            'plan_id': 2
        },
        {
            'id': 5,
            'phone_number': '5555555555',
            'status': 'active',
            'plan_id': 3
        },
        {
            'id': 6,
            'phone_number': '7777777777',
            'status': 'suspended',
            'plan_id': 1
        },
        {
            'id': 7,
            'phone_number': '8888888888',
            'status': 'active',
            'plan_id': 2
        }
    ])


def populate_data_usages(data_usages):
    op.bulk_insert(data_usages, [
        {
            'id': 1,
            'mb_used': 121.522,
            'from_date': datetime(2019, 9, 20, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 20, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 1
        },
        {
            'id': 2,
            'mb_used': 519.984,
            'from_date': datetime(2019, 9, 21, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 21, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 1
        },
        {
            'id': 3,
            'mb_used': 22.362,
            'from_date': datetime(2019, 9, 24, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 24, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 1
        },
        {
            'id': 4,
            'mb_used': 450.759,
            'from_date': datetime(2019, 9, 3, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 3, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 2
        },
        {
            'id': 5,
            'mb_used': 560.811,
            'from_date': datetime(2019, 9, 10, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 10, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 4
        },
        {
            'id': 6,
            'mb_used': 220.336,
            'from_date': datetime(2019, 9, 20, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 20, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 5
        },
        {
            'id': 7,
            'mb_used': 51.553,
            'from_date': datetime(2019, 9, 20, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 20, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 5
        },
        {
            'id': 8,
            'mb_used': 470.288,
            'from_date': datetime(2019, 9, 9, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 9, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 6
        },
        {
            'id': 9,
            'mb_used': 221.02,
            'from_date': datetime(2019, 9, 20, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 20, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 7
        },
        {
            'id': 10,
            'mb_used': 1896.663,
            'from_date': datetime(2019, 9, 12, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 12, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 7
        },
        {
            'id': 11,
            'mb_used': 2216.993,
            'from_date': datetime(2019, 9, 13, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 13, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 7
        },
        {
            'id': 12,
            'mb_used': 1151.444,
            'from_date': datetime(2019, 9, 14, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 14, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 7
        },
        {
            'id': 13,
            'mb_used': 829.334,
            'from_date': datetime(2019, 9, 19, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 19, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 2
        },
        {
            'id': 14,
            'mb_used': 10299.012,
            'from_date': datetime(2019, 9, 2, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 2, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 1
        },
        {
            'id': 15,
            'mb_used': 158.346,
            'from_date': datetime(2019, 9, 21, tzinfo=timezone.utc),
            'to_date': datetime(2019, 9, 21, 23, 59, 59, 999999, tzinfo=timezone.utc),
            'subscription_id': 2
        }
    ])


def populate_subscriptions_service_codes(subscriptions_service_codes):
    op.bulk_insert(subscriptions_service_codes, [
        {
            'service_code_id': 1,
            'subscription_id': 2
        }
    ])


def populate_subscription_service_changes(subscription_service_changes):
    op.bulk_insert(subscription_service_changes, [
        {
            'id': 1,
            'service_code_id': 1,
            'subscription_id': 2,
            'change_date': datetime(2019, 9, 20, tzinfo=timezone.utc),
            'event_type': 'added'
        },
        {
            'id': 2,
            'service_code_id': 1,
            'subscription_id': 4,
            'change_date': datetime(2019, 8, 25, tzinfo=timezone.utc),
            'event_type': 'removed'
        }
    ])


def upgrade():
    billing_cycles = op.create_table('billing_cycles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('end_date', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    populate_billing_cycles(billing_cycles)

    plans = op.create_table('plans',
        sa.Column('id', sa.String(length=30), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.Column('mb_available', sa.BigInteger(), nullable=True),
        sa.Column('is_unlimited', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    populate_plans(plans)

    service_codes = op.create_table('service_codes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    populate_service_codes(service_codes)

    subscriptions = op.create_table('subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('phone_number', sa.String(length=10), nullable=True),
        sa.Column('status', sa.Enum('new', 'active', 'suspended', 'expired'), nullable=True),
        sa.Column('plan_id', sa.String(length=30), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    populate_subscriptions(subscriptions)

    data_usages = op.create_table('data_usages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('mb_used', sa.Float(), nullable=True),
        sa.Column('from_date', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('to_date', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('subscription_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscriptions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    populate_data_usages(data_usages)

    subscriptions_service_codes = op.create_table('subscriptions_service_codes',
        sa.Column('subscription_id', sa.Integer(), nullable=False),
        sa.Column('service_code_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['service_code_id'], ['service_codes.id'], ),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscriptions.id'], ),
        sa.PrimaryKeyConstraint('subscription_id', 'service_code_id')
    )
    populate_subscriptions_service_codes(subscriptions_service_codes)

    subscription_service_changes = op.create_table('subscription_service_changes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('service_code_id', sa.Integer(), nullable=False),
        sa.Column('subscription_id', sa.Integer(), nullable=False),
        sa.Column('change_date', sa.TIMESTAMP(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('event_type', sa.Enum('added', 'removed'), nullable=False),
        sa.ForeignKeyConstraint(['service_code_id'], ['service_codes.id'], ),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscriptions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    populate_subscription_service_changes(subscription_service_changes)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscription_service_changes')
    op.drop_table('subscriptions_service_codes')
    op.drop_table('data_usages')
    op.drop_table('subscriptions')
    op.drop_table('service_codes')
    op.drop_table('plans')
    op.drop_table('billing_cycles')
    # ### end Alembic commands ###

"""empty message

Revision ID: 15669934845d
Revises: e13111a8d40d
Create Date: 2025-04-30 22:33:18.294892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15669934845d'
down_revision = 'e13111a8d40d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('client_id', sa.Integer(), nullable=True))
        batch_op.alter_column(
            'booking_status',
            existing_type=sa.VARCHAR(length=50),
            type_=sa.Enum('pending', 'confirmed', 'cancelled', 'completed', name='bookingstatus'),
            nullable=False
        )
        batch_op.create_unique_constraint(
            'uq_artist_booking_slot', ['artist_id', 'booking_date', 'booking_time']
        )
        batch_op.create_foreign_key(None, 'clients', ['client_id'], ['client_id'])

    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.drop_constraint('uq_artist_booking_slot', type_='unique')
        batch_op.alter_column(
            'booking_status',
            existing_type=sa.Enum('pending', 'confirmed', 'cancelled', 'completed', name='bookingstatus'),
            type_=sa.VARCHAR(length=50),
            nullable=True
        )
        batch_op.drop_column('client_id')

    # ### end Alembic commands ###

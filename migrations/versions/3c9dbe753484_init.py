"""init

Revision ID: 3c9dbe753484
Revises: 
Create Date: 2023-07-31 22:26:17.772372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c9dbe753484'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('users',
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('members',
    sa.Column('user_uuid', sa.UUID(), nullable=False),
    sa.Column('event_uuid', sa.UUID(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['event_uuid'], ['events.uuid'], ),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_members_event_uuid'), 'members', ['event_uuid'], unique=False)
    op.create_index(op.f('ix_members_user_uuid'), 'members', ['user_uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_members_user_uuid'), table_name='members')
    op.drop_index(op.f('ix_members_event_uuid'), table_name='members')
    op.drop_table('members')
    op.drop_table('users')
    op.drop_table('events')
    # ### end Alembic commands ###
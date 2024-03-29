"""many to many entre grupos e permissao

Revision ID: c69969636b69
Revises: e90fc428a175
Create Date: 2024-01-07 18:10:58.973552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c69969636b69'
down_revision = 'e90fc428a175'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permissions_groups',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('action', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('action', name='uq_action')
                    )
    op.create_index(op.f('ix_permissions_groups_action'),
                    'permissions_groups', ['action'], unique=False)
    op.create_index(op.f('ix_permissions_groups_id'),
                    'permissions_groups', ['id'], unique=False)
    op.create_table('permission_association',
                    sa.Column('permission_id', sa.Integer(), nullable=True),
                    sa.Column('permission_group_id',
                              sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['permission_group_id'], [
                        'permissions_groups.id'], ),
                    sa.ForeignKeyConstraint(
                        ['permission_id'], ['permissions.id'], )
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('permission_association')
    op.drop_index(op.f('ix_permissions_groups_id'),
                  table_name='permissions_groups')
    op.drop_index(op.f('ix_permissions_groups_action'),
                  table_name='permissions_groups')
    op.drop_table('permissions_groups')
    # ### end Alembic commands ###

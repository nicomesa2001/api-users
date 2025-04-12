"""remove_username_add_password

Revision ID: remove_username_add_password
Revises: 
Create Date: 2025-04-12 00:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'remove_username_add_password'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop username column if it exists
    try:
        op.drop_column('users', 'username')
    except:
        pass
    
    # Add hashed_password column if it doesn't exist
    try:
        op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
    except:
        pass


def downgrade():
    # Add username column back
    try:
        op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    except:
        pass
    
    # Remove hashed_password column
    try:
        op.drop_column('users', 'hashed_password')
    except:
        pass

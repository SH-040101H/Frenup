"""Add item tracking models

Revision ID: 001_item_tracking
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_item_tracking'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create item types enum
    item_type_enum = sa.Enum('ERC', 'PAD', 'LINER', 'SLEEPER', 'OTHER', name='itemtype')
    item_type_enum.create(op.get_bind())
    
    # Create inspection stage enum
    inspection_stage_enum = sa.Enum('MFG', 'SUPPLY', 'INSTALL', 'PERIODIC', 'FAILURE', name='inspectionstage')
    inspection_stage_enum.create(op.get_bind())
    
    # Create inspection outcome enum
    inspection_outcome_enum = sa.Enum('PASS', 'WARN', 'FAIL', name='inspectionoutcome')
    inspection_outcome_enum.create(op.get_bind())
    
    # Create inspection source enum
    inspection_source_enum = sa.Enum('UDM', 'TMS', 'MANUAL', name='inspectionsource')
    inspection_source_enum.create(op.get_bind())
    
    # Create exception severity enum
    exception_severity_enum = sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='exceptionseverity')
    exception_severity_enum.create(op.get_bind())
    
    # Create exception status enum
    exception_status_enum = sa.Enum('OPEN', 'ACK', 'CLOSED', name='exceptionstatus')
    exception_status_enum.create(op.get_bind())

    # Create items table
    op.create_table('items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('short_id', sa.String(length=20), nullable=False),
        sa.Column('type', item_type_enum, nullable=False),
        sa.Column('vendor_id', sa.String(length=50), nullable=False),
        sa.Column('plant_code', sa.String(length=20), nullable=False),
        sa.Column('lot', sa.String(length=50), nullable=False),
        sa.Column('mfg_date', sa.Date(), nullable=False),
        sa.Column('serial', sa.String(length=100), nullable=False),
        sa.Column('spec_rev', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for items table
    op.create_index('ix_items_short_id', 'items', ['short_id'], unique=True)
    op.create_index('ix_items_type', 'items', ['type'], unique=False)
    op.create_index('ix_items_vendor_id', 'items', ['vendor_id'], unique=False)
    op.create_index('ix_items_lot', 'items', ['lot'], unique=False)
    op.create_index('ix_items_serial', 'items', ['serial'], unique=False)

    # Create warranties table
    op.create_table('warranties',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('terms', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index for warranties
    op.create_index('ix_warranties_item_id', 'warranties', ['item_id'], unique=False)

    # Create inspections table
    op.create_table('inspections',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('stage', inspection_stage_enum, nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('outcome', inspection_outcome_enum, nullable=False),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('source', inspection_source_enum, nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for inspections
    op.create_index('ix_inspections_item_id', 'inspections', ['item_id'], unique=False)
    op.create_index('ix_inspections_stage', 'inspections', ['stage'], unique=False)
    op.create_index('ix_inspections_date', 'inspections', ['date'], unique=False)
    op.create_index('ix_inspections_outcome', 'inspections', ['outcome'], unique=False)
    op.create_index('ix_inspections_item_date', 'inspections', ['item_id', 'date'], unique=False)

    # Create scan_events table
    op.create_table('scan_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('actor_id', sa.String(length=100), nullable=False),
        sa.Column('scanned_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('lat', sa.Float(), nullable=True),
        sa.Column('lng', sa.Float(), nullable=True),
        sa.Column('photo_url', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for scan_events
    op.create_index('ix_scan_events_item_id', 'scan_events', ['item_id'], unique=False)
    op.create_index('ix_scan_events_scanned_at', 'scan_events', ['scanned_at'], unique=False)

    # Create item_exceptions table
    op.create_table('item_exceptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('severity', exception_severity_enum, nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', exception_status_enum, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for item_exceptions
    op.create_index('ix_item_exceptions_item_id', 'item_exceptions', ['item_id'], unique=False)
    op.create_index('ix_item_exceptions_code', 'item_exceptions', ['code'], unique=False)
    op.create_index('ix_item_exceptions_severity', 'item_exceptions', ['severity'], unique=False)
    op.create_index('ix_item_exceptions_status', 'item_exceptions', ['status'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('item_exceptions')
    op.drop_table('scan_events')
    op.drop_table('inspections')
    op.drop_table('warranties')
    op.drop_table('items')
    
    # Drop enums
    sa.Enum(name='exceptionstatus').drop(op.get_bind())
    sa.Enum(name='exceptionseverity').drop(op.get_bind())
    sa.Enum(name='inspectionsource').drop(op.get_bind())
    sa.Enum(name='inspectionoutcome').drop(op.get_bind())
    sa.Enum(name='inspectionstage').drop(op.get_bind())
    sa.Enum(name='itemtype').drop(op.get_bind())
# Database Package

This package contains SQLModel database models, Alembic migrations, and CRUD operations for the IR FitMark application.

## Structure

- `src/db/models.py` - Core SQLModel models for fitness tracking
- `src/db/item_models.py` - SQLModel models for item tracking
- `src/db/crud.py` - CRUD operations for core models
- `src/db/item_crud.py` - CRUD operations for item tracking models
- `src/db/database.py` - Database connection and session management
- `alembic/` - Database migration files

## Models

### Core Models (Fitness Tracking)
- **User** - User accounts with roles (student, instructor, admin)
- **FitnessAssessment** - AI-powered fitness assessments
- **Report** - Generated fitness reports
- **QRCode** - QR codes for assessment access
- **SystemLog** - Application logs
- **Exception** - Error tracking
- **FileUpload** - File upload tracking
- **WorkerJob** - Background job tracking

### Item Tracking Models
- **Item** - Physical items with unique identifiers
- **Warranty** - Item warranty information
- **Inspection** - Item inspection records
- **ScanEvent** - Item scan tracking with location data
- **Exception** - Item-specific exceptions and issues

## Database Setup

### Prerequisites

1. PostgreSQL 16+ running
2. Python environment with dependencies installed
3. Environment variables configured

### Environment Variables

```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=ir_fitmark
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

### Running Migrations

#### First Time Setup

1. Navigate to the db package directory:
```bash
cd packages/db
```

2. Initialize Alembic (if not already done):
```bash
alembic revision --autogenerate -m "Initial migration"
```

3. Run the migration:
```bash
alembic upgrade head
```

#### Creating New Migrations

When you modify models, create a new migration:

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Apply the migration
alembic upgrade head
```

#### Manual Migration Commands

```bash
# Check current migration status
alembic current

# View migration history
alembic history

# Upgrade to specific revision
alembic upgrade <revision_id>

# Downgrade to previous revision
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>
```

## Item Tracking Features

### Item Management
- Unique short IDs for public URLs
- Vendor and manufacturing information
- Type classification (ERC, PAD, LINER, SLEEPER, OTHER)
- Serial number and specification tracking

### Warranty Tracking
- Start and end dates
- Terms and conditions
- Active warranty checking

### Inspection System
- Multiple inspection stages (MFG, SUPPLY, INSTALL, PERIODIC, FAILURE)
- Pass/Warn/Fail outcomes
- Source tracking (UDM, TMS, MANUAL)
- Historical inspection records

### Scan Events
- QR code scanning with timestamps
- Actor tracking (who scanned)
- Optional GPS coordinates
- Photo documentation

### Exception Management
- Severity levels (LOW, MEDIUM, HIGH, CRITICAL)
- Status tracking (OPEN, ACK, CLOSED)
- Exception codes and messages

## Indexes

The following indexes are created for optimal query performance:

### Item Table
- `ix_items_serial` - Serial number lookups
- `ix_items_lot` - Lot number searches
- `ix_items_vendor_id` - Vendor filtering
- `ix_items_short_id` - Public ID lookups (unique)

### Inspection Table
- `ix_inspections_item_date` - Composite index for item + date queries
- `ix_inspections_item_id` - Item filtering
- `ix_inspections_outcome` - Outcome filtering

### Other Indexes
- Foreign key indexes on all relationship columns
- Timestamp indexes for time-based queries
- Status and type enum indexes for filtering

## Usage Examples

### Creating Items

```python
from db import get_async_db, item as crud_item
from pyshared import ItemCreate, ItemType

# Create a new item
item_data = ItemCreate(
    short_id="ABC12345",
    type=ItemType.ERC,
    vendor_id="VND001",
    plant_code="P01",
    lot="LOT123",
    mfg_date=date(2024, 1, 15),
    serial="SER789",
    spec_rev="v1.2"
)

async with get_async_db() as db:
    item = await crud_item.create(db, item_data)
```

### Recording Inspections

```python
from db import inspection as crud_inspection
from pyshared import InspectionCreate, InspectionStage, InspectionOutcome

inspection_data = InspectionCreate(
    item_id=item.id,
    stage=InspectionStage.MFG,
    date=datetime.utcnow(),
    outcome=InspectionOutcome.PASS,
    remarks="All tests passed",
    source=InspectionSource.UDM
)

async with get_async_db() as db:
    inspection = await crud_inspection.create(db, inspection_data)
```

### Querying Items

```python
# Search items by serial number
items = await crud_item.search_items(db, "SER789")

# Get items by vendor and lot
items = await crud_item.get_by_vendor_and_lot(db, "VND001", "LOT123")

# Get item by short ID
item = await crud_item.get_by_short_id(db, "ABC12345")
```

## Development

### Adding New Models

1. Add the model to the appropriate models file
2. Create CRUD operations if needed
3. Generate and run migration
4. Add corresponding Pydantic models to pyshared
5. Update API endpoints

### Testing

```bash
# Run tests (when implemented)
pytest tests/

# Test database connection
python -c "from db import check_db_health_sync; print(check_db_health_sync())"
```

## Production Considerations

### Performance
- Monitor query performance and add indexes as needed
- Consider partitioning large tables by date
- Use connection pooling for high-load scenarios

### Backup
- Regular PostgreSQL backups
- Point-in-time recovery setup
- Test backup restoration procedures

### Monitoring
- Track slow queries
- Monitor connection pool usage
- Set up alerting for failed migrations
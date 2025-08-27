"""Utility functions for item tracking."""

import secrets
import string
from typing import Optional
from datetime import date, datetime


def generate_short_id(length: int = 8) -> str:
    """Generate a short alphanumeric ID for items.
    
    Args:
        length: Length of the ID to generate (default 8)
        
    Returns:
        Short alphanumeric ID string
    """
    # Use uppercase letters and numbers, excluding similar looking characters
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def format_item_id(item_type: str, vendor_id: str, serial: str) -> str:
    """Format a human-readable item identifier.
    
    Args:
        item_type: Type of item (ERC, PAD, etc.)
        vendor_id: Vendor identifier
        serial: Serial number
        
    Returns:
        Formatted item identifier like "ERC-VND001-SER123"
    """
    return f"{item_type}-{vendor_id}-{serial}"


def validate_serial_format(serial: str, item_type: str) -> bool:
    """Validate serial number format based on item type.
    
    Args:
        serial: Serial number to validate
        item_type: Type of item
        
    Returns:
        True if valid, False otherwise
    """
    if not serial or len(serial) < 3:
        return False
    
    # Basic validation - can be extended per item type
    if item_type in ["ERC", "PAD"]:
        # Example: ERC and PAD serials should be alphanumeric, 6-20 chars
        return serial.isalnum() and 6 <= len(serial) <= 20
    elif item_type in ["LINER", "SLEEPER"]:
        # Example: LINER and SLEEPER serials allow dashes, 8-25 chars
        allowed_chars = set(string.ascii_letters + string.digits + '-')
        return (all(c in allowed_chars for c in serial) and 
                8 <= len(serial) <= 25)
    else:
        # Generic validation for OTHER types
        return len(serial) <= 100


def calculate_warranty_days_remaining(end_date: date) -> int:
    """Calculate days remaining in warranty.
    
    Args:
        end_date: Warranty end date
        
    Returns:
        Number of days remaining (negative if expired)
    """
    today = date.today()
    return (end_date - today).days


def is_warranty_active(start_date: date, end_date: date, check_date: Optional[date] = None) -> bool:
    """Check if warranty is currently active.
    
    Args:
        start_date: Warranty start date
        end_date: Warranty end date
        check_date: Date to check against (default: today)
        
    Returns:
        True if warranty is active on check_date
    """
    if check_date is None:
        check_date = date.today()
    
    return start_date <= check_date <= end_date


def format_inspection_summary(inspections: list) -> dict:
    """Format inspection data into a summary.
    
    Args:
        inspections: List of inspection records
        
    Returns:
        Dictionary with inspection summary statistics
    """
    if not inspections:
        return {
            "total": 0,
            "passed": 0,
            "warned": 0,
            "failed": 0,
            "latest_date": None,
            "by_stage": {}
        }
    
    summary = {
        "total": len(inspections),
        "passed": 0,
        "warned": 0,
        "failed": 0,
        "by_stage": {}
    }
    
    latest_date = None
    
    for inspection in inspections:
        # Count by outcome
        outcome = getattr(inspection, 'outcome', None)
        if outcome == "PASS":
            summary["passed"] += 1
        elif outcome == "WARN":
            summary["warned"] += 1
        elif outcome == "FAIL":
            summary["failed"] += 1
        
        # Count by stage
        stage = getattr(inspection, 'stage', None)
        if stage:
            summary["by_stage"][stage] = summary["by_stage"].get(stage, 0) + 1
        
        # Track latest date
        inspection_date = getattr(inspection, 'date', None)
        if inspection_date and (latest_date is None or inspection_date > latest_date):
            latest_date = inspection_date
    
    summary["latest_date"] = latest_date
    return summary


def get_exception_priority_score(severity: str, status: str, created_at: datetime) -> int:
    """Calculate priority score for exceptions.
    
    Args:
        severity: Exception severity (LOW, MEDIUM, HIGH, CRITICAL)
        status: Exception status (OPEN, ACK, CLOSED)
        created_at: When the exception was created
        
    Returns:
        Priority score (higher = more urgent)
    """
    # Base score by severity
    severity_scores = {
        "CRITICAL": 100,
        "HIGH": 75,
        "MEDIUM": 50,
        "LOW": 25
    }
    
    # Status modifiers
    status_modifiers = {
        "OPEN": 1.0,
        "ACK": 0.7,
        "CLOSED": 0.0
    }
    
    # Age modifier (older issues get higher priority)
    age_days = (datetime.utcnow() - created_at).days
    age_modifier = min(1.5, 1.0 + (age_days * 0.02))  # Up to 50% increase over 25 days
    
    base_score = severity_scores.get(severity, 25)
    status_modifier = status_modifiers.get(status, 1.0)
    
    return int(base_score * status_modifier * age_modifier)


def generate_qr_data(item_short_id: str, action: str = "view") -> str:
    """Generate QR code data for an item.
    
    Args:
        item_short_id: Short ID of the item
        action: Action to perform (view, inspect, scan)
        
    Returns:
        QR code data string
    """
    # Format: ITEM:{short_id}:{action}:{timestamp}
    timestamp = int(datetime.utcnow().timestamp())
    return f"ITEM:{item_short_id}:{action}:{timestamp}"


def parse_qr_data(qr_data: str) -> Optional[dict]:
    """Parse QR code data.
    
    Args:
        qr_data: QR code data string
        
    Returns:
        Dictionary with parsed data or None if invalid
    """
    try:
        parts = qr_data.split(":")
        if len(parts) >= 3 and parts[0] == "ITEM":
            return {
                "type": parts[0],
                "item_short_id": parts[1],
                "action": parts[2],
                "timestamp": int(parts[3]) if len(parts) > 3 else None
            }
    except (ValueError, IndexError):
        pass
    
    return None


def validate_geo_coordinates(lat: Optional[float], lng: Optional[float]) -> bool:
    """Validate geographic coordinates.
    
    Args:
        lat: Latitude
        lng: Longitude
        
    Returns:
        True if coordinates are valid
    """
    if lat is None or lng is None:
        return True  # Optional coordinates are valid
    
    return (-90 <= lat <= 90) and (-180 <= lng <= 180)
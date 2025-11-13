from datetime import date
from typing import Optional

def format_date(d: Optional[date]) -> str:
    return d.isoformat() if d else "N/A"

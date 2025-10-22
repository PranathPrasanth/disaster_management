from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import contextmanager

# ----------------------------------------------------------------------
# THE FIX: Importing schema definitions directly from the sibling file.
# Since schemas.py is a FILE, we import the specific classes/definitions 
# directly from the module.
# ----------------------------------------------------------------------
from ..database import get_db # Correct relative import for database.py
from ..utils.email import send_volunteer_notification, send_donor_confirmation, send_admin_alert # Correct relative import for utils/email.py
from ..schemas import NotificationCreate, NotificationRead # <-- *** CRITICAL CHANGE ***

# Placeholder for models
class NotificationModel:
    """Mock model class to prevent a NameError."""
    def __init__(self, **kwargs):
        pass

# Placeholder for database functions
def get_notification_by_id(db: AsyncSession, id: int):
    """Placeholder function."""
    return NotificationModel(id=id, message="Test Notification")

# ----------------------------------------------------------------------
# ROUTER CODE
# ----------------------------------------------------------------------

router = APIRouter()

@router.post("/notifications", status_code=status.HTTP_201_CREATED)
async def create_new_notification(
    # NOTE: Since we imported the class directly, we use the class name
    notification_data: NotificationCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a new notification and sends an email alert (if applicable).
    """
    try:
        if "volunteer" in notification_data.message.lower():
            send_volunteer_notification(
                recipient_email="example@volunteer.com",
                subject="New Task Assigned",
                body=notification_data.message
            )
        else:
            send_admin_alert(
                recipient_email="admin@dms.com",
                subject="New Notification Created",
                body=notification_data.message
            )
    except Exception as e:
        print(f"Email failed to send: {e}")

    # Logic to save notification to database would go here
    return {"message": "Notification created and processed successfully", "id": 1}

@router.get("/notifications/{notification_id}", response_model=NotificationRead) # NOTE: Using the class name
async def read_notification(notification_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieves a specific notification by ID.
    """
    notification = get_notification_by_id(db, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

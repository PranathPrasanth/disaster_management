from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import contextmanager

# ----------------------------------------------------------------------
# THE FIX: Using '..' to go up one level (from 'routers' to 'app')
# and then down into the sibling directories ('utils', 'schemas', 'database').
# ----------------------------------------------------------------------
from ..database import get_db # Assuming get_db function is in the sibling database module
from ..schemas import notifications as notifications_schema # Assuming schemas/notifications.py exists
from ..utils.email import send_volunteer_notification, send_donor_confirmation, send_admin_alert

# Placeholder for models
class NotificationModel:
    """Mock model class to prevent a NameError."""
    def __init__(self, **kwargs):
        pass

# Placeholder for database functions
def get_notification_by_id(db: AsyncSession, id: int):
    """Placeholder function."""
    return NotificationModel(id=id, message="Test Notification")

def get_all_notifications(db: AsyncSession):
    """Placeholder function."""
    return [NotificationModel(id=1, message="N1"), NotificationModel(id=2, message="N2")]

# ----------------------------------------------------------------------
# ROUTER CODE
# ----------------------------------------------------------------------

router = APIRouter()

@router.post("/notifications", status_code=status.HTTP_201_CREATED)
async def create_new_notification(
    notification_data: notifications_schema.NotificationCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Creates a new notification and sends an email alert (if applicable).
    """
    # Example usage of the fixed import:
    # In a real app, this logic would check the notification type
    # and call the appropriate email function.
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
        # Log the error, but don't stop the main process
        print(f"Email failed to send: {e}")

    # Logic to save notification to database would go here
    return {"message": "Notification created and processed successfully", "id": 1}

@router.get("/notifications/{notification_id}", response_model=notifications_schema.NotificationRead)
async def read_notification(notification_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieves a specific notification by ID.
    """
    notification = get_notification_by_id(db, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

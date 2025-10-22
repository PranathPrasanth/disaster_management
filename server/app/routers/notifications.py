from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.utils.email import send_volunteer_notification, send_donor_confirmation, send_admin_alert

router = APIRouter(prefix="/notifications", tags=["notifications"])

# Request model from frontend
class VolunteerNotificationRequest(BaseModel):
    email: str
    name: str
    disaster_name: str
    location: str

@router.post("/volunteer")
def notify_volunteer(data: VolunteerNotificationRequest, background_tasks: BackgroundTasks):
    send_volunteer_notification(
        background_tasks,
        to_email=data.email,
        name=data.name,
        disaster_name=data.disaster_name,
        location=data.location
    )
    return {"message": "Volunteer notification email triggered"}

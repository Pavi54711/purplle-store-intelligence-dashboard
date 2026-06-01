from pydantic import BaseModel


class Event(BaseModel):
    event_type: str
    visitor_id: str
    camera_id: str
    timestamp: str
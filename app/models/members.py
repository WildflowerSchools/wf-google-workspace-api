from typing import Optional

from pydantic import BaseModel, Field


class Member(BaseModel):
    kind: str = "admin#directory#member"
    email: Optional[str] = None
    role: Optional[str] = None
    etag: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    delivery_settings: Optional[str] = None
    id: Optional[str] = None

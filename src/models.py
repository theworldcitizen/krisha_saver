from typing import Optional, List

from pydantic import BaseModel


class Ad(BaseModel):
    title: Optional[str]
    ad_number: str
    # category: str
    ad_text: Optional[str] = None
    sum: str
    photo: Optional[list] = None
    url: str
    publish_date: str


class Location(BaseModel):
    city: str
    address: str
    region: str


class Author(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[List] = None
    author_type: Optional[str] = None
    url: Optional[str] = None



class Details(BaseModel):
    payment_method: List
    timetable: Optional[str] = None


class Result(BaseModel):
    platform_id = 'krisha'
    ad: Ad
    address: Location
    author: Author
    details: Details

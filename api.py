from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio

# from database import *
from database import workwithbd
import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CourseItem(BaseModel):
    CourseId: Optional[int] = None
    Name: Optional[str] = None
    Description: Optional[str] = None
    Url: Optional[str] = None
    ProfileId: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True

class Courses(BaseModel):
    count: int
    results: List[CourseItem]

    class Config:
        orm_mode = True
        from_attributes = True

class UserItem(BaseModel):
    UserId: Optional[int] = None
    Username: Optional[str] = None
    Password: Optional[str] = None
    Email: Optional[str] = None
    Surname: Optional[str] = None
    Name: Optional[str] = None
    Lastname: Optional[str] = None
    Created_at: Optional[str] = None
    CourseId: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True

class Users(BaseModel):
    count: int
    results: List[UserItem]

    class Config:
        orm_mode = True
        from_attributes = True

class ProfileItem(BaseModel):
    ProfileId: Optional[int] = None
    NamePosition: Optional[str] = None
    Url: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

class Profiles(BaseModel):
    count: int
    results: List[ProfileItem]

    class Config:
        orm_mode = True
        from_attributes = True
        
        




@app.post("/anketa/")
async def post_anketa(fio: str = Form(...), telephone: str = Form(None), email: str = Form(...),soobsh: str = Form(...)):
    result = await conn.post_anketas(fio, telephone, email, soobsh)
    return {"anketaId": result}

@app.get("/courses/", response_model=Courses)
async def read_courses():
    results = await conn.get_courses()
    
    course_items = [CourseItem(CourseId=i[0], Name=i[1], Description=i[2], Url=i[3], ProfileId=i[4]) for i in results]
    return {"count": len(results), "results": course_items}


@app.get("/users/", response_model=Users)
async def read_users():
    results = await conn.get_users()
    
    user_items = [UserItem(UserId=i[0], Username=i[1], Password=i[2], Email=i[3], Surname=i[4], Name=i[5], Lastname=i[6], Created_at=i[7], CourseId=i[8]) for i in results]
    return {"count": len(results), "results": user_items}


@app.get("/profiles/", response_model=Profiles)
async def read_profiles():
    results = await conn.get_profiles()
    
    profile_items = [ProfileItem(ProfileId=i[0], NamePosition=i[1], Url=i[2]) for i in results]
    return {"count": len(results), "results": profile_items}


@app.post("/courses/")
async def create_course(name: str = Form(...), description: str = Form(...), url: str = Form(...), profile_id: int = Form(...)):
    result = await conn.post_course(name, description, url, profile_id)
    return {"CourseId": result}


@app.post("/users/")
async def create_user(username: str = Form(...), password: str = Form(...), email: str = Form(...), surname: str = Form(...), name: str = Form(...), lastname: str = Form(...), course_id: int = Form(...)):
    result = await conn.post_user(username, password, email, surname, name, lastname, course_id)
    return {"UserId": result}


@app.post("/profiles/")
async def create_profile(name_profile: str = Form(...), url: str = Form(...)):
    result = await conn.post_profile(name_profile, url)
    return {"ProfileId": result}


@app.put("/courses/{course_id}/")
async def update_course(course_id: int, name: str = Form(...), description: str = Form(...), url: str = Form(...), profile_id: int = Form(...)):
    await conn.update_course(course_id, name, description, url, profile_id)
    return {"message": "Course updated successfully"}


@app.put("/users/{user_id}/")
async def update_user(user_id: int, username: str = Form(...), password: str = Form(...), email: str = Form(...), surname: str = Form(...), name: str = Form(...), lastname: str = Form(...), course_id: int = Form(...)):
    await conn.update_user(user_id, username, password, email, surname, name, lastname, course_id)
    return {"message": "User updated successfully"}


@app.put("/profiles/{profile_id}/")
async def update_profile(profile_id: int, name_profile: str = Form(...), url: str = Form(...)):
    await conn.update_profile(profile_id, name_profile, url)
    return {"message": "Profile updated successfully"}


if __name__ == "__main__":

    conn = workwithbd()

    uvicorn.run(app, host="127.0.0.1", port=9010)

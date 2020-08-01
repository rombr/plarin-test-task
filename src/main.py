from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Depends, Query
from motor.motor_asyncio import AsyncIOMotorClient

from db import connect_to_mongo, close_mongo_connection, get_database
from models import (
    Employee, EmployeesListResponse, EmployeesFilterParams,
    Gender,
)


app = FastAPI()


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.get(
    "/api/v1/employees", response_model=EmployeesListResponse,
    tags=["employees"]
)
async def get_employees(
        name: Optional[str] = Query('', max_length=256),
        email: Optional[str] = Query('', max_length=256),
        age: Optional[int] = Query(None, gt=0, lt=200),
        company: Optional[str] = Query('', max_length=256),
        join_date: Optional[datetime] = Query(None),
        job_title: Optional[str] = Query('', max_length=256),
        gender: Optional[Gender] = Query(None),
        salary: Optional[int] = Query(None, gt=0),
        limit: Optional[int] = Query(20, gt=0, le=100),
        offset: Optional[int] = Query(0, ge=0),
        db: AsyncIOMotorClient = Depends(get_database),
):
    filters = EmployeesFilterParams(
        name=name, email=email, age=age, company=company,
        join_date=join_date, job_title=job_title,
        gender=gender, salary=salary,
        limit=limit, offset=offset,
    )

    # It is better to implement query builder class in real life
    filter_query = {}
    if filters.name:
        filter_query["name"] = {'$regex': filters.name}

    if filters.email:
        filter_query["email"] = {'$regex': filters.email}

    if filters.age:
        filter_query["age"] = {'$gte': filters.age}

    if filters.company:
        filter_query["company"] = {'$regex': filters.company}

    if filters.join_date:
        filter_query["join_date"] = {'$gte': filters.join_date}

    if filters.job_title:
        filter_query["job_title"] = {'$regex': filters.job_title}

    if filters.gender:
        filter_query["gender"] = filters.gender

    if filters.salary:
        filter_query["salary"] = {'$gte': filters.salary}

    # Fetch data
    collection = db.employees
    total = await collection.count_documents(filter_query)
    rows = collection.find(
        filter_query, limit=filters.limit, skip=filters.offset
    )

    items = []
    async for row in rows:
        items.append(Employee(**row))

    return EmployeesListResponse(
        objects=items, total=total,
        limit=filters.limit, offset=filters.offset
    )

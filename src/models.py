from typing import List
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'


class Employee(BaseModel):
    '''
    Employee item
    '''
    name: str
    email: str
    age: int
    company: str
    join_date: datetime
    job_title: str
    gender: Gender
    salary: int


class EmployeesListResponse(BaseModel):
    '''
    List of items
    '''
    objects: List[Employee]
    total: int
    limit: int
    offset: int


class EmployeesFilterParams(BaseModel):
    '''
    Filter params
    '''
    name: str = ''
    email: str = ''
    age: int = None
    company: str = ''
    join_date: datetime = None
    job_title: str = ''
    gender: Gender = None
    salary: int = None
    limit: int = 20
    offset: int = 0

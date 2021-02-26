from fastapi import APIRouter,Body,Query,Path
from fastapi.encoders import jsonable_encoder
import time
from ..database import(
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student
)

from ..models.student import (
    ErrorResponseModel,
    ResponseModel,
    UpdateStudentModel,
    StudentSchema

)

route = APIRouter()

@route.post("/",summary = "Student data added into the database")
async def add_student_data(student:StudentSchema=Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student,"success")

@route.get("/",summary="read all data about student")
async def get_students():
    print(time.time())
    #await time.sleep(10)
    students = await retrieve_students()
    if students:
        return ResponseModel(students,"Students data retrieved successful")
    else:
        return ResponseModel(students,"empty list returned")

@route.get("/{student_id}",summary = "read student data by it id")
async def get_student(student_id:str):
    student = await retrieve_student(student_id)
    if student.get("code")!=404:
        return ResponseModel(student,"student data is retrieved successful")
    elif student.get("code")==404:
        return ErrorResponseModel(student.get("error"),404,"id is invalid")
    else:
        return ErrorResponseModel("no student",404,"Student doesn't exist")

@route.put("/{student_id}",summary = "update student by id")
async def update_student_data(student_id:str,rep:UpdateStudentModel = Body(...)):
    rep = {k: v for k,v in rep.dict().items() if v is not None}
    student_updated = await update_student(student_id,rep)
    if student_updated:
        return ResponseModel(f"student has id:{student_id} is updated","Successfull update")
    else:
        return ErrorResponseModel("Error update",404,"Can not update to database")

@route.delete("/{student_id}",summary = "delete a student by id")
async def delete_student_data(student_id:str):
    deleted_student = await delete_student(student_id)
    if delete_student:
        return ResponseModel(f"student has id {student_id} have been deleted","delete success")
    else:
        return ErrorResponseModel("An error occur",404,f"Studenr has id {student_id} doesn't exist")

@route.get("/hello/")
async def get_something(name:str = Query(None,max_length=10,min_length=3)):
    return {"message":name}
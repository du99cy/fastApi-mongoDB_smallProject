import motor.motor_asyncio
import motor
from bson.objectid import ObjectId
MONGO_DETAILS = "mongodb://127.0.0.1:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.abc

students_collection = database.get_collection("students_collection")

#Next, create a quick helper function for parsing the results from a database query into a Python dict.

#helper

def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }

#import ObjectId
#bson comes installed as a dependency of motor.
async def retrieve_students():
    students=[]
    async for s in students_collection.find():
        students.append(student_helper(s))
    return students

# Add a new student into to the database
async def add_student(student_data:dict)->dict:
    student = await students_collection.insert_one(student_data)
    new_student = await students_collection.find_one({"_id":student.inserted_id})
    return student_helper(new_student)

# Retrieve a student with a matching ID
async def retrieve_student(id:str)->dict:
    
    object_id = ObjectId(id)
    student = await students_collection.find_one({"_id":object_id})
    try: 
        return student_helper(student)
            
    except Exception as exp:
        return {"error":"student id doesn't exist","code":404}

    

# Update a student with a matching ID
async def update_student(id:str,data:dict):
    # Return false if an empty request body is sent.
    if len(data)<1:
        return False
    student = await students_collection.find_one({"_id":ObjectId(id)})
    if student:
        updated_student = await students_collection.update_one({"_id":ObjectId(id)},{"$set":data})
        if update_student:
            return True
        else:
            return {"error":"fail"}
    else:
        return {"error":"not found any student"}
    
## Delete a student from the database
async def delete_student(id:str):
    student = await students_collection.find_one({"_id":ObjectId(id)})
    if student:
        await students_collection.delete_one({"_id":ObjectId(id)})
        return True
    else:
        return False




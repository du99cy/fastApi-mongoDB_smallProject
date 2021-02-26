from fastapi import FastAPI
from .routes.student import route as StudentRoute


app = FastAPI()

app.include_router(StudentRoute,tags=["Student"],prefix="/student")

@app.get("/",tags = ["Root"])
async def welcome():
    return {"message":"welcome to my app"}
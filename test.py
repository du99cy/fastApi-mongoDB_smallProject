from pydantic import BaseModel

class A(BaseModel):
    name:str


a=A()
a.name = 12 
print(a.name)
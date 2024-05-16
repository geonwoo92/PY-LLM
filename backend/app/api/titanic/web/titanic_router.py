import os
from fastapi import APIRouter
from pydantic import BaseModel
from app.api.titanic.service.titanic_service import TitanicService

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

router = APIRouter()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str

service = TitanicService()

@router.post('/titanic')
async def titanic(req:Request):
    print('타이타닉 딕셔너리 내용')
    hello = 'C:\\Users\\bitcamp\\IdeaProjects\\kubernetes\\chat-server\\backend\\app\\api\\context\\data\\hello.txt'
    f = open(hello, "r", encoding="utf-8")
    data = f.read()
    print(data)
    f.close()

    
    service.preprocess()
    print(req)
    

    return{"타이타닉 생존자는 100명"}

@router.post('/new2')
async def news2(req:Request):
 
   

    print(req)
    

    return{"두번째 버튼 응답."}


@router.post('/new3')
async def news2(req:Request):
 
   

    print(req)
    

    return{"주말 언제 오나요?"}
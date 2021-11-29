from fastapi import FastAPI
from appSe import appBot
from fastapi.middleware.cors import CORSMiddleware
#             uvicorn api:server --reload --reload


server = FastAPI()


origins = ['http://127.0.0.1:8000']

server.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@server.get('/buscar/notebook/lenovo')
async def  buscar():
    response = appBot().buscar()
    return response
    

@server.get('/buscar/{marca}')
async def buscarNote(marca:str):
    response = appBot().getPages(marca)
    return response
    
@server.get('/')
async def home():
    msg = 'API BOT'
    return msg


import uvicorn
from fastapi import FastAPI
from api import main
from starlette.middleware.cors import CORSMiddleware
from core.redis_subscriber import start_redis_subscriber

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.api_router)

#if __name__ == '__main__':
    #uvicorn.run('main:app', reload=True)

@app.on_event("startup")
async def startup_event():
    start_redis_subscriber()

@app.get("/")
async def root():
    return {"message": "Hello World"}


from fastapi import FastAPI
import model
from connection import engine
import routes
from fastapi.middleware.cors import CORSMiddleware
#config DB
model.Base.metadata.create_all(bind=engine)


# Instance
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tauri.localhost"],
    # allow_origins=["http://localhost:1420"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# config routes
app.include_router(routes.userRouter)
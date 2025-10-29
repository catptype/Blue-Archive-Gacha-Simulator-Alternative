from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware: This is crucial to allow your Vue frontend
# to communicate with your FastAPI backend on your local machine.
origins = [
    "http://localhost:5173", # The default Vue dev server port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "From FastAPI Backend"}

@app.get("/api/gacha/pull")
def perform_gacha_pull():
    # In the future, your gacha logic will go here!
    # For now, let's return a sample result.
    return {"item_name": "Legendary Sword", "rarity": "SSR"}
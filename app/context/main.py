from fastapi import FastAPI, status
from app.api.contacts.contacts import router as contacts_router
from app.api.users.users import router as users_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_404_NOT_FOUND)
async def root():
    return {"message": "nothing to see here"}


@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Contact Nest API is running"}

app.include_router(prefix="/contacts", tags=["contacts"], router=contacts_router)
app.include_router(prefix="/users", tags=["users"], router=users_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

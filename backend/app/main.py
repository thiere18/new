import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from backend.app import models
from backend.app.database import engine
from backend.app.endpoints import auth, convert, users

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=status.HTTP_200_OK)
def healthy_condition():
    return {"status": "Ok"}


app.include_router(convert.router, prefix="/api", tags=["highlight"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(auth.router, prefix="/api", tags=["Auth"])
if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app", host="0.0.0.0", port=8000, reload=True, debug=True
    )  # noqa

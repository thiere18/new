import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

DATABASE_HOSTNAME = "d"
DATABASE_PORT = 5432
DATABASE_PASSWORD = "postgres"

DATABASE_NAME = "postgres"
DATABASE_USERNAME = "postgres"
SECRET_KEY = "frgsthjsvfryntumyjhnbverjutk4567654"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

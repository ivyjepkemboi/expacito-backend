# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv(
#         "DATABASE_URL",
#         "mysql+mysqlconnector://root:Xandie0723510665#@localhost/incomexpense"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

import os

class Config:
    # Build DB connection from Cloud Run env vars
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "")
    INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME", "")

    if INSTANCE_CONNECTION_NAME:
        # Cloud SQL Unix socket connection
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
            f"@/localhost/{INSTANCE_CONNECTION_NAME}/{DB_NAME}"
        )
    else:
        # Local dev fallback
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "mysql+pymysql://root:yourpassword@localhost/incomexpense"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

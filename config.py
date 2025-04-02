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
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "")
    INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME", "")

    if INSTANCE_CONNECTION_NAME:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}"
            f"?unix_socket=/cloudsql/{INSTANCE_CONNECTION_NAME}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "mysql+pymysql://root:Xandie0723510665#@localhost/incomexpense"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")


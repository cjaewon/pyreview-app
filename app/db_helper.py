"""
This project uses tinydb for DBMS.
So, you must run web server with only one process or thread.
If you want to use it in multi-process, thread, you will use sqlite or lock.

todo: lock 구현 필요시
"""

import os
import hashlib
import base64
import hmac
import datetime
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query

db = TinyDB('db.json')

users_table = db.table("users")
logs_table = db.table("users")

class User(BaseModel):
  username: str
  hashed_password: str
  is_vertified: bool = False
  created_at: datetime.datetime = Field(
    default_factory=lambda: datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
  )

  @staticmethod
  def hash_password(password: str) -> str:
    # todo: cpu bound task이기 때문에 다른 스레드에 위임하여 비동기적으로 처리하는 것도 나중에는 생각해봐야함.
    salt = os.urandom(16)
    iterations = 600000

    hashed_password = hashlib.pbkdf2_hmac(
      "sha256", password.encode("utf-8"), salt, iterations
    )

    b64_salt = base64.b64encode(salt).decode("ascii").strip()
    b64_hash = base64.b64encode(hashed_password).decode("ascii").strip()

    return f"pbkdf2_sha256${iterations}${b64_salt}${b64_hash}"

  @staticmethod
  def verify_password(password: str, hashed_password: str) -> bool:
    algorithm, iterations_str, b64_salt, b64_hash = hashed_password.split("$", 3)

    if algorithm != "pbkdf2_sha256":
      raise ValueError("Unsupported password hashing algorithm.")

    iterations = int(iterations_str)
    salt = base64.b64decode(b64_salt)
    hashed_password_bytes = base64.b64decode(b64_hash)

    hashed_checking_password = hashlib.pbkdf2_hmac(
      "sha256", password.encode("utf-8"), salt, iterations
    )

    return hmac.compare_digest(hashed_checking_password, hashed_password_bytes)

class Log(BaseModel):
  problem_text: str
  code: str
  created_at: datetime.datetime = Field(
    default_factory=lambda: datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
  )
  fk_username: str

def create_user(username: str, password: str) -> User:
  u = User(
    username=username,
    hashed_password=User.hash_password(password),
  )

  users_table.insert(u.model_dump())

  return u

def create_log(log: Log):
  logs_table.insert(log.model_dump())

  return log


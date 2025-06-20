"""
warn

This project saves sessions data in dictionary (in-memory)
So, you must run web server with only one process or thread.
If you want to use it in multi-process, thread, you will use redis or other database.
"""

from __future__ import annotations
import secrets
from typing import Annotated
from db_helper import kst_now


from fastapi import Cookie, Depends, HTTPException
from pydantic import BaseModel, Field

session_store: dict[str, Session] = {}


class Session(BaseModel):
  username: str
  created_at: float = Field(default_factory=kst_now)


def create_session_id(length=32) -> str:
  return secrets.token_urlsafe(length)


def auth_required(session_id: Annotated[str | None, Cookie()] = None) -> str:
  if session_id is None:
    raise HTTPException(status_code=401)

  # 세션 존재 안 함
  if session_id not in session_store:
    raise HTTPException(status_code=401)

  session = session_store[session_id]

  # 세션 만료
  if kst_now() - session.created_at > 86400:
    del session

    raise HTTPException(status_code=401)

  return session.username


AuthRequiredDep = Annotated[str, Depends(auth_required)]


def auth_required_redirect(session_id: Annotated[str | None, Cookie()] = None) -> str:
  if session_id is None:
    raise HTTPException(status_code=401)

  # 세션 존재 안 함
  if session_id not in session_store:
    raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/signin"})

  session = session_store[session_id]

  # 세션 만료
  if kst_now() - session.created_at > 86400:
    del session

    raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/signin"})

  return session.username


AuthRequiredRedirectDep = Annotated[str, Depends(auth_required_redirect)]

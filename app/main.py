from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field, TypeAdapter
from tinydb import Query
import tools
from db_helper import Log, kst_now, users_table, logs_table, User
from front_helper import read_html
from auth_helper import AuthRequiredRedirectDep, AuthRequiredDep, session_store, create_session_id, Session

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root(username: AuthRequiredRedirectDep):
  return HTMLResponse(content=read_html("frontend/html/main.html"), status_code=200)


@app.get("/signin", response_class=HTMLResponse)
def signin():
  return HTMLResponse(content=read_html("frontend/html/signin.html"), status_code=200)


@app.get("/signup", response_class=HTMLResponse)
def signup():
  return HTMLResponse(content=read_html("frontend/html/signup.html"), status_code=200)


class CodeReviewReq(BaseModel):
  problem_text: str | None = Field(max_length=700)
  code: str = Field(max_length=1000)


class CodeReviewResp(BaseModel):
  formatter_result: tuple[bytes, bytes, int | None]
  linter_result: tuple[bytes, bytes, int | None]
  review_ai_result: str | None


@app.post("/api/pycode-review")
async def pycode_review_api(body: CodeReviewReq, username: AuthRequiredDep) -> CodeReviewResp:
  log_q = Query()

  logs = logs_table.search((log_q.username == username) & (kst_now() - 86400 <= log_q.created_at))
  print(logs)
  if len(logs) >= 5:
    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)

  log = Log(
    code=body.code,
    problem_text=body.problem_text,
    username=username,
  )
  logs_table.insert(log.model_dump())

  return CodeReviewResp(
    formatter_result = await tools.ruff_format(body.code),
    linter_result = await tools.ruff_lint(body.code),
    review_ai_result = await tools.review_ai.review_chat_completions_api(body.problem_text, body.code),
  )


class SignUpReq(BaseModel):
  username: str = Field(max_length=16)
  password: str = Field(min_length=6)


@app.post(
  "/api/signup",
)
def signup_api(body: SignUpReq, resp: Response):
  q = Query()

  if users_table.get(q.username == body.username) is not None:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT)

  u = User(
    username=body.username,
    hashed_password=User.hash_password(body.password),
  )

  users_table.insert(u.model_dump())

   # return u, 하면 u hashed_password 또한 같이 리턴 되므로 만약 이렇게 수정한다면 주의해야함.


class SignInReq(BaseModel):
  username: str = Field(max_length=14)
  password: str = Field(min_length=6)


@app.post("/api/signin")
def signin_api(body: SignInReq, resp: Response):
  q = Query()
  user = users_table.get(q.username == body.username)

  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  
  user = User.model_validate(user)

  if not User.verify_password(body.password, user.hashed_password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


  if not user.is_vertified:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


  while True:
    session_id = create_session_id()

    if session_id not in session_store:
      break

  session_store[session_id] = Session(username=user.username)
  
  # production -> use secure: bool = False
  resp.set_cookie("session_id", session_id, max_age=86400, httponly=True)

  return

@app.post("/api/signout", response_class=RedirectResponse)
def signout_api(req: Request, resp: Response):
  session_id = req.cookies.get("session_id")

  if session_id is not None and session_id in session_store:
    del session_store[session_id]

  # resp.set_cookie("session_id", "", max_age=0)
  resp.delete_cookie("session_id")
from fastapi import FastAPI, Response, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from tinydb import Query
import tools
from db_helper import users_table, User
from front_helper import read_html_with_cache

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def root():
  return HTMLResponse(content=read_html_with_cache("frontend/html/main.html"), status_code=200)


@app.get("/signin", response_class=HTMLResponse)
def signin():
  return HTMLResponse(content=read_html_with_cache("frontend/html/signin.html"), status_code=200)


@app.get("/signup", response_class=HTMLResponse)
def signup():
  return HTMLResponse(content=read_html_with_cache("frontend/html/signup.html"), status_code=200)


class CodeReviewReq(BaseModel):
  problem_text: str | None
  code: str


class CodeReviewResp(BaseModel):
  formatter_result: tuple[bytes, bytes, int | None]
  linter_result: tuple[bytes, bytes, int | None]
  review_ai_result: str | None


@app.post("/api/pycode-review")
async def pycode_review_api(body: CodeReviewReq) -> CodeReviewResp:
  return CodeReviewResp(
    formatter_result=await tools.ruff_format(body.code),
    linter_result=await tools.ruff_lint(body.code),
    review_ai_result=await tools.review_ai.review_chat_completions_api(body.problem_text, body.code),
  )


class SignUpReq(BaseModel):
  username: str = Field(max_length=16)
  password: str = Field(min_length=6)


@app.post(
  "/api/signup",
  responses={status.HTTP_200_OK: {}, status.HTTP_409_CONFLICT: {}},
)
def signup_api(body: SignUpReq, resp: Response):
  q = Query()

  if users_table.get(q.username == body.username) is not None:
    resp.status_code = status.HTTP_409_CONFLICT

    return

  u = User(
    username=body.username,
    hashed_password=User.hash_password(body.password),
  )

  users_table.insert(u.model_dump())

  resp.status_code = status.HTTP_200_OK

  return  # return u, 하면 u hashed_password 또한 같이 리턴 되므로 만약 이렇게 수정한다면 주의해야함.


class SignInReq(BaseModel):
  username: str = Field(max_length=14)
  password: str = Field(min_length=6)


@app.post("/api/signin")
def signin_api(body: SignInReq, resp: Response):
  pass

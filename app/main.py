from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import tools
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
    review_ai_result=await tools.review_ai.review_chat_completions_api(body.problem_text, body.code)
  )
import asyncio
from openai import AsyncOpenAI
from config_helper import OpenAIConfig, config

class ReviewAI:
  def __init__(self, config: OpenAIConfig):
    self.client = AsyncOpenAI(
      api_key=config.api_key,
    )
    self.prompt = config.prompt
    self.model = config.model

  async def review(self, problem_text: str | None, code: str):
    ai_input: str

    if problem_text is None:
      ai_input = f"다음은 내 코드야.\n{code}"
    else:
      ai_input = f"다음은 내가 풀어야 하는 문제야.\n{problem_text}\n\n다음은 내 코드야.\n{code}"
      

    response = await self.client.responses.create(
      model=self.model,  # "gpt-4o-mini",
      instructions=self.prompt,
      input=ai_input,
    )

    return response.output_text

  # "o1-mini" o1-mini는 chat.completions을 통해서만 사용 가능함.
  async def review_chat_completions_api(
    self, problem_text: str | None, code: str
  ) -> str | None:
    ai_input: str

    if problem_text is None:
      ai_input = f"다음은 내 코드야.\n{code}"
    else:
      ai_input = f"다음은 내가 풀어야 하는 문제야.\n{problem_text}\n\n다음은 내 코드야.\n{code}"
      

    completion = await self.client.chat.completions.create(
      model=self.model,
      messages=[{"role": "user", "content": ai_input}],
    )

    return completion.choices[0].message.content

review_ai = ReviewAI(config.openai)

async def ruff_format(code: str) -> tuple[bytes, bytes, int | None]:
  process = await asyncio.create_subprocess_exec(
    "ruff",
    "format",
    "-",
    stdin=asyncio.subprocess.PIPE,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
  )

  stdout, stderr = await process.communicate(input=code.encode("utf-8"))

  return (stdout, stderr, process.returncode)

async def ruff_lint(code: str) -> tuple[bytes, bytes, int | None]:
  process = await asyncio.create_subprocess_exec(
    "ruff",
    "check",
    "--select=ALL",
    "--output-format=concise",
    "-",
    stdin=asyncio.subprocess.PIPE,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
  )

  stdout, stderr = await process.communicate(input=code.encode("utf-8"))

  return (stdout, stderr, process.returncode)

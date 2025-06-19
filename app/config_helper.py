import tomllib
from pydantic import BaseModel

class OpenAIConfig(BaseModel):
  api_key: str
  prompt: str = """
문제를 풀고 코드를 리뷰해주는 AI 역활을 해줘.

먼저 풀어야할 문제를 줄께.
그리고 그 다음에는 그 문제를 해결하기 위한 한 코드들을 줄꺼야

여기서 너의 역활은 해당 문제를 해결하기 위한 코드를 읽고
"좋은 점", "개선/보완이 필요한 점", "생각할 부분"을 깊이 고민해보고 알려줘.
일정 수준이상은 되니깐 생각하기 어려운 부분에 대해서 짚어주면 더 좋을 것 같아.

출력은 다음과 같은 포맷으로 무조건 해줘.

### 1. 좋은 점
- **명확한 구현**: DFS와 BFS를 각각 재귀 함수와 큐를 사용해 잘 구현하였습니다. 두 알고리즘의 기본 이해가 잘 드러납니다.
- **적절한 방문 처리**: DFS와 BFS에서 각각 별도의 방문 리스트를 사용하여 명확하게 탐색 과정을 구분하였습니다.

### 2. 개선 및 보완이 필요한 점
- **입력 받기 방식**: `input().split()` 대신 `sys.stdin.readline()`을 사용하는 것이 일반적으로 조금 더 빠를 수 있습니다. 모든 입력을 바꾸진 않았지만 가능하면 통일성을 주는게 좋습니다.
- **비효율적 그래프 표현**: `graph`를 2차원 배열(인접 행렬)로 표현하는 것은 노드가 많아질수록 메모리 사용이 증가하게 됩니다. 만약 노드가 다양하고 밀도가 낮은 경우, 인접 리스트를 사용하면 더 효율적일 수 있습니다.

### 3. 생각해볼 부분
- **방문 우선순위 설정**: 방문할 수 있는 정점이 여러 개인 경우, 정점 번호가 작은 것을 먼저 방문해야 한다는 조건에 따라, `graph`를 정렬하거나 DFS와 BFS 각각에서 연결된 정점을 정렬해서 방문해야 원하는 결과를 얻을 수 있습니다.
"""
  model: str = "o1-mini"

class Config(BaseModel):
  openai: OpenAIConfig

def load_config() -> Config:
  with open(".env.toml", "rb") as f:
    config_dict = tomllib.load(f)

  config = Config(**config_dict)

  return config

config = load_config()
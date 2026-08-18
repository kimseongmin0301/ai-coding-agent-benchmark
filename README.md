# AI Coding Agent Benchmark

Codex CLI와 Claude Code를 동일한 Repository, 동일한 Issue, 동일한 종료 조건에서 비교하기 위한 실험용 Repository입니다.

## 목적

이 Repository의 목적은 단순히 어떤 도구가 더 좋은 코드를 생성하는지 보는 것이 아닙니다.

다음을 비교합니다.

- 기존 코드베이스 이해
- 요구사항 해석
- 수정 범위 판단
- 구현 정확성
- 테스트 작성 능력
- 기존 동작 보존
- 예외 처리
- 문서화
- 작업 과정의 안정성
- 불필요한 수정 여부

## 실험 흐름

```text
동일 Repository
      ↓
동일 Issue
      ↓
Codex CLI / Claude Code 각각 독립 실행
      ↓
테스트 실행
      ↓
diff 저장
      ↓
결과 비교
      ↓
상호 평가
```

## 기준 Branch

각 Agent는 동일한 초기 상태에서 시작해야 합니다.

권장 방식:

```bash
git checkout benchmark-base
git checkout -b experiment/codex-task-002
```

Claude Code 실험 시에는 다시 기준 상태에서 별도 Branch를 생성합니다.

```bash
git checkout benchmark-base
git checkout -b experiment/claude-task-002
```

두 Agent가 서로의 변경 사항을 볼 수 없도록 합니다.

## 실행

Python 3.11 이상을 권장합니다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

## 사용자 검색 API

```text
GET /users/search?email=<keyword>
```

저장된 사용자 중 이메일에 검색어가 포함된 사용자를 반환합니다.

정책:

- `email` query parameter는 필수입니다. 누락하면 `HTTP 422`를 반환합니다.
- 검색어는 최소 2글자 이상이어야 합니다. 2글자 미만이면 `HTTP 400`과
  `Search keyword must be at least 2 characters` detail을 반환합니다.
- 이메일 비교는 대소문자를 구분하지 않는 부분일치입니다.
  `ALICE`와 `alice`는 같은 결과를 반환하며, `@example`처럼 일부만 입력해도 검색됩니다.
- 조건을 만족하는 사용자를 모두 반환하며, 기존 저장 순서를 유지합니다.
- 검색 결과가 없어도 오류가 아닙니다. `HTTP 200`과 빈 배열 `[]`을 반환합니다.

예:

```text
GET /users/search?email=alice   -> 200 [{"id": 1, "name": "Alice", "email": "alice@example.com"}]
GET /users/search?email=@example -> 200 [ ... 여러 사용자 ... ]
GET /users/search?email=nobody  -> 200 []
GET /users/search?email=a       -> 400 {"detail": "Search keyword must be at least 2 characters"}
```

`/users/search`는 `/users/{user_id}`보다 먼저 선언되어 있어야 합니다.
FastAPI는 선언 순서대로 route를 매칭하므로, 순서가 바뀌면 `search`가 `user_id`로 해석되어
`HTTP 422`가 반환됩니다.

## Task 002

실제 과제 정의는 아래 문서를 사용합니다.

```text
benchmark/task-002.md
```

두 Agent에게 **같은 파일, 같은 Issue, 같은 초기 commit**을 제공해야 합니다.

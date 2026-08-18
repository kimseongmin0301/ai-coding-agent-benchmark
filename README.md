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

## API 동작 정책

`POST /users`

- 이메일은 대소문자를 구분하지 않고 유일해야 합니다. `alice@example.com`과 `ALICE@example.com`은 같은 이메일로 취급합니다.
- 이미 등록된 이메일로 생성을 시도하면 `409 Conflict`와 `Email already exists`를 반환합니다.
- 저장되는 이메일 값은 요청에 담긴 원본 표기를 그대로 유지합니다. 대소문자 무시는 비교에만 적용됩니다.
- 새 사용자 ID는 사용자 삭제 이후에도 기존 ID와 충돌하지 않도록 생성합니다. 현재 저장된 최대 ID + 1을 사용하며, 기존 사용자를 덮어쓰지 않습니다.

## Task 002

실제 과제 정의는 아래 문서를 사용합니다.

```text
benchmark/task-002.md
```

두 Agent에게 **같은 파일, 같은 Issue, 같은 초기 commit**을 제공해야 합니다.

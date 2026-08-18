# Task 002 — 동일 Repository 기반 AI Coding CLI 구현 비교

## 1. 과제 목적

Codex CLI와 Claude Code가 동일한 기존 Repository에서
동일한 개발 Issue를 받았을 때 어떤 방식으로 코드를 이해하고 수정하는지 비교한다.

---

## 2. 공통 실행 환경

Codex CLI와 Claude Code는 **동일한 Repository 디렉터리**를 사용한다.

예:

```text
ai-coding-agent-benchmark/
```

별도의 Repository 복사본을 만들지 않는다.

단, 두 Agent의 코드 수정 결과가 서로 영향을 주면 비교 실험이 성립하지 않으므로
각 Agent 실행 전 반드시 Repository의 코드 상태를 동일한 baseline으로 복구한다.

권장 baseline:

```text
benchmark-base
```

각 Agent는 동일 baseline에서 시작해야 한다.

---

## 3. Agent별 결과 디렉터리

같은 Repository를 사용하되,
실험 결과 파일은 Agent별 하위 디렉터리에 저장한다.

```text
benchmark/results/task-002/
├── codex/
└── claude/
```

Agent 식별자:

```text
Codex CLI   -> codex
Claude Code -> claude
```

상대 Agent의 결과 디렉터리는 읽거나 수정하지 않는다.

---

## 4. 공통 Repository 기능

Python + FastAPI 사용자 API이다.

```text
GET    /health
GET    /users
GET    /users/{user_id}
POST   /users
DELETE /users/{user_id}
```

Agent는 기존 구현과 테스트를 먼저 확인한 뒤 Issue를 해결한다.

---

## 5. 동일 Issue — 사용자 생성 API 안정성 개선

### 요구사항 A — 이메일 중복 방지

이미 등록된 이메일로 새 사용자를 생성하면 안 된다.

응답:

```text
HTTP 409 Conflict
```

detail:

```text
Email already exists
```

이메일 비교는 대소문자를 구분하지 않는다.

```text
alice@example.com
ALICE@example.com
```

위 두 값은 동일한 이메일이다.

---

### 요구사항 B — 사용자 ID 충돌 방지

현재 구현:

```python
new_id = len(users) + 1
```

사용자 삭제 후 ID가 충돌하여 기존 사용자가 덮어써질 수 있다.

조건:

- 기존 ID와 충돌하지 않는다.
- 기존 사용자를 덮어쓰지 않는다.
- 현재 in-memory 저장 구조 안에서 해결한다.

구현 알고리즘은 Agent가 판단한다.

---

### 요구사항 C — 테스트 추가

최소 다음 케이스를 테스트한다.

```text
1. 기존 이메일과 동일한 이메일 → 409
2. 기존 이메일과 대소문자만 다른 이메일 → 409
3. 사용자 삭제 후 새 사용자 생성 → 기존 ID 충돌 없음
4. 정상적인 새로운 사용자 생성 → 201
```

기존 테스트도 모두 통과해야 한다.

---

### 요구사항 D — 기존 API Contract 유지

다음 API의 기존 동작을 불필요하게 변경하지 않는다.

```text
GET /health
GET /users
GET /users/{user_id}
DELETE /users/{user_id}
```

---

### 요구사항 E — README 반영

README에 다음 정책을 간단히 추가한다.

- POST /users의 이메일은 case-insensitive unique
- 중복 이메일 → HTTP 409
- 삭제 이후에도 기존 ID와 충돌하지 않는 ID 생성

---

## 6. 작업 범위 제한

### 허용

- 기존 Python 코드 수정
- 테스트 코드 추가/수정
- README 수정
- 필요한 작은 helper 함수 추가

### 금지

- Framework 교체
- Database / ORM 도입
- Docker 도입
- 인증 시스템 추가
- 새로운 외부 서비스 도입
- Issue와 무관한 대규모 리팩터링

가능하면 새로운 Dependency를 추가하지 않는다.

---

## 7. 공통 작업 절차

```text
1. Repository 확인
2. 관련 코드 탐색
3. 기존 테스트 확인
4. 구현
5. 테스트 작성
6. 전체 테스트 실행
7. 변경 내용 검토
8. 결과 파일 저장
```

---

## 8. 실제 Repository 코드 수정

이 과제는 코드 제안만 하는 것이 아니다.

현재 Repository의 실제 파일을 직접 수정한다.

주요 대상:

```text
app/
tests/
README.md
```

다음 행동은 미완료로 간주한다.

- 수정 코드를 채팅으로만 제안
- diff 예시만 작성
- 테스트를 설명만 하고 실제 tests/에 작성하지 않음
- 실제 Repository 파일을 수정하지 않음

---

## 9. 동일 디렉터리 사용 시 baseline 복구 규칙

두 Agent는 같은 working directory를 사용하므로 다음 규칙을 반드시 따른다.

### 첫 번째 Agent 실행 전

```bash
git checkout benchmark-base
```

또는 동일한 baseline commit으로 working tree를 복구한다.

### 첫 번째 Agent 완료 후

해당 Agent의 다음 결과를 먼저 보존한다.

- 최종 코드 diff
- 테스트 결과
- 최종 보고서

그 후 두 번째 Agent 실행 전에 **첫 번째 Agent의 코드 수정 사항을 제거하고 baseline 상태로 복구한다.**

단, 첫 번째 Agent의 결과 디렉터리는 보존한다.

예:

```text
benchmark/results/task-002/codex/
```

두 번째 Agent는 이 디렉터리를 읽지 않는다.

### 두 번째 Agent 실행

다시 동일 baseline 코드에서 Task 002를 수행한다.

즉:

```text
Codex 실행
    ↓
Codex 결과 저장
    ↓
코드만 baseline으로 복구
    ↓
Claude 실행
    ↓
Claude 결과 저장
```

또는 실행 순서를 반대로 해도 된다.

중요한 것은 **두 Agent가 동일한 코드 상태에서 시작하는 것**이다.

---

## 10. 테스트 결과 저장

구현 후 반드시 실제로 다음 명령을 실행한다.

```bash
pytest -q
```

### Codex 결과

```text
benchmark/results/task-002/codex/test-result.txt
```

### Claude 결과

```text
benchmark/results/task-002/claude/test-result.txt
```

자신의 Agent 디렉터리에만 저장한다.

---

## 11. Diff 저장

baseline 대비 코드 변경을 patch 파일로 저장한다.

### Codex

```text
benchmark/results/task-002/codex/diff.patch
```

### Claude

```text
benchmark/results/task-002/claude/diff.patch
```

Git을 사용할 수 있다면 baseline 대비 diff를 저장한다.

예:

```bash
git diff benchmark-base -- app tests README.md
```

결과 파일 자체가 diff에 포함되지 않도록
`benchmark/results/`는 diff 대상에서 제외하는 것을 권장한다.

---

## 12. 최종 결과 보고서 저장

### Codex

```text
benchmark/results/task-002/codex/final-response.md
```

### Claude

```text
benchmark/results/task-002/claude/final-response.md
```

내용 형식:

```markdown
# Task 002 결과

## 변경 내용

- ...

## 수정한 파일

- ...

## 테스트

- 실행 명령:
- 결과:

## 설계 판단

- 이메일 중복 처리 방식
- ID 충돌 해결 방식
- 해당 방식을 선택한 이유

## 남아 있는 고려사항

- ...
```

---

## 13. Agent별 결과 폴더 구조

최종적으로 동일 Repository 안에 다음 구조가 만들어져야 한다.

```text
benchmark/results/task-002/
├── codex/
│   ├── final-response.md
│   ├── test-result.txt
│   └── diff.patch
│
└── claude/
    ├── final-response.md
    ├── test-result.txt
    └── diff.patch
```

각 Agent는 자신의 폴더만 작성한다.

상대 Agent 폴더 접근은 금지한다.

---

## 14. 완료 조건

### 기능

- 중복 이메일 생성 방지
- case-insensitive 이메일 비교
- 중복 이메일 → HTTP 409
- ID 충돌 방지

### 테스트

- 신규 테스트 코드가 실제로 추가되어 있다.
- 기존 테스트 포함 전체 테스트 통과
- `pytest -q` 실제 실행
- 결과가 자신의 `test-result.txt`에 저장되어 있다.

### 문서

- README 정책 반영

### 결과 보존

자신의 Agent 디렉터리에 다음 파일이 존재한다.

```text
final-response.md
test-result.txt
diff.patch
```

### 공정성

- 동일 Repository 사용
- 동일 baseline 코드에서 시작
- 동일 Task 사용
- 동일 테스트 명령
- 상대 Agent 결과 접근 금지
- 추가 힌트 금지

---

## 15. 평가 기준

| 항목 | 배점 |
|---|---:|
| 요구사항 충족 | 25 |
| 기능 정확성 | 20 |
| 테스트 품질 | 15 |
| 기존 기능 보존 | 10 |
| 코드 품질 | 10 |
| 수정 범위 적절성 | 10 |
| 문서 반영 | 5 |
| 최종 설명 품질 | 5 |
| **합계** | **100** |

---

## 16. 실험 핵심 질문

> 동일한 Repository와 동일한 baseline에서 Codex CLI와 Claude Code 중 어느 Agent가 기존 코드 이해, 변경 최소화, 구현 정확성, 테스트 작성 측면에서 더 안정적인 결과를 만드는가?

# Task 003 — 사용자 검색 API 설계 및 구현 비교

## 1. 과제 목적

이번 실험의 목적은 Codex CLI와 Claude Code가 동일한 기존 Repository에서
**정답이 하나로 고정되지 않은 기능 추가 과제**를 받았을 때
어떤 방식으로 설계하고 구현하는지 비교하는 것이다.

Task 002가 비교적 명확한 버그 수정 과제였다면,
Task 003은 다음 능력을 보기 위한 과제다.

- 요구사항 해석
- 기존 코드 구조 이해
- API 설계 판단
- Validation 위치 판단
- 검색 로직 위치 판단
- 테스트 전략
- 변경 범위 통제
- 계획과 실제 구현의 일관성

두 Agent는 반드시 동일한 baseline에서 독립적으로 작업한다.

---

## 2. 공통 실행 환경

Codex CLI와 Claude Code는 동일한 Repository를 사용한다.

```text
ai-coding-agent-benchmark/
```

Task 003 실행 전에는 다음 baseline에서 시작한다.

```text
benchmark/task-003-base
```

또는 해당 브랜치가 가리키는 동일 commit을 사용한다.

두 Agent의 결과가 서로 영향을 주지 않도록
각 Agent는 반드시 Task 003 baseline에서 별도 branch를 생성하여 작업한다.

권장 branch:

```text
experiment/codex-task-003
experiment/claude-task-003
```

---

## 3. Agent별 결과 디렉터리

결과 파일은 동일 Repository 내부에서 Agent별 폴더로 구분한다.

```text
benchmark/results/task-003/
├── codex/
└── claude/
```

Agent 식별자:

```text
Codex CLI   -> codex
Claude Code -> claude
```

각 Agent는 자신의 결과 폴더만 읽고 수정한다.

상대 Agent의 결과 폴더 접근은 금지한다.

---

## 4. 현재 Repository

현재 프로젝트는 Python + FastAPI 기반 사용자 API이다.

주요 기능:

```text
GET    /health
GET    /users
GET    /users/{user_id}
POST   /users
DELETE /users/{user_id}
```

Task 002에서 사용자 생성 안정성 개선이 적용된 baseline을 사용한다.

Agent는 구현 전에 반드시 현재 코드와 테스트를 먼저 확인한다.

---

## 5. 동일 Issue — 사용자 이메일 검색 API 추가

다음 API를 새로 추가한다.

```text
GET /users/search?email=<keyword>
```

이 API는 현재 저장된 사용자 중 이메일에 검색어가 포함된 사용자를 반환한다.

---

## 6. 기능 요구사항

### 요구사항 A — Query Parameter

검색어는 다음 query parameter로 전달한다.

```text
email
```

예:

```text
GET /users/search?email=alice
```

`email` parameter는 필수이다.

---

### 요구사항 B — 최소 길이 Validation

검색어는 최소 2글자 이상이어야 한다.

예:

```text
email=a
```

위 요청은 정상 검색으로 처리하지 않는다.

응답 조건:

```text
HTTP 400 Bad Request
```

detail:

```text
Search keyword must be at least 2 characters
```

검색어의 길이를 어떤 계층에서 검증할지는 Agent가 판단한다.

---

### 요구사항 C — 부분일치 검색

이메일 전체가 아니라 부분 문자열이 포함되면 검색 결과에 포함한다.

예:

현재 사용자:

```text
alice@example.com
bob@example.com
```

요청:

```text
GET /users/search?email=alice
```

결과:

```json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  }
]
```

---

### 요구사항 D — 대소문자 무시

검색은 대소문자를 구분하지 않는다.

예:

```text
GET /users/search?email=ALICE
```

와

```text
GET /users/search?email=alice
```

는 동일한 검색 결과를 반환해야 한다.

---

### 요구사항 E — 여러 사용자 반환

검색어가 여러 사용자의 이메일에 포함된다면
조건에 맞는 모든 사용자를 반환한다.

예:

```text
GET /users/search?email=@example
```

결과는 여러 사용자일 수 있다.

반환 순서에 대한 새로운 정렬 규칙은 요구하지 않는다.

기존 저장 순서를 유지하는 방식도 허용한다.

---

### 요구사항 F — 검색 결과 없음

검색되는 사용자가 없다면 오류를 반환하지 않는다.

응답:

```text
HTTP 200 OK
```

body:

```json
[]
```

---

### 요구사항 G — 기존 API Contract 유지

Task 003과 직접 관계없는 기존 API의 동작을 변경하지 않는다.

```text
GET /health
GET /users
GET /users/{user_id}
POST /users
DELETE /users/{user_id}
```

Task 002에서 추가된 이메일 중복 방지와 ID 충돌 방지 로직도 유지한다.

---

### 요구사항 H — README 반영

README에 새 검색 API를 간단히 추가한다.

최소 다음 내용을 포함한다.

```text
GET /users/search?email=<keyword>
```

정책:

- email query parameter 필수
- 최소 2글자
- case-insensitive 부분일치
- 검색 결과 없으면 HTTP 200 + []
```

---

## 7. 구현 방법은 강제하지 않는다

다음 사항은 Agent가 판단한다.

- 검색 로직을 어느 파일/계층에 둘지
- 검색어 Validation을 어느 계층에서 처리할지
- helper 함수를 추가할지
- route에서 직접 처리할지 service를 사용할지
- response model을 어떻게 재사용할지
- 문자열 정규화 방식을 어떻게 할지

단, 기존 프로젝트 구조를 불필요하게 크게 변경해서는 안 된다.

---

## 8. 작업 범위 제한

### 허용

- 기존 Python 코드 수정
- 필요한 작은 helper 함수 추가
- 테스트 코드 추가/수정
- README 수정
- Task 003 결과 파일 생성

### 금지

- Web Framework 교체
- Database / ORM 도입
- Docker 도입
- 인증/인가 추가
- 새로운 외부 서비스 도입
- 검색 기능과 관계없는 대규모 리팩터링
- 기존 Task 002 기능 제거 또는 재설계
- 불필요한 신규 Dependency 추가

이번 과제는 기존 Dependency만으로 해결 가능하도록 설계되어 있다.

---

## 9. 구현 전 계획 작성

Task 003에서는 **코드를 수정하기 전에 반드시 plan.md를 먼저 작성한다.**

결과 경로:

Codex:

```text
benchmark/results/task-003/codex/plan.md
```

Claude:

```text
benchmark/results/task-003/claude/plan.md
```

plan.md에는 최소 다음 내용을 작성한다.

```markdown
# Task 003 구현 계획

## 요구사항 해석

- ...

## 수정 예상 파일

- 파일명
- 수정 이유

## 설계 판단

- 검색 로직 위치
- Validation 위치
- 기존 response model 재사용 여부
- 문자열 비교 방식

## 테스트 전략

- 어떤 케이스를 테스트할 것인지

## 예상 위험

- 기존 route와의 충돌 가능성
- 기존 API 회귀 가능성
- 기타 고려사항
```

### 중요

`plan.md`를 작성한 이후 구현 과정에서 계획을 변경할 수 있다.

다만 변경한 경우 `final-response.md`에서 다음을 기록한다.

- 어떤 계획이 변경되었는지
- 왜 변경했는지

이를 통해 계획 능력과 실제 구현 판단을 함께 평가한다.

---

## 10. 테스트 요구사항

최소 다음 테스트를 실제 코드로 추가한다.

```text
1. "alice" 검색 → Alice 반환
2. "ALICE" 검색 → Alice 반환
3. "@example" 검색 → 여러 사용자 반환
4. 존재하지 않는 검색어 → HTTP 200 + []
5. 한 글자 검색어 → HTTP 400
6. 두 글자 검색어 → 정상 검색 수행
7. 기존 /users API 정상 동작
```

기존 테스트도 모두 통과해야 한다.

필요하다고 판단하면 추가 테스트를 작성해도 된다.

단, 과제 범위를 벗어난 정책을 테스트로 강제하지 않는다.

---

## 11. Route 충돌 검토

현재 다음 route가 존재한다.

```text
GET /users/{user_id}
```

새로 추가할 route:

```text
GET /users/search
```

Agent는 FastAPI route 구성 관점에서
이 두 endpoint가 안전하게 동작하는지 확인해야 한다.

필요하다면 route 선언 순서 또는 path 구조에 대한 판단을 내린다.

이 요구사항은 구현 방식 자체를 강제하지 않으며,
Agent가 기존 구조를 얼마나 정확하게 이해하는지 평가하기 위한 항목이다.

---

## 12. 실제 Repository 수정

이 과제는 코드 예시나 채팅 답변만으로 완료되지 않는다.

실제 Repository 내부 파일을 직접 수정한다.

예상되는 주요 수정 대상:

```text
app/
tests/
README.md
```

다음은 미완료로 간주한다.

- 코드 변경안을 채팅에만 출력
- 테스트를 설명만 하고 실제 파일 미작성
- README 변경안을 제안만 하고 실제 수정하지 않음
- 실제 테스트 미실행

---

## 13. 테스트 실행

구현 후 반드시 실제로 다음 명령을 실행한다.

```bash
pytest -q
```

전체 테스트가 통과해야 한다.

테스트 결과는 자신의 Agent 결과 폴더에 저장한다.

Codex:

```text
benchmark/results/task-003/codex/test-result.txt
```

Claude:

```text
benchmark/results/task-003/claude/test-result.txt
```

---

## 14. Diff 저장

baseline 대비 실제 코드 변경 내용을 저장한다.

Codex:

```text
benchmark/results/task-003/codex/diff.patch
```

Claude:

```text
benchmark/results/task-003/claude/diff.patch
```

가능하면 다음 범위만 diff 대상으로 사용한다.

```text
app/
tests/
README.md
```

결과 폴더 자체가 diff에 포함되어 patch가 불필요하게 커지지 않도록 한다.

---

## 15. 실행 메트릭 기록

이번 Task부터 실행 효율도 비교한다.

자신의 결과 폴더에 다음 파일을 생성한다.

```text
metrics.md
```

Codex:

```text
benchmark/results/task-003/codex/metrics.md
```

Claude:

```text
benchmark/results/task-003/claude/metrics.md
```

가능한 범위에서 다음을 기록한다.

```markdown
# Task 003 Execution Metrics

## 실행 정보

- Agent:
- 시작 시각:
- 종료 시각:
- 총 소요 시간:

## 변경 정보

- 수정 파일 수:
- 추가 라인 수:
- 삭제 라인 수:

## 테스트

- 테스트 실행 횟수:
- 최종 테스트 결과:

## 사용자 개입

- 추가 질문 횟수:
- 사용자 힌트 횟수:

## 비고

- 측정할 수 없는 항목:
```

정확하게 측정할 수 없는 값은 추측하지 않고
`측정 불가`라고 기록한다.

---

## 16. 최종 결과 보고서

다음 파일을 실제로 생성한다.

Codex:

```text
benchmark/results/task-003/codex/final-response.md
```

Claude:

```text
benchmark/results/task-003/claude/final-response.md
```

형식:

```markdown
# Task 003 결과

## 변경 내용

- ...

## 수정한 파일

- ...

## 테스트

- 실행 명령:
- 결과:

## 설계 판단

- 검색 로직 위치:
- Validation 위치:
- 문자열 비교 방식:
- 해당 방식을 선택한 이유:

## 계획 대비 변경 사항

- plan.md와 동일하게 구현한 부분:
- 구현 과정에서 변경한 부분:
- 변경 이유:

## Route 설계 검토

- /users/search와 /users/{user_id} 관계:
- 선택한 처리 방식:

## 남아 있는 고려사항

- ...
```

---

## 17. 최종 결과 폴더 구조

Task 종료 후 각 Agent의 결과는 다음 구조를 가진다.

```text
benchmark/results/task-003/
├── codex/
│   ├── plan.md
│   ├── final-response.md
│   ├── test-result.txt
│   ├── diff.patch
│   └── metrics.md
│
└── claude/
    ├── plan.md
    ├── final-response.md
    ├── test-result.txt
    ├── diff.patch
    └── metrics.md
```

각 Agent는 자신의 폴더만 작성한다.

---

## 18. 완료 조건

다음 조건을 모두 만족해야 완료로 인정한다.

### 계획

- 구현 전에 `plan.md`를 작성했다.

### 기능

- `/users/search` 추가
- email query parameter 사용
- 최소 2글자 validation
- case-insensitive 부분일치
- 여러 사용자 반환
- 결과 없음 → 200 + []
- 기존 API 유지

### 테스트

- 신규 테스트 실제 작성
- 기존 테스트 포함 전체 테스트 통과
- `pytest -q` 실제 실행
- `test-result.txt` 저장

### 문서

- README 반영
- `final-response.md` 작성

### 비교 자료

- `diff.patch` 저장
- `metrics.md` 저장

### 독립성

- 동일 Task 003 baseline에서 시작
- 상대 Agent 결과 폴더 접근 금지
- 사용자 추가 힌트 없이 독립 수행

---

## 19. Task 003 평가 기준

| 평가 항목 | 배점 |
|---|---:|
| 요구사항 충족 | 20 |
| 설계 적절성 | 20 |
| 코드 품질 | 15 |
| 테스트 품질 | 15 |
| 기존 구조 이해 | 10 |
| 변경 최소화 | 10 |
| 계획-구현 일관성 | 5 |
| 문서 및 설명 품질 | 5 |
| **합계** | **100** |

실행 시간은 품질 점수와 별도로 기록한다.

속도가 빠르다는 이유만으로 품질 점수를 높이지 않고,
최종 종합 분석 시 **품질 대비 효율성** 지표로 별도 활용한다.

---

## 20. 실험 핵심 질문

> 동일한 기능 추가 과제에서 Codex CLI와 Claude Code 중 어느 Agent가 기존 구조를 더 잘 이해하고, 더 적절한 설계를 선택하며, 계획과 구현을 일관되게 연결하는가?

Task 003의 결과는 향후 Planner / Coder / Tester 역할 분리에 활용한다.

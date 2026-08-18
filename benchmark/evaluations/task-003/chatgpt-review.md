# Task 003 독립 평가

## 1. 평가 대상

### 기준 문서

- `benchmark/experiment-definition.md`
- `benchmark/task-003.md`

### Codex 결과

- `benchmark/results/task-003/codex/plan.md`
- `benchmark/results/task-003/codex/final-response.md`
- `benchmark/results/task-003/codex/test-result.txt`
- `benchmark/results/task-003/codex/diff.patch`
- `benchmark/results/task-003/codex/metrics.md`

### Claude 결과

- `benchmark/results/task-003/claude/plan.md`
- `benchmark/results/task-003/claude/final-response.md`
- `benchmark/results/task-003/claude/test-result.txt`
- `benchmark/results/task-003/claude/diff.patch`
- `benchmark/results/task-003/claude/metrics.md`

평가는 `final-response.md`의 설명만이 아니라 실제 `diff.patch`, `test-result.txt`, `plan.md`, `metrics.md`를 기준으로 수행했다.

---

## 2. 평가 전제

Task 003 문서에는 중요한 불일치가 있다.

- §2는 baseline을 `benchmark/task-003-base`로 지정한다.
- §4와 §6-G는 Task 002의 이메일 중복 방지와 ID 충돌 방지 로직이 적용된 baseline을 전제로 하며, 해당 기능 유지도 요구한다.
- 실제 Codex 산출물과 Claude 산출물의 diff를 보면 baseline에는 Task 002 기능이 없었던 것으로 보인다.

이 평가에서는 다음 원칙을 적용했다.

- 검색 API 자체는 `benchmark/task-003-base` 대비 구현 결과로 평가한다.
- 그러나 Task 003 요구사항과 평가 프롬프트가 “Task 002 기능 유지”를 명시했으므로, 최종 산출물이 Task 002 기능을 포함하는지도 요구사항 충족 항목에 반영한다.
- Claude가 baseline 불일치를 명확히 발견하고 근거를 남긴 점은 계획·설명 품질에서 인정한다.
- Codex가 Task 002 기능까지 복원한 점은 요구사항 충족에서 인정하되, 변경 최소화 항목에서는 추가 변경 비용으로 함께 고려한다.

---

## 3. Task 003 점수표

| 평가 항목 | Codex | Claude | 우세 |
|---|---:|---:|---|
| 요구사항 충족 | 20/20 | 16/20 | Codex |
| 설계 적절성 | 18/20 | 19/20 | Claude |
| 코드 품질 | 14/15 | 15/15 | Claude |
| 테스트 품질 | 14/15 | 14/15 | 동점 |
| 기존 구조 이해 | 10/10 | 8/10 | Codex |
| 변경 최소화 | 8/10 | 10/10 | Claude |
| 계획-구현 일관성 | 5/5 | 5/5 | 동점 |
| 문서 및 설명 품질 | 4/5 | 5/5 | Claude |
| **총점** | **93/100** | **92/100** | **Codex** |

---

## 4. 항목별 근거

### 4.1 요구사항 충족

Codex: 20/20

- `/users/search`를 구현했고 `email` query parameter를 사용했다.
- 한 글자 검색어는 `HTTP 400`과 `Search keyword must be at least 2 characters` detail을 반환하도록 구현했다.
- `casefold()` 기반으로 case-insensitive 부분일치 검색을 구현했다.
- `@example` 검색으로 여러 사용자 반환이 가능하고, 결과 없음은 `200 []`로 처리했다.
- `/users/search`를 `/users/{user_id}`보다 먼저 선언해 실제 route 충돌을 회피했다.
- 기존 `/users` API 테스트가 유지되며, Task 002 기능인 이메일 중복 방지와 삭제 후 ID 충돌 방지도 함께 구현했다.
- README에 검색 API 정책과 사용자 생성 정책이 반영되어 있다.

Claude: 16/20

- 검색 API 요구사항 A~F와 README 반영은 충족했다.
- `email` query parameter 누락 시 FastAPI 기본 422를 사용했고, 이를 테스트로 확인했다. 요구사항은 필수 여부만 명시하고 누락 상태 코드는 명시하지 않았으므로 적절하다.
- route 충돌을 정확히 처리했다.
- 그러나 Task 003 §6-G가 요구한 “Task 002에서 추가된 이메일 중복 방지와 ID 충돌 방지 로직 유지”를 최종 코드에 반영하지 않았다. baseline 불일치를 발견하고 합리적으로 설명했지만, 결과물 기준으로는 Task 002 기능 유지 요구를 만족하지 못한다.

### 4.2 설계 적절성

Codex: 18/20

- 검색 로직을 `service.py`, HTTP validation을 `main.py`에 두어 기존 계층 구조를 따랐다.
- route 선언 순서로 `/users/search`와 `/users/{user_id}` 충돌을 해결했다.
- `list[UserResponse]`를 재사용해 불필요한 model을 만들지 않았다.
- `casefold()` helper를 검색과 이메일 중복 비교에 재사용한 점은 일관적이다.
- 다만 route 순서 의존성을 코드 주석이나 전용 테스트로 고정하지 않아 유지보수 안전성은 Claude보다 낮다.

Claude: 19/20

- 검색 로직은 `service.py`, HTTP validation은 `main.py`에 두어 역할 분리가 명확하다.
- `Query(min_length=2)`를 쓰면 422가 된다는 점을 근거로 route에서 400을 직접 반환하도록 설계한 판단이 좋다.
- route 순서 문제를 실제로 검토하고, 주석과 테스트로 고정했다.
- response model 재사용, 불필요한 model/dependency 미추가도 적절하다.
- 단, Task 002 기능 유지 요구를 baseline 해석으로 제외한 점은 전체 설계 요구 해석 관점에서 아쉽다.

### 4.3 코드 품질

Codex: 14/15

- 구현이 단순하고 읽기 쉽다.
- helper `_normalize_email()`과 `search_users_by_email()`의 책임이 명확하다.
- Task 002와 Task 003의 문자열 비교를 같은 helper로 처리해 중복이 적다.
- 아쉬운 점은 route 순서 의존성에 대한 코드 주석이 없고, `DuplicateEmailError` 클래스가 비어 있어 의도를 설명하는 정보가 적다는 점이다.

Claude: 15/15

- `MIN_SEARCH_KEYWORD_LENGTH` 상수, route 순서 주석, `search_users_by_email()` docstring이 모두 유지보수에 도움이 된다.
- 기존 route 코드를 거의 건드리지 않고 정적 route를 앞에 삽입했다.
- 요구사항 밖의 strip, 정렬, pagination을 추가하지 않은 점도 좋다.
- 코드 자체만 보면 가장 깔끔한 Task 003 검색 API 구현이다.

### 4.4 테스트 품질

Codex: 14/15

- 요구된 최소 검색 테스트를 모두 충족한다.
- `"alice"`, `"ALICE"`, `"@example"`, 결과 없음, 한 글자 400, 두 글자 정상 검색을 검증한다.
- 기존 `/users` API와 Task 002 기능 회귀 테스트도 포함했다.
- 여러 사용자 반환은 body 전체를 검증해 충분히 강하다.
- 아쉬운 점은 `email` query parameter 누락 테스트와 `/users/abc` 유지 테스트가 없고, route 순서 회귀를 직접 고정하는 테스트가 Claude보다 약하다는 점이다.

Claude: 14/15

- 요구된 최소 검색 테스트 7개를 모두 충족한다.
- `email` query parameter 누락 시 오류 위치가 `["query", "email"]`인지 확인해 route 충돌과 구분했다.
- `/users/search`가 `/users/{user_id}`에 잡히지 않고, `/users/abc`는 기존처럼 422인 점까지 확인했다.
- 신규 테스트를 baseline에 적용해 회귀 유효성을 검증한 기록도 매우 좋다.
- 다만 Task 002 기능 유지 테스트는 없다. Task 003 요구사항에 Task 002 유지가 포함되어 있으므로 이 부분은 감점한다.

### 4.5 기존 구조 이해

Codex: 10/10

- 기존 service/main 계층을 유지했다.
- 기존 response model을 재사용했다.
- route 선언 순서 문제를 plan/final에서 인지하고 실제 구현도 올바른 위치에 추가했다.
- Task 002 기능이 현재 코드에 없음을 확인하고, 요구사항 G에 맞춰 생성 안정성도 함께 보존했다.

Claude: 8/10

- route matching, FastAPI validation, service/main 역할 분리를 매우 정확히 이해했다.
- 다만 Task 002 기능 유지 요구를 baseline 불일치 때문에 제외했다. 실험 공정성 관점의 판단 근거는 훌륭하지만, Task 003 문서가 요구한 기존 기능 보존 관점에서는 일부 미충족이다.

### 4.6 변경 최소화

Codex: 8/10

- 수정 파일 수는 4개로 적절하다.
- 그러나 Task 002 기능 복원까지 포함해 검색 API만 구현한 Claude보다 변경 범위가 넓다.
- 요구사항 G를 충족하기 위한 변경으로 볼 수 있으므로 과도한 리팩터링은 아니지만, 순수 검색 기능 구현 기준으로는 더 크다.

Claude: 10/10

- 수정 파일 수 4개, 추가 162줄/삭제 1줄로 검색 API에 필요한 범위만 변경했다.
- 기존 route 코드를 수정하지 않고 새 route를 삽입했다.
- 신규 dependency와 새 파일이 없다.
- 단, 이 점수는 검색 API 구현 범위의 최소화에 대한 평가이며, Task 002 미구현 문제는 요구사항 충족과 기존 구조 이해 항목에서 감점했다.

### 4.7 계획-구현 일관성

Codex: 5/5

- 수정 예상 파일과 실제 수정 파일이 일치한다.
- 검색 로직 위치, validation 위치, response model 재사용, 문자열 비교 방식이 계획과 일치한다.
- Task 002 기능 복원도 plan에서 미리 언급했고 실제 구현했다.
- 계획 변경 없음으로 보고한 내용이 diff와 일치한다.

Claude: 5/5

- 계획이 매우 상세하며 실제 구현과 거의 완전히 일치한다.
- route 순서, validation 위치, `lower()` 사용, 테스트 9종, 수정 파일 4개가 모두 계획대로 구현되었다.
- 누락 query parameter 테스트를 강화한 변경은 final-response에서 이유를 설명했다.

### 4.8 문서 및 설명 품질

Codex: 4/5

- README에 Task 003 검색 API 정책과 Task 002 사용자 생성 정책을 반영했다.
- final-response가 요구 형식을 충족하고 계획 대비 변경 사항과 route 검토를 포함한다.
- 다만 baseline 불일치와 route 순서 의존성에 대한 설명은 Claude보다 짧다.

Claude: 5/5

- README가 검색 API, 필수 query, 400 detail, 결과 없음, route 순서 주의까지 잘 설명한다.
- final-response는 요구사항 대응표, route 설계 검토, baseline 불일치 판단, 테스트 유효성 검증까지 매우 상세하다.

---

## 5. Route 설계 검토

Codex:

- 실제 diff에서 `/users/search`가 `/users/{user_id}`보다 먼저 선언되어 있다.
- 따라서 `/users/search?email=alice`는 구조적으로 정상 route로 매칭된다.
- plan과 final-response에서도 route 충돌 가능성을 인지하고 정적 route를 먼저 선언한다고 설명했다.
- 다만 코드에 route 순서 주석이 없고, `/users/abc`가 여전히 기존처럼 422인지 검증하는 테스트도 없다.

Claude:

- 실제 diff에서 `/users/search`를 `/users/{user_id}` 앞에 선언했다.
- route 위에 선언 순서가 중요한 이유를 주석으로 남겼다.
- `test_search_route_is_not_captured_by_the_user_id_route`에서 `/users/search`가 200이고 `/users/abc`는 422인 점을 함께 확인했다.
- route 설계 검토는 Claude가 더 강하다.

---

## 6. 실행 효율성 비교

| 지표 | Codex | Claude | 우세 |
|---|---:|---:|---|
| 총 소요 시간 | 측정 불가 | 약 6분 | 판단 보류 |
| 수정 파일 수 | 4 | 4 | 동점 |
| 추가 라인 수 | 163 | 162 | Claude |
| 삭제 라인 수 | 6 | 1 | Claude |
| 테스트 실행 횟수 | 2 | 7 | Codex |
| 사용자 추가 질문 | 0 | 0 | 동점 |
| 사용자 힌트 | 0 | 0 | 동점 |

실행 시간은 Codex가 측정 불가이므로 직접 비교하지 않는다.

변경량은 거의 동일하지만, Codex는 Task 002 기능까지 포함하고도 Claude와 비슷한 추가 라인 수를 기록했다. 테스트 실행 횟수는 Codex가 적다. Claude는 테스트 실행 횟수가 많지만, 그중 일부는 회귀 유효성 검증과 테스트 단언 강화에 사용되어 품질 향상 목적이 있었다.

품질 대비 실행 효율은 **Codex 우세**로 판단한다. 이유는 최종 점수가 근소하게 높고, 측정 가능한 변경량이 유사하며, 테스트 실행 횟수가 더 적기 때문이다. 다만 Codex 총 소요 시간이 측정 불가이므로 이 판단은 벽시계 시간 기준이 아니라 “변경 비용과 테스트 실행 횟수 대비 품질” 기준이다.

---

## 7. Agent별 분석

### 7.1 Codex

강점:

- Task 003 검색 API와 Task 002 기능 유지 요구를 모두 최종 코드에 반영했다.
- 구현이 간결하고 service/main 계층 분리가 적절하다.
- `casefold()`를 재사용해 검색과 이메일 중복 비교를 일관되게 처리했다.
- 계획과 구현이 잘 일치한다.

약점:

- route 순서 의존성을 코드 주석이나 전용 route 회귀 테스트로 충분히 고정하지 않았다.
- `email` query parameter 누락 케이스를 테스트하지 않았다.
- 설명과 README는 요구를 충족하지만 Claude보다 덜 상세하다.

설계 특징:

- service에 검색 로직을 두고 route에서 HTTP validation을 처리한다.
- Task 002 기능 복원을 같은 service 계층에서 함께 처리한다.
- `/users/search`를 동적 route보다 먼저 선언한다.

테스트 특징:

- 최소 검색 요구사항과 Task 002 회귀 테스트를 모두 포함한다.
- body 검증이 비교적 강하다.
- route collision의 세부 회귀와 query 누락 테스트는 부족하다.

계획 수행 특징:

- plan.md에서 예상한 파일, 설계, 테스트 전략을 그대로 수행했다.
- 계획 변경 없음으로 보고했고 실제 diff와 모순되지 않는다.

### 7.2 Claude

강점:

- route 충돌 문제를 가장 정확히 분석하고 코드 주석과 테스트로 고정했다.
- `Query(min_length=2)`가 422를 반환한다는 점을 피하고 400을 직접 구현한 설계 판단이 좋다.
- 테스트가 촘촘하며 query parameter 누락과 `/users/abc` 기존 동작까지 확인한다.
- plan.md와 final-response의 설명 품질이 매우 높다.

약점:

- Task 002 기능 유지 요구를 최종 코드에 반영하지 않았다.
- baseline 불일치 판단은 근거가 있지만, Task 003 요구사항 전체를 결과물 기준으로 보면 이메일 중복 방지와 ID 충돌 방지가 빠져 있다.
- 테스트 품질은 높지만 Task 002 유지 테스트가 없다.

설계 특징:

- 검색 API만 최소 구현했다.
- `MIN_SEARCH_KEYWORD_LENGTH` 상수와 route 순서 주석을 추가했다.
- `lower()` 기반 부분일치 검색을 사용하고, 요구사항 밖 정책을 추가하지 않았다.

테스트 특징:

- 최소 요구 테스트 7개에 더해 query 누락과 route 충돌 회귀를 테스트했다.
- 신규 테스트의 baseline 실패 여부까지 검증했다.
- Task 002 기능 유지 검증은 없다.

계획 수행 특징:

- 계획이 매우 상세하고 실제 구현과 일치한다.
- 구현 중 테스트 단언 강화라는 변경 사항을 final-response에 명확히 기록했다.
- baseline 불일치에 대한 판단 근거를 매우 상세히 남겼다.

---

## 8. 직접 비교

1. 요구사항을 더 정확히 이해한 Agent:
   - **Codex**. 검색 API뿐 아니라 Task 002 기능 유지 요구까지 최종 코드에 반영했다.

2. 기존 코드 구조를 더 잘 활용한 Agent:
   - **동점**. 둘 다 service/main 계층과 `UserResponse` 재사용을 잘 지켰다. route matching 세부 이해는 Claude가 더 강하다.

3. 설계가 더 단순하고 적절한 Agent:
   - **Claude**. 검색 API 구현만 보면 더 명확하고 주석/상수/테스트 설계가 좋다. 단, Task 002 요구 충족은 Codex가 낫다.

4. 테스트 품질이 더 높은 Agent:
   - **동점에 가깝지만 Claude 근소 우세**. Claude는 route collision과 query 누락까지 검증한다. Codex는 Task 002 회귀를 포함한다. 전체 요구 범위까지 보면 동점으로 처리했다.

5. 계획을 더 잘 세운 Agent:
   - **Claude**. baseline 불일치와 route collision을 구현 전 계획에서 더 상세히 분석했다.

6. 계획과 구현의 일관성이 더 높은 Agent:
   - **동점**. 둘 다 계획과 구현이 일치한다.

7. 불필요한 변경이 더 적은 Agent:
   - **Claude**. 검색 API만 최소 변경했다.

8. 최종 결과물을 유지보수하기 쉬운 Agent:
   - **동점**. Claude는 route 주석과 테스트가 강하고, Codex는 Task 002 기능까지 포함해 기능 완결성이 좋다.

9. 같은 품질 수준을 기준으로 더 효율적인 Agent:
   - **Codex**. 최종 품질이 근소하게 높고, 측정 가능한 변경량은 유사하며 테스트 실행 횟수는 적다. 단, 총 소요 시간은 비교 불가다.

10. Task 003 전체 우세 Agent:
   - **Codex**. 점수 차이는 작지만, Task 003 명시 요구사항 중 Task 002 기능 유지까지 충족한 점을 더 높게 평가했다.

---

## 9. Task 001~003 관점의 잠정 역할 판단

| 역할 | 현재 우세 Agent | Task 003에서 얻은 새로운 근거 | 확신도 |
|---|---|---|---|
| Planner | Claude | Task 003 plan이 baseline 불일치, route collision, validation 대안까지 더 체계적으로 다뤘다. | 중간 |
| Coder | Codex | Task 003에서 최종 요구사항 전체를 더 완결적으로 반영했다. 다만 검색 API 단독 구현은 Claude도 우수하다. | 낮음 |
| Tester | Claude | route collision, query 누락, baseline 회귀 유효성까지 확인했다. 단 Task 002 유지 테스트 누락은 감점이다. | 중간 |
| Reviewer | Claude | 위험 분석과 route 설계 검토가 더 깊다. | 중간 |
| Debugger | 판단 보류 | Task 003은 기능 추가 과제라 디버깅 능력을 독립적으로 판단하기 어렵다. | 낮음 |
| Technical Writer | Claude | final-response, README, plan 설명 품질이 더 높다. | 중간 |
| Researcher | Claude | FastAPI route/validation 동작과 baseline 불일치 근거를 더 자세히 기록했다. | 중간 |

---

## 10. 최종 결론

- Codex Task 003 총점: **93/100**
- Claude Task 003 총점: **92/100**
- Task 003 우세 Agent: **Codex**

우세하다고 판단한 핵심 이유:

- Codex는 검색 API 요구사항뿐 아니라 Task 003 문서가 명시한 Task 002 기능 유지까지 최종 코드에 반영했다.
- Claude는 baseline 불일치를 근거 있게 해석했지만, 결과물 기준으로는 이메일 중복 방지와 삭제 후 ID 충돌 방지 로직이 없다.

상대 Agent가 더 잘한 부분:

- Claude는 route 충돌 검토, query parameter 누락 테스트, baseline 회귀 유효성 검증, plan/final-response 설명에서 Codex보다 우수했다.
- 검색 API만 놓고 보면 Claude 구현은 더 작고 유지보수 친화적이다.

품질 차이가 실질적으로 큰지 작은지:

- **작다.** 둘 다 검색 API의 핵심 기능은 통과했고, 테스트도 15개 모두 통과했다.
- 차이는 Task 002 유지 요구를 엄격히 반영하느냐, baseline 브랜치 해석을 우선하느냐에서 발생했다.

실행 속도 및 효율성 차이:

- Codex 총 소요 시간은 측정 불가, Claude는 약 6분으로 기록되어 직접 시간 비교는 불가능하다.
- 수정 파일 수는 동일하고 추가 라인 수는 거의 같다.
- 테스트 실행 횟수는 Codex 2회, Claude 7회다.
- 품질 대비 실행 효율은 **Codex 우세**로 판단한다.

Planner 역할에 대한 새로운 판단:

- **Claude 우세**가 강화되었다. 계획 단계에서 route 충돌, validation 방식, baseline 불일치를 더 깊게 분석했다.

Coder 역할에 대한 새로운 판단:

- **Codex 근소 우세**로 잠정 판단한다. 최종 요구사항 전체를 더 완결적으로 반영했다.

Tester 역할에 대한 새로운 판단:

- **Claude 우세**로 잠정 판단한다. route collision과 query 누락, baseline 회귀 유효성 검증이 강했다. 다만 Task 002 유지 테스트 누락 때문에 압도적 우세는 아니다.

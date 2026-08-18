# Task 003 결과

- Agent 식별자: `claude`
- Baseline: `benchmark/task-003-base` (51a7886)
- 작업 Branch: `experiment/claude-task-003`
- 변경 규모: 4 files changed, 162 insertions(+), 1 deletion(-)
- 최종 테스트: `15 passed` (기존 6 + 신규 9)

---

## 변경 내용

### 1. 검색 API 추가 — `GET /users/search?email=<keyword>`

- `app/service.py`에 `search_users_by_email(keyword) -> list[dict]`를 추가했다.
  대소문자를 무시하는 부분일치(substring) 검사로 사용자를 걸러 반환한다.
- `app/main.py`에 `GET /users/search` route를 추가했다.
  **`GET /users/{user_id}`보다 먼저 선언**했다 (아래 "Route 설계 검토" 참조).
- 응답 모델은 기존 `list[UserResponse]`를 그대로 재사용했다. `app/models.py`는 수정하지 않았다.

### 2. 최소 검색어 길이 검증

- route에서 `len(email) < 2`를 검사하고
  `HTTP 400` + `detail: "Search keyword must be at least 2 characters"`를 반환한다.
- 상수 `MIN_SEARCH_KEYWORD_LENGTH = 2`를 두고 detail 문자열도 이 값에서 생성해
  숫자가 두 곳에 중복되지 않게 했다.

### 3. 요구사항 대응 요약

| 요구 | 구현 | 검증 테스트 |
|---|---|---|
| A. `email` query parameter 필수 | 기본값 없는 인자로 선언 → 누락 시 422 | `..._requires_the_email_parameter` |
| B. 최소 2글자, 위반 시 400 + 지정 detail | route에서 명시 검증 후 `HTTPException(400)` | `..._rejects_short_keyword`, `..._accepts_two_character_keyword` |
| C. 부분일치 | `normalized in user["email"].lower()` | `..._returns_matching_user` |
| D. 대소문자 무시 | 양쪽 `lower()` 정규화 | `..._is_case_insensitive` |
| E. 여러 사용자 반환 | 조건 만족 전부 반환, 저장 순서 유지 | `..._returns_every_match` |
| F. 결과 없음 → 200 + `[]` | 빈 리스트 그대로 반환 | `..._returns_empty_list_when_no_match` |
| G. 기존 contract 유지 | 기존 route 코드 무수정, 선언 위치만 앞에 삽입 | `..._existing_user_endpoints_are_unchanged_by_search`, `..._not_captured_by_the_user_id_route` |
| H. README 반영 | `## 사용자 검색 API` 섹션 추가 | — |

---

## 수정한 파일

| 파일 | 추가/삭제 | 변경 |
|---|---:|---|
| `app/service.py` | +16 / 0 | `search_users_by_email()` 추가 |
| `app/main.py` | +28 / -1 | `/users/search` route 추가, import 확장 (삭제 1줄은 import 한 줄 → 여러 줄 변환) |
| `tests/test_users.py` | +87 / 0 | 신규 테스트 9종 추가 (기존 테스트 무수정) |
| `README.md` | +31 / 0 | 검색 API 섹션 추가 |

**수정하지 않은 파일**: `app/__init__.py`, `app/models.py`, `app/store.py`,
`tests/conftest.py`, `tests/test_health.py`, `requirements.txt`.
신규 파일 생성 0건, 신규 Dependency 0건, 기존 route 코드 수정 0줄.

---

## 테스트

- **실행 명령**: `pytest -q`
- **결과**: `15 passed` (기존 6 + 신규 9, 실패 0)
- 전체 출력과 테스트 목록은 같은 디렉터리의 `test-result.txt`에 있다.

### 신규 테스트 9종

| # | 테스트 | 대응 요구 |
|---|---|---|
| 1 | `..._returns_matching_user` | §10-1 `alice` 검색 |
| 2 | `..._is_case_insensitive` | §10-2 `ALICE` 검색 |
| 3 | `..._returns_every_match` | §10-3 `@example` 다건 |
| 4 | `..._returns_empty_list_when_no_match` | §10-4 200 + `[]` |
| 5 | `..._rejects_short_keyword` | §10-5 한 글자 → 400 |
| 6 | `..._accepts_two_character_keyword` | §10-6 두 글자 경계값 |
| 7 | `..._existing_user_endpoints_are_unchanged_by_search` | §10-7 기존 API |
| 8 | `..._search_route_is_not_captured_by_the_user_id_route` | 추가 — route 순서 고정 |
| 9 | `..._requires_the_email_parameter` | 추가 — 요구 A |

5번은 상태 코드뿐 아니라 `detail` 문자열까지 정확히 단언한다. 요구사항이 문자열을 지정했기 때문이다.

### 회귀 유효성 검증

신규 테스트가 실제로 무언가를 잡는지 확인하기 위해, **신규 테스트만 baseline `app/` 코드에 적용**해
실행했다.

```text
8 failed, 7 passed
```

9종 중 8종이 baseline에서 실패한다. 나머지 1종
(`..._existing_user_endpoints_are_unchanged_by_search`)은 기존 동작 보존을 확인하는 테스트이므로
baseline에서도 통과하는 것이 정상이다.

---

## 설계 판단

### 검색 로직 위치 — `app/service.py`

기존 구조가 이미 계층을 나누고 있다. `app/main.py`는 HTTP만 다루고(`HTTPException`을 던지는 곳은
`main.py`뿐), 데이터 접근은 전부 `app/service.py`가 담당한다(`list_users`, `get_user`,
`create_user`, `delete_user`). 검색도 데이터 조회이므로 같은 자리에 두었다.
route에서 `get_users()`를 직접 순회하면 이 분리가 깨진다.

### Validation 위치 — route (`app/main.py`)

최소 길이 검증을 route에서 수행하고 `HTTPException(400)`을 던진다.

**`Query(min_length=2)`를 쓰지 않은 것이 핵심 판단이다.** pydantic 검증 실패는 FastAPI가
`RequestValidationError`로 처리해 **422**를 반환한다. 요구사항 B가 지정한 **400**과 다르다.
따라서 프레임워크 검증에 위임할 수 없고 명시적으로 검사해야 한다.

route를 택한 이유는 세 가지다.

1. 요구된 결과가 HTTP 400이라는 전송 계층 개념이다. service는 HTTP를 모르는 것이 기존 규약이다.
2. `main.py`가 이미 같은 방식으로 404를 던지고 있다. 새 패턴을 만들지 않았다.
3. `search_users_by_email()`을 순수 함수로 유지하면 다른 호출자가 재사용할 수 있다.

검토했으나 채택하지 않은 대안: service에서 도메인 예외를 던지고 main에서 400으로 변환하는 방식.
이메일 중복과 달리 최소 길이는 **저장소 불변식이 아니라 입력 정책**이라 예외 클래스를 새로 만들
근거가 약하다고 판단했다.

### 문자열 비교 방식 — `lower()` 기반 substring

```python
normalized = keyword.lower()
[u for u in get_users().values() if normalized in u["email"].lower()]
```

- `casefold()`가 아니라 `lower()`를 썼다. `casefold()`는 유니코드 폴딩이 더 공격적이라
  (예: `ß` → `ss`) 서로 다른 이메일 주소를 같다고 볼 수 있다. 이메일에는 `lower()`가 안전하다.
- **저장된 이메일 값은 변경하지 않는다.** 정규화는 비교 시에만 적용한다.
- 정렬을 추가하지 않고 저장 순서를 유지했다. 요구사항 E가 "반환 순서에 대한 새로운 정렬 규칙은
  요구하지 않는다"고 명시했기 때문이다.

### 요구되지 않아 넣지 않은 것

- 검색어 앞뒤 공백 `strip`: 길이 검사는 원본 문자열 길이로 한다.
  §10이 "과제 범위를 벗어난 정책을 테스트로 강제하지 않는다"고 하므로 임의 정책을 만들지 않았다.
- 결과 정렬, 최대 길이 제한, 페이지네이션, `name` 검색 확장: 요구 없음.

---

## 계획 대비 변경 사항

### plan.md와 동일하게 구현한 부분

계획의 설계 판단은 **전부 그대로 구현했다.**

- 검색 로직 → `app/service.py` (계획 §3.2 그대로)
- Validation → route, `HTTPException(400)` (계획 §3.3 그대로)
- `/users/search`를 `/users/{user_id}` 앞에 선언 (계획 §3.1 대안 A 그대로)
- `list[UserResponse]` 재사용, `app/models.py` 무수정 (계획 §3.4 그대로)
- `lower()` 기반 substring, 저장 값 불변 (계획 §3.5 그대로)
- 수정 파일 4개 예측 → 실제 4개 일치 (계획 §2 그대로)
- 테스트 9종 구성 → 그대로 구현 (계획 §4 그대로)

### 구현 과정에서 변경한 부분

**변경 1건.** 계획 §4의 9번 테스트(`email` 파라미터 누락 → 422)를 강화했다.

- 계획: `assert response.status_code == 422` 만 확인
- 실제: 여기에 더해 오류 위치가 `["query", "email"]`인지 단언

**변경 이유**: 회귀 유효성 검증(테스트 실행 3회차)에서 이 테스트가 **baseline에서도 통과**한다는
것을 발견했다. baseline에서는 `/users/search`가 `/users/{user_id}`에 잡혀 int 파싱 실패로
422를 내기 때문에, 상태 코드만 보면 "우연히 같은 값"이라 검색 API의 동작을 전혀 검증하지 못한다.
오류 위치까지 단언하도록 바꾼 뒤 baseline 실패 수가 7 → 8로 늘어 회귀 테스트로서 유효해졌다.

이 외에 계획 변경은 없다. 구현 중 테스트 실패로 인한 코드 수정도 0회였다.

### 계획 단계에서 미리 해소한 위험

계획 §0에 기록한 baseline 불일치가 실제 문제였고, 착수 전에 확인해 둔 덕분에 구현 중 혼선이 없었다.

`benchmark/task-003.md` §2는 baseline을 `benchmark/task-003-base`로 지정하는데,
§4는 "Task 002 개선이 **적용된** baseline"이라 서술하고 §6-G는 "Task 002 로직도 유지"를 요구한다.
그러나 실제 commit을 확인하면 다음과 같다.

```text
benchmark/task-003-base = 51a7886 -> app/service.py 에 new_id = len(users) + 1
                                      이메일 중복 검사 없음 => Task 002 미적용
experiment/codex-task-003 = 4accc85 -> app/tests/README 트리가 위와 동일
```

**§2를 따랐다.** 근거는 세 가지다.

1. §2는 브랜치를 명시한 유일한 실행 지시이고 §4·§6-G는 배경 서술이다.
2. 상대 Agent의 branch가 가리키는 트리도 동일하므로, 이 baseline을 쓰는 것이 두 Agent의
   출발점을 같게 만드는 유일한 선택이다. 여기서 Task 002를 임의로 재구현하면 출발점이 달라져
   비교 실험이 무효가 된다.
3. §8이 "검색 기능과 관계없는 대규모 리팩터링"을 금지한다. Task 002 재구현은 Task 003 범위 밖이다.

따라서 §6-G는 **"baseline에 존재하는 기존 동작을 깨뜨리지 않는다"**로 해석해 이행했다.
`POST /users`를 포함한 기존 5개 엔드포인트의 코드를 한 줄도 수정하지 않았고,
기존 테스트 6종이 전부 통과한다.

---

## Route 설계 검토

### `/users/search`와 `/users/{user_id}`의 관계 — 실측 확인

구현 전에 baseline 앱에 직접 요청해 확인했다.

```text
기존 앱에 GET /users/search?email=alice  ->  422
  detail: type=int_parsing, loc=["path","user_id"], input="search"
```

`/users/{user_id}`가 `search`를 `user_id`로 받으려다 int 변환에 실패한다.
**404도 아니고 요구된 200도 아닌 422**가 나온다. 즉 route를 그냥 추가하면
선언 위치에 따라 조용히 깨지는 구조다.

FastAPI(Starlette)는 route를 **선언 순서대로 먼저 매칭되는 것**에 배정한다.

### 선택한 처리 방식 — `/users/search`를 앞에 선언

```python
# app/main.py
@app.get("/users", ...)                    # 기존
@app.get("/users/search", ...)             # 신규 — 여기에 삽입
@app.get("/users/{user_id}", ...)          # 기존 (코드 무수정)
```

검토한 대안:

| 대안 | 판단 |
|---|---|
| **A. `/users/search`를 앞에 선언** ← 채택 | 기존 route 코드 수정 0줄. 요구된 경로 그대로 유지 |
| B. 경로를 `/search/users` 등으로 변경 | §5가 `GET /users/search`를 명시했다. 위반 |
| C. `/users/{user_id}`를 `str`로 받고 분기 | 기존 route 수정 필요. `/users/abc` → 422 동작이 깨져 요구 G 위반 |
| D. `APIRouter` 분리 | 파일 구조 변경. §7의 "기존 구조를 불필요하게 크게 변경 금지"에 저촉 |

### 순서 의존성을 코드와 테스트로 고정

A안의 약점은 **선언 순서에 암묵적으로 결합된다는 것**이다. 누군가 route를 재배열하면 조용히 깨진다.
두 가지로 방어했다.

1. route 위에 이유를 명시한 주석을 남겼다.

```python
# NOTE:
# This route must stay declared BEFORE "/users/{user_id}".
# FastAPI matches routes in declaration order, so if "/users/{user_id}" came
# first it would capture "/users/search" and fail to parse "search" as an int.
```

2. `test_search_route_is_not_captured_by_the_user_id_route`가 이 결합을 고정한다.
   `/users/search`가 200을 반환하는 것과, `/users/abc`는 **여전히 422**라는 것을 함께 단언한다.
   후자는 `search`만 특수하게 처리되었을 뿐 route 테이블이 그대로임을 보인다.

---

## 남아 있는 고려사항

1. **Validation 우회 경로.** 최소 길이 검증이 route에 있으므로 `search_users_by_email()`을
   직접 호출하면 길이 제한이 적용되지 않는다. 현재 호출자가 route뿐이라 허용 가능하다고 보았으나,
   다른 호출자가 생기면 검증을 service로 옮기거나 양쪽에 두어야 한다.
2. **검색어 공백 처리.** `email=%20%20`(공백 2개)은 길이 2를 통과해 검색을 수행하고 `200 []`을
   반환한다. 요구사항이 규정하지 않아 의도적으로 정책을 만들지 않았다. 정책이 필요하면
   `strip()` 후 길이를 검사하도록 한 줄만 바꾸면 된다.
3. **선형 탐색.** `search_users_by_email()`은 O(n)이다. 현재 in-memory 소규모 저장소에서는
   충분하지만, 사용자 수가 커지면 인덱스나 실제 검색 엔진이 필요하다.
4. **부분일치의 의미.** 현재는 단순 substring이다. `alice`로 검색하면 `notalice@x.com`도 잡힌다.
   요구사항 C가 "부분 문자열이 포함되면"이라고 명시했으므로 의도한 동작이지만,
   실제 서비스라면 prefix 매칭이나 도메인/로컬파트 구분 검색이 더 적절할 수 있다.
5. **Task 002 기능 부재.** 위 "계획 대비 변경 사항"에서 설명했듯 baseline에 이메일 중복 방지와
   ID 충돌 방지가 없다. 이 Repository를 계속 쓸 예정이라면 Task 002 결과를 baseline에 반영한 뒤
   Task 004를 진행하는 편이 문서 서술과 실제 코드의 불일치를 없앤다.
6. **응답 개수 제한 없음.** 사용자가 많고 검색어가 짧으면 전체에 가까운 목록이 반환된다.
   요구사항에 페이지네이션이 없어 넣지 않았다.
7. **테스트 실행 환경.** 로컬 머신에 `fastapi`/`pytest`가 없고 네트워크 접근이 불가해,
   파일 sha256 일치를 검증한 별도 환경에서 `pytest -q`를 실행했다. 자세한 내용은
   `test-result.txt`와 `metrics.md`에 기록했다.

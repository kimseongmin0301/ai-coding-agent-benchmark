# Task 003 구현 계획

- Agent 식별자: `claude`
- 작성 시각: 2026-08-18 13:37 KST (구현 착수 전)
- Baseline: `benchmark/task-003-base` (51a7886)
- 작업 Branch: `experiment/claude-task-003`

---

## 0. Baseline 확정 근거 (착수 전 확인 사항)

`task-003.md`의 서술 사이에 불일치가 있어 착수 전에 사실을 확인했다.

| 문서 위치 | 서술 |
|---|---|
| §2 공통 실행 환경 | baseline은 `benchmark/task-003-base` 브랜치가 가리키는 commit |
| §4 현재 Repository | "Task 002에서 사용자 생성 안정성 개선이 **적용된** baseline을 사용한다" |
| §6-G | "Task 002에서 추가된 이메일 중복 방지와 ID 충돌 방지 로직도 유지한다" |

실제 commit을 확인한 결과는 다음과 같다.

```text
benchmark/task-003-base = 51a7886  -> app/service.py 에 `new_id = len(users) + 1`
                                       이메일 중복 검사 없음  => Task 002 미적용
benchmark-base          = 4accc85  -> 동일 (task-003 문서 2개만 추가된 commit)
experiment/codex-task-003 = 4accc85 -> app/tests/README 트리가 위와 동일
```

즉 **§2가 지정한 baseline 코드에는 Task 002 기능이 들어 있지 않다.** §4·§6-G의 서술과 어긋난다.

**판단: §2를 따른다.** 근거는 세 가지다.

1. §2는 브랜치 이름을 명시한 유일한 실행 지시이고, §4·§6-G는 배경 서술이다.
2. `experiment/codex-task-003` 브랜치가 가리키는 트리도 동일하므로, 이 baseline을 쓰는 것이
   두 Agent의 출발점을 같게 만드는 유일한 선택이다. 여기서 Task 002를 임의로 다시 구현하면
   상대 Agent와 출발점이 달라져 비교 실험 자체가 무효가 된다.
3. §8이 "검색 기능과 관계없는 대규모 리팩터링"을 금지한다. Task 002 재구현은 Task 003 범위 밖이다.

따라서 §6-G는 **"baseline에 존재하는 기존 동작을 깨뜨리지 않는다"**로 해석해 이행한다.
baseline에 Task 002 기능이 없으므로 보존할 대상도 없다. 이 판단은 `final-response.md`에 다시 기록한다.

착수 전 baseline 복구를 수행했고(`app/`, `tests/`, `README.md`),
`git diff benchmark/task-003-base -- app tests README.md`가 비어 있음과
`pytest -q` → `6 passed`를 확인했다.

---

## 1. 요구사항 해석

| 요구 | 해석 | 판단이 필요한 지점 |
|---|---|---|
| A. query parameter `email` 필수 | FastAPI에서 기본값 없는 비-path 스칼라 인자는 필수 query parameter가 된다. 누락 시 FastAPI 기본 동작인 422 | 누락 시 상태 코드는 명세되지 않음 → FastAPI 기본값 유지 |
| B. 최소 2글자, 위반 시 **400** + `Search keyword must be at least 2 characters` | **`Query(min_length=2)`를 쓰면 안 된다.** pydantic 검증 실패는 422를 반환하므로 요구된 400과 다르다 | 명시적 길이 검사 후 `HTTPException(400)` 필요 |
| C. 부분일치 | `keyword in email` 형태의 substring 포함 검사 | — |
| D. 대소문자 무시 | 양쪽을 `lower()`로 정규화 후 비교 | 저장 값은 변경하지 않음 |
| E. 여러 사용자 반환 | 조건을 만족하는 전부 반환. "반환 순서에 대한 새로운 정렬 규칙은 요구하지 않는다" | 정렬 추가하지 않고 기존 저장 순서 유지 |
| F. 결과 없음 | 404가 아니라 `200 []` | 빈 리스트를 그대로 반환하면 충족 |
| G. 기존 contract 유지 | 기존 5개 엔드포인트 동작 불변 | **route 순서 문제가 여기에 걸린다 (§3)** |
| H. README 반영 | 검색 API와 4개 정책 기재 | — |

명세되지 않아 **정책을 새로 만들지 않기로 한 것**:

- 검색어 앞뒤 공백 `strip` 여부 → **하지 않는다.** 길이 검사는 원본 문자열 길이로 수행한다.
  §10이 "과제 범위를 벗어난 정책을 테스트로 강제하지 않는다"고 하므로 임의 정책을 넣지 않는다.
- 결과 정렬 → 추가하지 않는다 (E가 명시적으로 요구하지 않음).
- 최대 길이 제한, 페이지네이션 → 요구 없음. 추가하지 않는다.

---

## 2. 수정 예상 파일

| 파일 | 수정 이유 | 예상 규모 |
|---|---|---|
| `app/service.py` | 검색 로직 `search_users_by_email()` 추가 | 함수 1개 |
| `app/main.py` | `GET /users/search` route 추가 + **`/users/{user_id}` 앞에 배치** + 길이 검증 | route 1개 |
| `tests/test_users.py` | 신규 테스트 추가 (§10의 7종 + 구조 회귀 2종) | 함수 9개 |
| `README.md` | 검색 API 및 정책 기재 | 섹션 1개 |

**수정하지 않을 파일**: `app/models.py`(기존 `UserResponse` 재사용), `app/store.py`,
`tests/conftest.py`, `tests/test_health.py`, `requirements.txt`.
신규 파일 생성 없음. 신규 Dependency 없음.

---

## 3. 설계 판단

### 3.1 Route 설계 — /users/search 와 /users/{user_id} (§11)

**착수 전 실측으로 확인한 사실이다.**

baseline 앱에 `/users/search?email=alice`를 요청해 보았다.

```text
기존 앱에 /users/search 요청 -> 422
  detail: int_parsing / loc: ["path","user_id"] / input: "search"
```

즉 `/users/{user_id}`가 `search`를 `user_id`로 받으려다 int 변환에 실패한다.
**404도 아니고 요구된 200도 아닌 422가 나온다.**

FastAPI(Starlette)는 route를 **선언 순서대로 먼저 매칭되는 것**에 배정한다.
따라서 해결책은 `/users/search`를 `/users/{user_id}`보다 **먼저 선언**하는 것이다.

검토한 대안:

| 대안 | 판단 |
|---|---|
| **A. `/users/search`를 `/users/{user_id}` 앞에 선언** ← 채택 | 코드 이동 없이 삽입 위치만 정하면 된다. 기존 route 수정 0줄. 요구된 경로를 그대로 유지 |
| B. 경로를 `/users/search/`나 `/search/users`로 변경 | 요구사항 §5가 `GET /users/search`를 명시했다. 위반 |
| C. `/users/{user_id}`의 타입을 `str`로 바꾸고 분기 | 기존 route를 수정해야 하고 `/users/abc` → 422 동작이 깨진다. 요구사항 G 위반 |
| D. APIRouter 분리 | 파일 구조 변경. §7의 "기존 구조를 불필요하게 크게 변경 금지"에 저촉 |

**A를 채택한다.** 이 선택은 "선언 순서에 의존한다"는 암묵적 결합을 만들므로,
누군가 route를 재배열하면 조용히 깨진다. 따라서 **순서 의존성을 고정하는 테스트를 반드시 추가한다** (§4).

### 3.2 검색 로직 위치 — service 계층

`app/service.py`에 `search_users_by_email(keyword) -> list[dict]`를 둔다.

근거: 기존 구조가 이미 그렇게 되어 있다. `main.py`는 HTTP만 다루고
(`HTTPException` 404를 던지는 곳은 `main.py`뿐), 데이터 접근은 전부 `service.py`가 담당한다
(`list_users`, `get_user`, `create_user`, `delete_user`). 검색도 데이터 조회이므로 같은 자리에 둔다.
route에서 직접 `get_users()`를 순회하면 이 분리가 깨진다.

### 3.3 Validation 위치 — route(main.py)

최소 길이 검증은 `main.py`의 route 함수에서 수행하고 `HTTPException(400)`을 던진다.

근거:

1. 요구된 결과가 **HTTP 400**이라는 전송 계층 개념이다. service는 HTTP를 모르는 것이 기존 규약이다.
2. `main.py`가 이미 동일한 방식으로 404를 던지고 있다. 새 패턴을 만들지 않는다.
3. `search_users_by_email()`을 순수 함수로 두면 다른 호출자가 재사용할 수 있다.

검토한 대안:

| 대안 | 판단 |
|---|---|
| `Query(min_length=2)` | **불가.** 422를 반환하므로 요구된 400과 다르다 (실측 근거 §3.1의 422 동작과 동일 메커니즘) |
| service에서 도메인 예외 → main에서 400 변환 | Task 002의 이메일 중복과 달리 이것은 **저장소 불변식이 아니라 입력 정책**이다. 예외 클래스를 새로 만들 만한 이유가 약하다 |
| **route에서 직접 검증** ← 채택 | 가장 적은 코드로 요구 동작을 정확히 만족. 기존 스타일과 일치 |

이 판단의 약점: 검증이 route에 있으므로 `search_users_by_email()`을 직접 호출하면 길이 제한이 우회된다.
현재 호출자가 route뿐이므로 허용 가능하다고 본다. `final-response.md`에 한계로 기록한다.

### 3.4 기존 response model 재사용

`list[UserResponse]`를 그대로 재사용한다. `GET /users`와 동일한 응답 형태이므로
새 모델을 만들 이유가 없다. `app/models.py`는 수정하지 않는다.

### 3.5 문자열 비교 방식

```python
keyword.lower() in user["email"].lower()
```

- `casefold()`가 아니라 `lower()`를 쓴다. `casefold()`는 유니코드 폴딩이 더 공격적이어서
  (예: `ß` → `ss`) 서로 다른 이메일 주소를 같다고 볼 수 있다. 이메일에는 `lower()`가 안전하다.
- 저장된 이메일 값은 변경하지 않는다. 정규화는 **비교 시에만** 적용한다.

---

## 4. 테스트 전략

`tests/test_users.py`에 추가한다. §10이 요구한 7종을 모두 작성하고, 구조 회귀 2종을 더한다.

| # | 테스트 | 검증 대상 | §10 대응 |
|---|---|---|---|
| 1 | `alice` 검색 → Alice 1건 | 요구 C | 1 |
| 2 | `ALICE` 검색 → 1과 동일 결과 | 요구 D | 2 |
| 3 | `@example` 검색 → 2건 전부 | 요구 E | 3 |
| 4 | 없는 검색어 → `200` + `[]` | 요구 F (404 아님을 명시 단언) | 4 |
| 5 | 한 글자 → `400` + detail 문자열 일치 | 요구 B | 5 |
| 6 | 두 글자 → 200, 정상 검색 수행 | 요구 B 경계값 | 6 |
| 7 | 기존 `/users`, `/users/{id}`, 404, `/health` 정상 | 요구 G | 7 |
| 8 | `/users/search`가 `/users/{user_id}`에 잡히지 않음 + `/users/abc`는 여전히 422 | **§3.1 순서 의존성 고정** | 추가 |
| 9 | `email` 파라미터 누락 → 422 | 요구 A | 추가 |

- 5번은 상태 코드만이 아니라 `detail` 문자열까지 정확히 단언한다. 요구사항이 문자열을 명시했기 때문이다.
- 8번이 이번 과제에서 가장 중요한 테스트다. 3.1의 결합을 명시적으로 고정한다.
- 검증 절차로 **신규 테스트를 baseline 코드에 적용해 실제로 실패하는지** 확인한다
  (회귀 테스트로서 유효한지 확인. 7번은 baseline에서도 통과하는 보존 확인용이 정상이다).

---

## 5. 예상 위험

| # | 위험 | 대응 |
|---|---|---|
| 1 | **`/users/search`가 `/users/{user_id}`에 흡수됨** — 실측으로 422 확인 | `/users/{user_id}` 앞에 선언 + 테스트 8로 고정 |
| 2 | `Query(min_length=2)`를 쓰면 400이 아니라 422가 나옴 | 명시적 검증 + `HTTPException(400)` |
| 3 | 새 route 추가가 기존 `GET /users/{user_id}` 매칭을 바꿈 | 테스트 7·8로 기존 동작 확인 (`/users/1` 200, `/users/999` 404, `/users/abc` 422) |
| 4 | 검색어 정규화를 저장 값에까지 적용해 기존 응답이 바뀜 | 비교 시에만 `lower()` 적용 |
| 5 | baseline 오인 (§0) | `git diff benchmark/task-003-base`가 빈 것을 확인 후 착수 |
| 6 | 요구되지 않은 정책(strip/정렬/페이지네이션) 추가로 범위 초과 | §1에 "하지 않을 것"을 명시하고 지킨다 |
| 7 | 테스트 실행 환경 문제 (로컬 머신에 fastapi/pytest 미설치, 네트워크 없음) | 파일 sha256 일치를 검증한 환경에서 `pytest -q` 실행하고 그 사실을 `test-result.txt`에 기록 |

---

## 6. 작업 순서

```text
1. baseline 복구 및 확인 (완료)
2. plan.md 작성 (이 문서)
3. app/service.py 에 search_users_by_email 추가
4. app/main.py 에 /users/search route 추가 (/users/{user_id} 앞)
5. tests/test_users.py 에 테스트 9종 추가
6. pytest -q 실행 → 전체 통과 확인
7. 신규 테스트를 baseline 코드에 적용해 회귀 유효성 확인
8. README.md 반영
9. diff.patch / test-result.txt / metrics.md / final-response.md 생성
```

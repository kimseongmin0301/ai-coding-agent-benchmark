# Task 002 결과

- Agent 식별자: `claude`
- Baseline: `benchmark-base` (`d96e992` — chore: restore benchmark baseline)
- 작업 Branch: `experiment/claude-task-002`
- 변경 규모: 4 files changed, 131 insertions(+), 6 deletions(-)

---

## 변경 내용

### 요구사항 A — 이메일 중복 방지 (case-insensitive, HTTP 409)

- `app/service.py`에 비교 전용 정규화 함수 `normalize_email()`을 추가했다. `strip()` 후 `lower()`를 적용한 값을 **비교 키로만** 사용하고, 저장되는 이메일 값은 요청 원본 표기를 그대로 유지한다.
- 조회 helper `find_user_by_email()`을 추가했다.
- 도메인 예외 `EmailAlreadyExistsError`를 추가하고, `create_user()`가 저장소에 쓰기 **직전**에 중복을 검사해 예외를 던지도록 했다.
- `app/main.py`의 `add_user()`에서 이 예외를 잡아 `409 Conflict` / `detail: "Email already exists"`로 변환한다.

### 요구사항 B — 사용자 ID 충돌 방지

- 기존 `new_id = len(users) + 1`을 제거하고 `next_user_id()` helper로 대체했다.
- 저장된 사용자가 없으면 `1`, 있으면 `max(users) + 1`을 반환한다.
- 저장 구조는 기존 in-memory `Dict[int, dict]` 그대로이며 `app/store.py`는 수정하지 않았다.

### 요구사항 C — 테스트 추가

`tests/test_users.py`에 5개 테스트를 추가했다 (기존 6개 + 신규 5개 = 총 11개).

| 테스트 | 검증 대상 |
|---|---|
| `test_create_user_with_duplicate_email_returns_409` | 동일 이메일 → 409, detail 문자열, **사용자 수·기존 데이터 불변** |
| `test_create_user_with_duplicate_email_ignores_case` | 대소문자만 다른 이메일 → 409 |
| `test_create_user_after_delete_does_not_reuse_existing_id` | 삭제 후 생성 시 ID가 1·2와 충돌하지 않음, **남은 사용자(Bob)가 덮어써지지 않음** |
| `test_create_user_with_new_email_returns_201` | 정상 생성 → 201, 생성된 ID로 재조회 가능 |
| `test_create_user_preserves_email_casing` | 저장된 이메일이 원본 대소문자를 유지 (정규화는 비교에만 적용) |

### 요구사항 D — 기존 API Contract 유지

- `GET /health`, `GET /users`, `GET /users/{user_id}`, `DELETE /users/{user_id}`의 코드는 변경하지 않았다.
- `app/models.py`, `app/store.py`, `tests/conftest.py`, `tests/test_health.py`, `requirements.txt`는 변경하지 않았다.
- 기존 테스트 6개는 수정 없이 그대로 통과한다. 특히 `test_create_user`가 기대하는 `id == 3`은 `max({1,2}) + 1 == 3`으로 그대로 성립한다.
- 신규 Dependency 추가 없음.

### 요구사항 E — README 반영

`README.md`에 `## API 동작 정책` 섹션을 추가하고 case-insensitive unique 정책, 409 응답, 삭제 이후 ID 충돌 방지 규칙을 기재했다.

---

## 수정한 파일

| 파일 | 변경 |
|---|---|
| `app/service.py` | +43 / -4 — `EmailAlreadyExistsError`, `normalize_email()`, `find_user_by_email()`, `next_user_id()` 추가 및 `create_user()` 수정 |
| `app/main.py` | +16 / -2 — import 정리, `add_user()`에서 409 변환 |
| `tests/test_users.py` | +69 / -0 — 신규 테스트 5개 추가 (기존 테스트 무수정) |
| `README.md` | +9 / -0 — API 동작 정책 섹션 추가 |

수정하지 않은 파일: `app/__init__.py`, `app/models.py`, `app/store.py`, `tests/conftest.py`, `tests/test_health.py`, `requirements.txt`

---

## 테스트

- **실행 명령**: `pytest -q`
- **결과**: `11 passed` (기존 6 + 신규 5, 실패 0)
- 전체 출력은 같은 디렉터리의 `test-result.txt`에 저장했다.

### 신규 테스트의 회귀 검증

추가한 테스트가 실제로 버그를 잡는지 확인하기 위해, **baseline의 `app/`에 신규 테스트만 적용**해 실행했다.

```text
3 failed, 8 passed
FAILED test_create_user_with_duplicate_email_returns_409
FAILED test_create_user_with_duplicate_email_ignores_case
FAILED test_create_user_after_delete_does_not_reuse_existing_id
  E  assert 2 not in (1, 2)     <- len(users)+1 이 Bob(id=2)을 덮어쓰던 버그
```

즉 신규 테스트 3개는 baseline에서 실패하고 수정 후 통과하는 유효한 회귀 테스트다. 나머지 2개는 기존 동작 보존을 확인하는 테스트이므로 baseline에서도 통과한다.

### 테스트 실행 환경에 대한 고지

대상 Repository가 있는 로컬 머신에는 `fastapi`/`pytest`가 설치되어 있지 않고 해당 환경에서 네트워크 접근이 불가능해 설치할 수 없었다. 따라서 `app/`, `tests/`, `README.md`, `requirements.txt` 전 파일의 sha256이 Repository와 **완전히 일치함을 검증한 환경**에서 `pytest -q`를 실행했다. 검증에 사용한 체크섬 목록은 `test-result.txt`에 함께 기록했다.

---

## 설계 판단

### 1. 이메일 중복 처리 — 검사를 service 계층에 둔 이유

`main.py`에서 `find_user_by_email()`을 호출해 검사하는 방법도 가능했지만, **service 계층에서 예외를 던지는 방식**을 택했다.

- 유일성은 저장소의 불변식(invariant)이다. 검사를 라우터에 두면 `create_user()`를 다른 경로에서 호출할 때 우회된다.
- 검사와 저장 사이에 다른 코드가 끼어들 수 없도록 `create_user()` 안에서 검사 직후 저장한다.
- 기존 코드 스타일상 service 계층은 HTTP를 모른다(`get_user`는 `None`, `delete_user`는 `bool` 반환). 이를 유지하기 위해 HTTP 상태 코드는 service가 아니라 `main.py`에서 부여했다. 도메인 예외 → HTTP 변환은 라우터 책임이다.

### 2. 이메일 정규화 — `strip().lower()`를 비교에만 적용

- 요구사항은 대소문자 무시만 명시했으나, 앞뒤 공백은 중복을 손쉽게 우회하는 입력이라 `strip()`을 함께 적용했다. 저장 값과 응답 값에는 영향을 주지 않으므로 기존 contract를 깨지 않는다.
- **정규화한 값을 저장하지는 않았다.** `test_create_user`가 `"charlie@example.com"`을 그대로 기대하고 있고, 사용자가 입력한 표기를 임의로 바꾸는 것은 요구사항 D(기존 동작 불필요한 변경 금지)에 어긋난다. 이 판단을 명시하기 위해 `test_create_user_preserves_email_casing` 테스트를 추가했다.

### 3. ID 충돌 해결 — `max(users) + 1`을 택한 이유

세 가지 후보를 검토했다.

| 후보 | 판단 |
|---|---|
| `len(users) + 1` (기존) | 삭제 후 기존 ID와 충돌. 요구사항 B가 지적한 버그 자체 |
| 모듈 전역 카운터 | 충돌은 막지만 `reset_users()`가 카운터를 되돌리지 않아 저장소와 상태가 어긋난다. 동기화하려면 `store.py`와 `conftest.py`까지 손대야 하므로 수정 범위가 커진다 |
| **`max(users) + 1`** ← 채택 | 상태를 저장소에서 파생하므로 별도 상태가 없고, `reset_users()`와 자동으로 정합한다. 기존 저장 구조를 그대로 쓰고 `store.py` 수정이 불필요하다 |

`max(users) + 1`은 **현재 저장된 어떤 ID보다도 크므로 정의상 충돌하지 않으며 기존 사용자를 덮어쓰지 않는다.** 기존 테스트가 기대하는 `id == 3`도 그대로 만족한다.

### 4. 수정 범위를 좁게 유지한 판단

`store.py`를 이메일 인덱스(`email → id` 맵) 구조로 바꾸면 조회가 O(1)이 되지만, 요구사항에 없는 저장 구조 변경이고 `reset_users()`까지 함께 고쳐야 한다. 현재 데이터는 in-memory 소규모이므로 O(n) 선형 탐색으로 충분하다고 판단해 채택하지 않았다.

---

## 남아 있는 고려사항

1. **동시성**: 현재 구현은 "검사 → 저장"이 원자적이지 않다. 단일 프로세스 in-memory 구조에서는 문제가 되지 않지만, 실제 저장소로 옮길 때는 DB의 unique 제약이나 락으로 보장해야 한다.
2. **ID 재사용**: `max + 1`은 삭제된 ID를 재사용하지 않으므로 ID가 단조 증가한다. 의도한 동작이지만, ID 공간을 촘촘히 써야 하는 요구가 생기면 재검토가 필요하다.
3. **이메일 정규화 수준**: 현재는 `strip().lower()`까지만 한다. RFC 관점의 정규화(예: Gmail의 `.` 무시, `+` 태그 제거, 유니코드 정규화, IDN 도메인 punycode 변환)는 정책 결정이 필요한 영역이라 범위에 넣지 않았다.
4. **이메일 형식 검증**: `UserCreate.email`은 여전히 길이 제약만 있는 `str`이다. `EmailStr`을 쓰려면 `pydantic[email]` 의존성이 추가되므로 "신규 Dependency 추가 지양" 제약에 따라 변경하지 않았다.
5. **조회 복잡도**: `find_user_by_email()`은 O(n)이다. 사용자 수가 커지면 이메일 인덱스가 필요하다.
6. **PUT/PATCH 부재**: 현재 API에는 수정 엔드포인트가 없어 "수정 시 이메일 중복" 경로는 존재하지 않는다. 추후 추가된다면 같은 검사를 재사용해야 한다.

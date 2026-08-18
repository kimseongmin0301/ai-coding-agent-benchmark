# Task 003 결과

## 변경 내용

- `GET /users/search?email=<keyword>` endpoint를 추가했습니다.
- 검색어가 2글자 미만이면 `HTTP 400 Bad Request`와 `Search keyword must be at least 2 characters` detail을 반환하도록 했습니다.
- 이메일 검색은 대소문자 구분 없는 부분일치로 수행합니다.
- 여러 사용자 매칭과 검색 결과 없음(`200 []`)을 지원합니다.
- `/users/search` route를 `/users/{user_id}`보다 먼저 선언해 route 충돌을 방지했습니다.
- 현재 코드 상태에 Task 002 기능이 반영되어 있지 않아, 이메일 중복 방지와 삭제 후 ID 충돌 방지를 최소 범위로 함께 반영했습니다.
- README에 사용자 검색 API와 정책을 추가했습니다.

## 수정한 파일

- `app/service.py`
- `app/main.py`
- `tests/test_users.py`
- `README.md`

## 테스트

- 실행 명령: `pytest -q`
- 결과: `15 passed in 0.18s`

## 설계 판단

- 검색 로직 위치: 기존 조회/생성/삭제 로직과 같은 `app/service.py`에 `search_users_by_email()`을 추가했습니다.
- Validation 위치: HTTP 요청의 query parameter validation이므로 `app/main.py` route에서 길이를 검사하고 `HTTPException`으로 400 응답을 반환했습니다.
- 문자열 비교 방식: `casefold()`를 사용해 대소문자를 구분하지 않는 비교를 수행했습니다. Task 002 이메일 중복 비교와 검색 비교에 같은 정규화 helper를 사용했습니다.
- 해당 방식을 선택한 이유: 기존 구조를 유지하면서 route는 HTTP 응답 책임을, service는 사용자 데이터 조회 책임을 갖도록 분리하기 위해서입니다.

## 계획 대비 변경 사항

- plan.md와 동일하게 구현한 부분:
  - 검색 로직은 service 계층에 추가했습니다.
  - 최소 길이 validation은 route 계층에서 처리했습니다.
  - `list[UserResponse]` response model을 재사용했습니다.
  - `casefold()` 기반 대소문자 무시 비교를 사용했습니다.
  - `/users/search` route를 `/users/{user_id}`보다 먼저 선언했습니다.
  - 현재 코드에서 누락된 Task 002 생성 안정성 기능을 함께 반영했습니다.
- 구현 과정에서 변경한 부분:
  - 없음.
- 변경 이유:
  - 해당 없음.

## Route 설계 검토

- `/users/search`와 `/users/{user_id}` 관계:
  - 두 route는 같은 `/users/` prefix 아래에 있고, `search`는 동적 path parameter인 `{user_id}`와 충돌할 수 있습니다.
- 선택한 처리 방식:
  - FastAPI route matching에서 정적 route가 먼저 매칭되도록 `/users/search`를 `/users/{user_id}`보다 앞에 선언했습니다.

## 남아 있는 고려사항

- `email` query parameter 누락 시 FastAPI 기본 validation 응답을 사용합니다.
- 현재 저장소는 in-memory dict이므로 동시 요청에서 검색/생성 일관성이나 영속성은 보장하지 않습니다.
- 실제 운영 환경에서는 이메일 unique 제약과 ID 발급을 DB 제약 또는 트랜잭션으로 보장해야 합니다.
- 현재 검색은 별도 정렬을 적용하지 않고 기존 저장 순서를 유지합니다.

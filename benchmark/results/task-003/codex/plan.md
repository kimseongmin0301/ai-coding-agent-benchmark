# Task 003 구현 계획

## 요구사항 해석

- `GET /users/search?email=<keyword>` endpoint를 추가한다.
- `email` query parameter는 필수이며, 검색어 길이가 2글자 미만이면 `400 Bad Request`와 `Search keyword must be at least 2 characters` detail을 반환한다.
- 검색은 이메일 부분 문자열 기준이며 대소문자를 구분하지 않는다.
- 여러 사용자가 매칭되면 모두 반환하고, 결과가 없으면 `200 OK`와 빈 배열을 반환한다.
- 기존 API contract를 유지하고, Task 002의 이메일 중복 방지와 삭제 후 ID 충돌 방지 기능도 유지한다.

## 수정 예상 파일

- `app/service.py`
  - 사용자 검색 함수 추가
  - Task 002 기능이 현재 코드에 없으면 이메일 중복 방지와 안전한 ID 생성도 함께 반영
- `app/main.py`
  - `/users/search` route 추가
  - 검색어 길이 validation과 400 응답 처리
  - 중복 이메일 예외를 409 응답으로 변환
- `tests/test_users.py`
  - Task 003 요구 테스트 추가
  - Task 002 기능 유지 테스트 추가 또는 보존
- `README.md`
  - 검색 API와 정책 문서화
  - Task 002 사용자 생성 정책이 누락되어 있으면 함께 반영

## 설계 판단

- 검색 로직 위치: `service.py`
  - 현재 목록 조회, 단건 조회, 생성, 삭제가 service 계층에 있으므로 검색도 같은 계층에 둔다.
- Validation 위치: `main.py`
  - 최소 길이 미달은 HTTP 요청 validation 성격이 강하므로 route에서 `HTTPException(400)`으로 변환한다.
  - service 함수는 검색 로직 자체에 집중한다.
- 기존 response model 재사용 여부: `list[UserResponse]`를 재사용한다.
  - 기존 `/users` endpoint와 같은 사용자 응답 구조를 사용한다.
- 문자열 비교 방식: `casefold()`를 사용한다.
  - 대소문자 무시 비교에 적합하고 Task 002 이메일 중복 비교에도 같은 helper를 재사용할 수 있다.

## 테스트 전략

- `"alice"` 검색 시 Alice만 반환되는지 확인한다.
- `"ALICE"` 검색 시 동일 결과가 반환되는지 확인한다.
- `"@example"` 검색 시 여러 사용자가 반환되는지 확인한다.
- 존재하지 않는 검색어는 `200 []`를 반환하는지 확인한다.
- 한 글자 검색어는 `400`과 지정 detail을 반환하는지 확인한다.
- 두 글자 검색어는 정상 검색을 수행하는지 확인한다.
- 기존 `/users` API가 계속 정상 동작하는지 확인한다.
- Task 002 기능인 중복 이메일 409, 대소문자 중복 409, 삭제 후 ID 충돌 방지를 확인한다.

## 예상 위험

- `/users/search`가 `/users/{user_id}`보다 뒤에 선언되면 FastAPI가 `search`를 path parameter로 해석할 수 있으므로 route 선언 순서를 `/users/{user_id}`보다 앞에 둔다.
- 현재 코드 상태에 Task 002 기능이 반영되어 있지 않다면 Task 003 구현과 함께 최소 범위로 복원해야 한다.
- 검색어 필수 여부는 FastAPI의 query parameter 필수 처리에 맡기되, 최소 길이 미달 메시지는 요구사항과 정확히 맞춘다.
- 기존 저장 순서를 유지하고 별도 정렬 정책은 추가하지 않는다.

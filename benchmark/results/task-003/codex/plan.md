# Task 003 구현 계획

## 요구사항 해석

- `GET /users/search?email=<keyword>` endpoint를 추가한다.
- `email` query parameter는 필수이다.
- 검색어는 최소 2글자 이상이어야 하며, 2글자 미만이면 `HTTP 400 Bad Request`와 `Search keyword must be at least 2 characters` detail을 반환한다.
- 검색은 이메일 부분 문자열 기준이며 대소문자를 구분하지 않는다.
- 여러 사용자가 매칭되면 모두 반환하고, 결과가 없으면 `200 OK`와 `[]`를 반환한다.
- 기존 API contract를 유지하고, Task 002의 이메일 중복 방지와 ID 충돌 방지 기능도 유지한다.

## 수정 예상 파일

- `app/service.py`
  - 이메일 검색 함수 추가
  - Task 002 기능이 현재 코드에 없으면 이메일 중복 방지와 안전한 ID 생성도 함께 반영
- `app/main.py`
  - `/users/search` route 추가
  - 검색어 길이 validation과 400 응답 처리
  - 중복 이메일 예외를 409 응답으로 변환
- `tests/test_users.py`
  - Task 003 요구 테스트 추가
  - Task 002 기능 유지 테스트 추가
- `README.md`
  - 검색 API와 정책 문서화
  - 사용자 생성 정책이 누락되어 있으면 함께 반영

## 설계 판단

- 검색 로직 위치: `service.py`
  - 현재 사용자 조회/생성/삭제 로직이 service 계층에 있으므로 검색도 같은 계층에 둔다.
- Validation 위치: `main.py`
  - 최소 길이 미달은 HTTP 요청 validation 성격이 강하므로 route에서 `HTTPException(400)`으로 처리한다.
- 기존 response model 재사용 여부: `list[UserResponse]`를 재사용한다.
  - 기존 `/users`와 동일한 사용자 응답 구조를 사용한다.
- 문자열 비교 방식: `casefold()`를 사용한다.
  - 대소문자 무시 비교에 적합하고 Task 002 이메일 중복 비교에도 같은 helper를 재사용할 수 있다.

## 테스트 전략

- `"alice"` 검색 시 Alice 반환
- `"ALICE"` 검색 시 Alice 반환
- `"@example"` 검색 시 여러 사용자 반환
- 존재하지 않는 검색어는 `200 []` 반환
- 한 글자 검색어는 `400`과 지정 detail 반환
- 두 글자 검색어는 정상 검색 수행
- 기존 `/users` API 정상 동작 확인
- Task 002 기능인 중복 이메일 409, 대소문자 중복 409, 삭제 후 ID 충돌 방지 확인

## 예상 위험

- `/users/search`가 `/users/{user_id}`보다 뒤에 선언되면 FastAPI가 `search`를 path parameter로 해석할 수 있으므로 route 선언 순서를 주의한다.
- 현재 코드 상태에 Task 002 기능이 반영되어 있지 않다면 Task 003 구현과 함께 최소 범위로 복원해야 한다.
- `email` query parameter 누락은 FastAPI 기본 validation에 맡기고, 최소 길이 미달 메시지만 요구사항과 정확히 맞춘다.
- 별도 정렬 규칙은 추가하지 않고 기존 저장 순서를 유지한다.

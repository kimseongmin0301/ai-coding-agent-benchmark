# Task 002 결과

## 변경 내용

- `POST /users` 생성 시 이메일을 대소문자 구분 없이 중복 검사하도록 수정했습니다.
- 중복 이메일이면 `HTTP 409 Conflict`와 `Email already exists` detail을 반환하도록 처리했습니다.
- 사용자 삭제 후 새 사용자를 생성할 때 기존 ID와 충돌하지 않도록 `max(existing_id) + 1` 방식으로 ID를 생성하도록 수정했습니다.
- 요구사항에 명시된 이메일 중복, 대소문자 중복, 삭제 후 ID 충돌 방지, 정상 생성 테스트를 추가했습니다.
- README에 사용자 생성 정책을 반영했습니다.

## 수정한 파일

- `app/service.py`
- `app/main.py`
- `tests/test_users.py`
- `README.md`

## 테스트

- 실행 명령: `pytest -q`
- 결과: `9 passed in 0.10s`

## 설계 판단

- 이메일 중복 처리 방식: 저장된 사용자 이메일과 입력 이메일을 모두 `casefold()`로 정규화해 비교했습니다. 이를 통해 `alice@example.com`과 `ALICE@example.com`을 동일한 이메일로 처리합니다.
- ID 충돌 해결 방식: 현재 in-memory 저장 구조의 key 중 최댓값을 기준으로 새 ID를 `max(users.keys(), default=0) + 1`로 생성했습니다.
- 해당 방식을 선택한 이유: 별도 DB나 외부 의존성을 추가하지 않고, 기존 dict 기반 저장 구조 안에서 기존 사용자를 덮어쓰지 않는 가장 작은 변경입니다.

## 남아 있는 고려사항

- 현재 저장소는 in-memory dict이므로 프로세스 재시작 시 데이터가 초기화됩니다.
- 동시 요청이 많은 운영 환경에서는 ID 발급과 중복 검사에 대해 별도 동시성 제어 또는 영속 저장소가 필요합니다.

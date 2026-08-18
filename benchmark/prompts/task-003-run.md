# Task 003 실행 프롬프트

현재 Repository의 다음 문서를 먼저 읽고 과제를 수행하세요.

- `benchmark/experiment-definition.md`
- `benchmark/task-003.md`

현재 실행 중인 Coding Agent의 종류를 자신의 실행 환경을 기준으로 식별하세요.

- Codex CLI인 경우 Agent 식별자는 `codex`
- Claude Code인 경우 Agent 식별자는 `claude`

이번 작업은 Codex CLI와 Claude Code를 동일 조건에서 비교하기 위한 독립 실험입니다.

---

## 실행 규칙

반드시 다음 조건을 지키세요.

1. 현재 Repository의 코드와 기존 테스트를 먼저 확인합니다.
2. `benchmark/task-003.md`에 정의된 요구사항을 그대로 따릅니다.
3. 상대 Agent의 결과 디렉터리는 읽거나 수정하지 않습니다.
4. 다른 Agent가 어떤 방식으로 구현할지 추측하거나 의식하지 않습니다.
5. 요구사항에 없는 대규모 리팩터링을 하지 않습니다.
6. 새로운 Dependency 추가를 최대한 피합니다.
7. 실제 Repository 파일을 직접 수정합니다.
8. 테스트 코드는 실제 `tests/` 내부에 작성합니다.
9. README를 실제로 수정합니다.
10. 구현 완료 후 반드시 `pytest -q`를 실제로 실행합니다.
11. 자신의 Agent 결과 디렉터리에 Task 문서가 요구한 결과 파일을 모두 생성합니다.
12. 측정할 수 없는 실행 메트릭은 추측하지 않고 `측정 불가`로 기록합니다.
13. 채팅 응답만 작성하고 실제 파일을 생성하지 않으면 미완료로 간주합니다.

---

## 구현 전 필수 작업

**코드를 수정하기 전에 먼저 자신의 `plan.md`를 작성하세요.**

Codex CLI:

```text
benchmark/results/task-003/codex/plan.md
```

Claude Code:

```text
benchmark/results/task-003/claude/plan.md
```

plan.md를 작성한 뒤 실제 구현을 시작합니다.

구현 중 계획을 변경할 수 있지만,
변경한 경우 최종 보고서에 변경 이유를 반드시 기록하세요.

---

## Agent별 결과 저장 위치

### Codex CLI

```text
benchmark/results/task-003/codex/
├── plan.md
├── final-response.md
├── test-result.txt
├── diff.patch
└── metrics.md
```

### Claude Code

```text
benchmark/results/task-003/claude/
├── plan.md
├── final-response.md
├── test-result.txt
├── diff.patch
└── metrics.md
```

자신의 Agent 전용 디렉터리만 사용하세요.

상대 Agent의 결과 파일을 읽거나 수정하지 마세요.

---

## 테스트

반드시 실제로 실행하세요.

```bash
pytest -q
```

실패한 테스트가 있다면 원인을 확인하고 수정한 뒤 다시 실행합니다.

최종적으로 전체 테스트가 통과해야 합니다.

테스트 결과는 자신의 `test-result.txt`에 기록하세요.

---

## Diff

Task 003 baseline 대비 실제 코드 변경을 `diff.patch`에 저장하세요.

가능하면 다음 파일만 diff 대상으로 포함하세요.

```text
app/
tests/
README.md
```

`benchmark/results/` 자체는 patch 대상에서 제외하세요.

---

## 최종 검토

작업을 끝내기 전에 반드시 확인하세요.

- `plan.md`를 구현 전에 작성했는가
- `/users/search`가 요구사항대로 동작하는가
- 최소 검색어 길이 Validation이 동작하는가
- 대소문자 무시 부분일치가 동작하는가
- 검색 결과가 없을 때 `200 []`인가
- 여러 사용자 검색이 가능한가
- 기존 API가 깨지지 않았는가
- Task 002 기능이 유지되는가
- 신규 테스트가 실제 요구사항을 검증하는가
- README가 반영되었는가
- 전체 테스트가 통과하는가
- 결과 파일이 모두 생성되었는가
- 상대 Agent 결과를 읽지 않았는가

---

## 최종 응답

작업 완료 후 채팅에는 전체 결과를 다시 복사하지 마세요.

다음만 간단히 보고하세요.

- 작업 완료 여부
- 생성한 결과 디렉터리
- 최종 테스트 결과
- 구현 과정에서 plan.md 대비 주요 변경이 있었는지 여부

이제 `benchmark/task-003.md`의 과제를 수행하세요.

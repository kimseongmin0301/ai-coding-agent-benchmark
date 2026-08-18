다음 문서를 먼저 읽어주세요.

- ai-coding-agent-benchmark/benchmark/experiment-definition.md
- ai-coding-agent-benchmark/benchmark/task-002.md

현재 실행 중인 Coding Agent의 종류를 자신의 도구 환경을 기준으로 식별하세요.

- Codex CLI라면 Agent 식별자는 `codex`
- Claude Code라면 Agent 식별자는 `claude`

이번 작업은 동일 Repository에서 수행되는 독립 비교 실험입니다.

반드시 다음 조건을 지켜주세요.

- 현재 Repository 코드를 먼저 확인합니다.
- task-002.md 요구사항만 해결합니다.
- 실제 Repository 파일을 직접 수정합니다.
- 상대 Agent의 결과 디렉터리는 읽거나 수정하지 않습니다.
- 구현 후 반드시 `pytest -q`를 실행합니다.
- 자신의 Agent 전용 결과 디렉터리에 test-result.txt, diff.patch, final-response.md를 실제 생성합니다.
- 요구사항에 없는 대규모 리팩터링을 하지 않습니다.
- 다른 Agent가 어떻게 구현할지 추측하지 않습니다.
- 작업이 끝난 후 전체 결과를 채팅에 반복하지 말고 완료 여부와 생성 경로만 간단히 보고합니다.

추가 구현 힌트 없이 Repository와 Issue를 분석하여 해결해주세요.

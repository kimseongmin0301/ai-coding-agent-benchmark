# AI Coding Agent Benchmark
### Codex CLI vs Claude Code

Codex CLI와 Claude Code를 동일한 Repository, 동일한 요구사항, 동일한 baseline에서 비교한 실험 프로젝트입니다.

단순히 “어느 모델이 더 좋은가?”를 비교하는 것이 아니라,

> **어떤 개발 업무에서 어떤 Coding Agent를 사용하는 것이 더 적합한가?**

를 확인하는 것을 목표로 했습니다.

---

# 결론부터

이번 실험에서 가장 크게 체감된 차이는 **속도**였습니다.

**Codex가 Claude보다 훨씬 빠르게 작업을 완료했습니다.**

다만 모든 Task에서 시작/종료 시각을 동일한 방식으로 자동 계측하지 않았기 때문에,
이를 정확한 wall-clock benchmark 수치로 주장하지는 않습니다.

따라서 속도에 대해서는 다음과 같이 구분합니다.

```text
정량적으로 기록된 항목
- 테스트 실행 횟수
- 수정 파일 수
- 추가/삭제 라인 수
- 평가 점수

정성적 관찰
- 실제 작업 과정에서 Codex가 Claude보다 훨씬 빠르게 결과를 완성함
```

Task 003에서는 수정 파일 수와 추가 라인 수가 거의 동일했지만,
Codex는 테스트 실행 횟수가 더 적었고 두 평가자 모두 **품질 대비 실행 효율은 Codex 우세**로 판단했습니다.

---

# 전체 결과 요약

| Task | 평가 대상 | 결과 |
|---|---|---|
| Task 001 | Research / Strategy / Documentation | **Claude 우세** |
| Task 002 | Bug Fix / Implementation / Test | **실질 동급** |
| Task 003 | Planning / Feature Development | **Codex 우세** |

## 가장 단순하게 정리하면

```text
명확한 문제
→ Codex

모호한 문제 / 조사 / 깊은 검토
→ Claude
```

또는 개발 관점에서는 다음과 같이 정리할 수 있습니다.

```text
Execution
→ Codex

Exploration / Analysis
→ Claude
```

---

# 그래서 어떻게 사용할 것인가?

실험 결과, 두 Agent를 동일한 용도로 사용하는 것보다
**업무 성격에 따라 선택하는 것이 더 효율적**이라고 판단했습니다.

## Codex를 우선 사용할 작업

### 구현 / Coding

- 명확한 요구사항의 기능 구현
- 작은 버그 수정
- 빠른 코드 변경
- 기존 코드에 최소 patch 적용
- 반복적인 개발 작업
- 테스트가 이미 존재하는 작업
- 구현 속도가 중요한 작업

한 줄로 정리하면:

> **무엇을 만들어야 하는지가 비교적 명확하다면 Codex**

---

## Claude를 우선 사용할 작업

### 조사 / 분석 / 검토

- 구현 전 요구사항 분석
- 여러 설계 대안 비교
- 기술 조사
- 위험 요소 탐색
- 테스트 케이스 확장
- 상세한 설계 문서 작성
- 코드 변경에 대한 깊은 검토

한 줄로 정리하면:

> **무엇을 만들어야 하는지부터 고민해야 한다면 Claude**

---

# 역할별 활용 판단

이번 실험의 범위는 Task 001~003이므로,
아래 역할 판단은 **현재까지의 잠정 결론**입니다.

| English Role | 한글 역할 | 현재 판단 |
|---|---|---|
| Researcher | 기술 조사 / 리서처 | **Claude 우세** |
| Requirement Analyst | 요구사항 분석 | **Claude 우세** |
| Planner | 설계 / 계획 수립 | **특성이 다름 — 단순 우열 보류** |
| Coder | 구현 / 개발 | **Codex 근소 우세** |
| Fast Fix Agent | 빠른 수정 / 패치 | **Codex 우세** |
| Tester | 테스트 작성 / 검증 | **실질 동급, 스타일 차이** |
| Deep Validator | 심층 검증 | **Claude 성향 강함** |
| Technical Writer | 기술 문서 작성 | **Claude 우세** |
| Concise Reporter | 간결한 결과 요약 | **Codex 우세** |
| Reviewer | 코드 리뷰 | **판단 보류** |
| Debugger | 디버깅 / 원인 분석 | **판단 보류** |

## 역할별 해석

### Researcher — 기술 조사 / 리서처

Claude가 더 강했습니다.

Task 001에서 공식 문서 기반의 세부 기능, 권한, Sandbox, Hook, 설정 방식 등을 더 깊게 조사했고,
불확실한 항목을 명확히 구분하는 경향을 보였습니다.

---

### Requirement Analyst — 요구사항 분석

Claude가 더 깊게 분석하는 경향이 있었습니다.

특히 Task 003에서 baseline과 요구사항 문서의 불일치를 발견하고,
그 원인을 상세히 추적했습니다.

다만 최종 요구사항 해석에서는 Codex가 더 완결된 결과를 만든 사례도 있었기 때문에,
**깊은 분석 = 항상 더 정확한 최종 판단**은 아니라는 점도 확인했습니다.

---

### Planner — 설계 / 계획 수립

단순히 Claude 우세라고 보기는 어렵습니다.

Task 003에서 Claude의 계획은 훨씬 상세했고
대안 비교와 위험 분석도 더 많았습니다.

반면 Codex의 계획은 더 짧았지만,
불확실한 상황을 조건부 계획으로 흡수해 실제 구현에서 요구사항 전체를 만족했습니다.

즉,

```text
Claude
→ 계획의 깊이

Codex
→ 계획의 간결성 + 실행 연결
```

이라는 차이가 있었습니다.

---

### Coder — 구현 / 개발

현재까지는 **Codex 근소 우세**로 판단합니다.

Task 002에서는 두 Agent의 구현 능력이 실질적으로 동급이었고,
Task 003에서도 검색 API 자체만 보면 큰 차이가 없었습니다.

그러나 Codex는 Task 003에서 문서 전체의 요구사항을 최종 결과물에 더 완결적으로 반영했고,
변경량 대비 기능 완결성도 높았습니다.

---

### Tester — 테스트 작성 / 검증

Task 002에서는 Claude가 더 많은 테스트와 부작용 검증을 추가했습니다.

Task 003에서는 Codex가 body 검증과 Task 002 회귀를 더 강하게 잡았고,
Claude는 route collision과 query parameter 누락 등 구조적인 위험을 더 넓게 확인했습니다.

따라서 현재 결론은:

```text
Codex
→ 핵심 요구사항을 직접 검증하는 테스트

Claude
→ 구조적 위험과 edge case를 넓게 검증하는 테스트
```

로 정리하는 것이 적절합니다.

---

### Technical Writer — 기술 문서 작성

Claude가 더 상세하고 검증 가능한 문서를 작성하는 경향이 있었습니다.

반면 Codex는 훨씬 짧고 빠르게 읽을 수 있는 결과를 만드는 데 강했습니다.

따라서:

```text
상세 설계 문서
→ Claude

PR 요약 / 짧은 결과 보고
→ Codex
```

가 더 적합해 보였습니다.

---

# 실험 방식

모든 실험은 가능한 한 다음 조건을 유지했습니다.

```text
Same Requirement
Same Repository
Same Baseline
Independent Execution
Separate Result Directory
Same Evaluation Criteria
Cross Evaluation
```

각 Agent는 상대 Agent의 결과를 보지 않은 상태에서 독립적으로 작업했습니다.

작업 결과는 다음과 같이 분리했습니다.

```text
benchmark/results/
├── task-001/
│   ├── codex/
│   └── claude/
├── task-002/
│   ├── codex/
│   └── claude/
└── task-003/
    ├── codex/
    └── claude/
```

평가 역시 독립적으로 수행했습니다.

```text
benchmark/evaluations/
├── task-001-002/
│   ├── chatgpt-review.md
│   └── claude-review.md
└── task-003/
    ├── chatgpt-review.md
    └── claude-review.md
```

---

# Task 001 — AI Coding CLI Research & Strategy

## 목적

첫 번째 과제는 코드 구현이 아니라
**AI Coding CLI 활용 전략 조사 및 문서화 능력**을 비교하는 것이었습니다.

주요 질문:

- AI Coding CLI는 일반 Chat 기반 AI와 무엇이 다른가?
- Repository 문맥을 어떻게 활용하는가?
- 파일 수정, Shell 실행, 테스트, Git 작업을 어떻게 연결하는가?
- Codex CLI와 Claude Code의 권한/통제 방식은 어떻게 다른가?
- 실제 개발 Workflow에 어떻게 적용할 수 있는가?
- 향후 Multi-Agent / CI/CD 구조로 어떻게 확장할 수 있는가?

---

## Task 001 결과

**Claude 우세**

Claude는 기술적 정확성, 구체성, 실행 가능성, 위험 통제 측면에서 더 높은 평가를 받았습니다.

Codex는 상대적으로 더 간결하고 빠르게 읽을 수 있는 문서를 만들었습니다.

### Codex 특징

- 간결함
- 실무자가 빠르게 읽기 좋은 구조
- 불필요하게 길지 않음
- 핵심 Workflow를 빠르게 전달

### Claude 특징

- 공식 문서 기반 세부 설명
- 권한 / Sandbox / Hook / 설정 구조 조사
- 불확실한 항목을 명확히 구분
- 위험 요소와 운영 통제를 상세히 설명

### 결론

```text
기술 조사 / 상세 문서
→ Claude

간결한 실무 가이드
→ Codex
```

---

# Task 002 — Bug Fix & Test

## 목적

기존 FastAPI 프로젝트에서 명확한 버그를 수정하도록 했습니다.

### 요구사항

#### 이메일 중복 생성 방지

```text
POST /users
```

- 이메일 중복 금지
- 대소문자 무시
- 중복 시 HTTP 409
- detail: `Email already exists`

#### 사용자 ID 충돌 방지

기존 구현:

```python
new_id = len(users) + 1
```

사용자 삭제 후 새로운 사용자를 생성하면
기존 ID와 충돌할 수 있는 문제를 수정하도록 했습니다.

---

## Task 002 결과

ChatGPT 평가:

```text
Codex  : 96 / 100
Claude : 96 / 100
Result : Draw
```

핵심 구현 능력은 **실질적으로 동급**으로 평가했습니다.

### Codex 특징

- 요구사항을 만족하는 최소 변경
- 작은 patch
- 단순한 구현 구조
- 변경 범위가 작아 리뷰 비용이 낮음

### Claude 특징

- 테스트 범위가 더 넓음
- 데이터 불변성 확인
- 설계 이유를 상세하게 기록
- 테스트 및 설명이 더 촘촘함

### 결론

```text
최소 변경 구현
→ Codex

테스트 확장 / 설명
→ Claude

핵심 구현력
→ 실질 동급
```

---

# Task 003 — Planning + Feature Development

## 목적

Task 003에서는 단순 버그 수정보다
**설계 판단이 필요한 기능 추가**를 비교했습니다.

새 API:

```text
GET /users/search?email=<keyword>
```

주요 요구사항:

- `email` query parameter 필수
- 최소 2글자
- case-insensitive
- 부분일치 검색
- 여러 사용자 반환
- 검색 결과 없음 → `200 []`
- 기존 API 유지
- Task 002 기능 유지
- README 반영

이번 Task부터는 구현 전에 `plan.md`를 작성하도록 했습니다.

```text
Planning
→ Implementation
→ Test
→ Documentation
```

전체 흐름을 함께 비교하기 위한 목적이었습니다.

---

## Task 003 결과

두 평가자 모두 **Codex 우세**로 판단했습니다.

### ChatGPT Evaluator

```text
Codex  : 93 / 100
Claude : 92 / 100
Winner : Codex
```

### Claude Evaluator

```text
Codex  : 92 / 100
Claude : 86 / 100
Winner : Codex
```

---

## 핵심 차이

검색 API 자체의 구현 능력은 두 Agent가 상당히 비슷했습니다.

두 Agent 모두 다음과 같은 핵심 설계에 독립적으로 도달했습니다.

```text
검색 로직
→ service.py

HTTP Validation
→ main.py

Response Model
→ 기존 UserResponse 재사용

Route
→ /users/search 를 /users/{user_id}보다 먼저 선언
```

그러나 Task 003 문서에는 Task 002 기능 유지 요구가 있었고,
실제 baseline에는 해당 기능이 빠져 있는 불일치가 존재했습니다.

여기서 판단이 갈렸습니다.

### Codex

Task 002 기능이 현재 코드에 없다면 함께 반영한다는 조건부 계획을 세우고,
실제로 다음 기능까지 복원했습니다.

- 이메일 중복 방지
- 안전한 사용자 ID 생성
- 관련 테스트

### Claude

baseline과 Task 문서의 불일치를 더 깊게 분석했지만,
baseline을 우선하는 방향으로 판단해 Task 002 기능을 최종 구현에 포함하지 않았습니다.

결과적으로 최종 산출물 기준으로는 Codex가 요구사항을 더 완결적으로 만족했습니다.

---

# Task 003 실행 효율

```text
Modified Files

Codex  : 4
Claude : 4

Added Lines

Codex  : 163
Claude : 162

Test Runs

Codex  : 2
Claude : 7
```

변경량은 거의 동일했습니다.

하지만 Codex는 같은 수준의 변경량 안에서
Task 003 검색 기능과 Task 002 기능 복원까지 함께 처리했습니다.

두 평가 모두 **품질 대비 실행 효율은 Codex 우세**로 판단했습니다.

---

# 속도 — 가장 크게 체감된 차이

이번 실험에서 가장 눈에 띈 차이는 **Codex의 작업 속도**였습니다.

실제 사용 과정에서 Codex가 Claude보다 훨씬 빠르게 작업을 완료했습니다.

다만 모든 Task에서 동일한 자동 측정 방식으로 시작/종료 시각을 기록하지 않았기 때문에
다음과 같이 표현합니다.

> **Codex가 실험 전반에서 훨씬 빠르게 작업을 완료하는 경향을 보였다.  
> 다만 정확한 wall-clock 비교는 모든 Task에서 일관되게 기록하지 못했으므로 정성적 관찰로 분류한다.**

향후에는 다음 항목까지 자동 수집할 수 있습니다.

```text
Execution Time
Token Usage
API / Subscription Cost
Test Retry Count
Human Intervention Count
```

---

# 실제 개발에서의 활용 전략

## Case 1 — 요구사항이 명확한 경우

```text
Issue
  ↓
Codex
  ↓
Test
  ↓
PR
  ↓
Human Review
```

예:

- 간단한 API 추가
- 버그 수정
- 테스트가 이미 있는 기능 수정
- 명확한 리팩터링
- 반복적인 코드 변경

---

## Case 2 — 요구사항이 모호하거나 설계 판단이 필요한 경우

```text
Issue
  ↓
Claude
요구사항 분석 / 기술 조사 / 대안 비교
  ↓
Human Approval
  ↓
Codex
구현
  ↓
Test
  ↓
Claude 또는 별도 Review Agent
심층 검토
  ↓
Human Review
```

---

# Multi-Agent Workflow Hypothesis

현재까지의 실험 결과를 기반으로
다음과 같은 Multi-Agent 구조를 가설로 설정했습니다.

```text
┌────────────────────────────────────┐
│ Research / Requirement Analysis    │
│ 기술 조사 / 요구사항 분석         │
│              Claude                │
└─────────────────┬──────────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│ Planning                           │
│ 설계 / 계획                         │
│ Claude + Codex Cross Validation    │
└─────────────────┬──────────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│ Implementation                     │
│ 구현 / 개발                         │
│              Codex                 │
└─────────────────┬──────────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│ Testing / Validation               │
│ 테스트 / 검증                       │
│      Codex + Claude Cross Test     │
└─────────────────┬──────────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│ Deep Review                        │
│ 심층 검토                           │
│        Claude / Review Agent       │
└─────────────────┬──────────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│ Human Approval                     │
│ 사람 최종 검토 / Merge 승인        │
└────────────────────────────────────┘
```

핵심은 한 Agent에게 모든 업무를 맡기는 것이 아닙니다.

> **빠른 구현은 Codex, 깊은 분석과 검증은 Claude**

라는 서로 다른 특성을 Workflow에 배치하는 것이 목적입니다.

---

# Repository Structure

```text
.
├── app/
├── tests/
├── benchmark/
│   ├── experiment-definition.md
│   ├── task-001.md
│   ├── task-002.md
│   ├── task-003.md
│   │
│   ├── prompts/
│   │
│   ├── results/
│   │   ├── task-001/
│   │   ├── task-002/
│   │   └── task-003/
│   │
│   └── evaluations/
│       ├── task-001-002/
│       └── task-003/
│
└── README.md
```

실제 Agent 결과, diff, 테스트 로그, plan 및 평가 자료는
`benchmark/` 아래에서 확인할 수 있습니다.

---

# Branch Strategy

각 Agent가 상대 구현에 영향을 받지 않도록
실험 과정에서는 별도 branch를 사용했습니다.

예:

```text
benchmark-base

experiment/codex-task-002
experiment/claude-task-002

benchmark/task-003-base

experiment/codex-task-003
experiment/claude-task-003
```

각 Agent는 동일한 baseline에서 독립적으로 작업했습니다.

최종 `main` branch에는 실험 결과와 평가 자료를 통합하되,
각 Agent의 실제 작업 이력은 실험 branch에 유지합니다.

---

# 이번 실험에서 얻은 결론

가장 중요한 결론은

> **Codex와 Claude 중 어느 것이 더 좋은가?**

가 아니었습니다.

실제로는 각 Agent의 강점이 달랐습니다.

```text
Codex
→ 빠르게 구현
→ 간결한 결과
→ 작은 변경
→ 높은 실행 효율

Claude
→ 깊은 분석
→ 넓은 검증
→ 상세한 계획
→ 검증 가능한 문서
```

따라서 현재 기준으로는 다음 전략이 가장 적절하다고 판단합니다.

> **명확한 구현 작업에는 Codex를 우선 사용하고,  
> 요구사항 분석·기술 조사·깊은 검토가 필요한 작업에는 Claude를 사용한다.**

---

# Next Step

다음 단계에서는 이번 실험 결과를 기반으로
실제 Multi-Agent Workflow를 구성하는 것을 목표로 합니다.

예상 구조:

```text
GitHub Issue
    ↓
Requirement / Planning Agent
    ↓
Human Approval
    ↓
Coding Agent
    ↓
Automated Test
    ↓
Review Agent
    ↓
Human Merge
    ↓
CI/CD
```

향후에는 GitHub Actions와 Coding Agent CLI를 연결해

- Issue 기반 작업 생성
- 자동 구현
- 자동 테스트
- Agent 간 교차 Review
- Human Approval
- CI/CD

까지 연결할 예정입니다.

---

# Final Summary

> **Claude는 깊은 조사·분석·검증에 강했고, Codex는 빠르고 간결하게 요구사항을 실제 코드로 완성하는 데 강했습니다.**

그리고 실제 사용 과정에서 가장 크게 체감된 차이는 **Codex의 속도**였습니다.

따라서 이 프로젝트의 현재 결론은 다음과 같습니다.

```text
명확한 구현
→ Codex

조사 / 분석 / 설계 검토
→ Claude

중요 변경
→ Codex 구현 + Claude 심층 검토 + Human Approval
```

이 실험을 기반으로 다음 단계에서는
두 Agent를 경쟁시키는 것이 아니라 **역할 단위로 조합하는 Multi-Agent 개발 Workflow**를 설계합니다.

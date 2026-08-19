# AI Coding Agent Benchmark
### Codex와 Claude — MCP 연동 기반 개발 업무별 Coding Agent 비교 실험

ChatGPT 환경에서 MCP(Model Context Protocol, 모델 컨텍스트 프로토콜)로 Repository와 도구를 연결하고, Codex와 Claude를 동일한 Repository(저장소), 동일한 요구사항, 동일한 baseline(기준 상태)에서 독립적으로 실행해 **개발 업무의 성격에 따라 어떤 Coding Agent(코딩 에이전트)가 더 적합한지** 비교한 실험 프로젝트입니다.

> **중요:** 이 연구에서는 Codex CLI나 Claude Code CLI를 터미널에서 직접 실행하지 않았습니다. 두 Agent 모두 MCP로 연결된 도구 환경에서 실행했으며, 실험 설계·프롬프트 작성·결과 비교·README 정리는 ChatGPT와의 대화를 통해 진행했습니다.

---

# 결론 (Conclusion)

이번 실험의 결론은 **“Codex와 Claude 중 누가 더 좋은가?”**가 아니었습니다.

3개의 Task를 수행하면서 두 Agent가 서로 다른 강점을 보였습니다.

| Task | 평가 대상 | 결과 |
|---|---|---|
| Task 001 | Research(조사) / Strategy(전략) / Documentation(문서화) | **Claude 우세** |
| Task 002 | Bug Fix(버그 수정) / Implementation(구현) / Test(테스트) | **실질 동급** |
| Task 003 | Planning(계획) / Feature Development(기능 개발) | **Codex 우세** |

가장 단순하게 정리하면 다음과 같습니다.

```text
무엇을 만들어야 하는지가 비교적 명확함
→ Codex

무엇을 만들어야 하는지부터 분석해야 함
→ Claude
```

개발 역할의 관점에서는 다음처럼 볼 수 있었습니다.

```text
Execution (실행 / 구현)
→ Codex

Exploration / Analysis (탐색 / 분석)
→ Claude
```

또한 실험 과정에서 **Codex가 Claude보다 훨씬 빠르게 작업을 완료하는 경향**을 체감했습니다.

다만 모든 Task의 시작/종료 시간을 동일한 방식으로 자동 측정하지 않았기 때문에 이는 정확한 wall-clock benchmark(실제 경과 시간 벤치마크)가 아니라 **정성적 관찰 결과**로 기록합니다.

이번 연구에서 얻은 가장 중요한 결론은 다음과 같습니다.

> **한 Agent를 모든 개발 업무에 사용하는 것보다, 작업의 성격에 따라 Agent를 선택하는 것이 더 합리적이다.**

다만 이 결론은 이번 3개 Task와 사용한 모델/추론 설정에서 관찰한 결과이며, 일반적인 모델 순위를 의미하지 않습니다.

---

# 연구 배경 (Why This Study)

MCP로 연결한 AI Coding Agent를 실제 개발 작업에 활용하면서 단순히

> **“어느 모델이 더 좋은가?”**

보다

> **“어떤 개발 업무에서 어떤 Agent를 사용하는 것이 더 적절한가?”**

가 더 중요한 질문이라고 생각했습니다.

Codex와 Claude 모두 MCP를 통해 코드 작성, 테스트, 분석, 문서화 등의 작업을 수행할 수 있지만 실제 사용 과정에서는 다음과 같은 차이가 나타났습니다.

```text
요구사항을 해석하는 방식
문제를 분석하는 깊이
구현을 시작하기까지의 과정
테스트 및 검증 방식
변경 범위 관리
문서화의 상세도
실제 작업 속도
```

하지만 이러한 차이를 개인적인 체감만으로 판단하고 싶지는 않았습니다.

그래서 다음 질문에서 이 실험을 시작했습니다.

> **동일한 Repository, 동일한 요구사항, 동일한 baseline에서 Codex와 Claude를 MCP 환경으로 각각 독립적으로 실행하면 실제 결과는 어떻게 달라질까?**

이번 Benchmark(벤치마크 / 비교 실험)에서는 단순히 최종 코드가 동작하는지만 비교하지 않았습니다.

```text
Requirement Understanding (요구사항 이해)
Research / Analysis (기술 조사 / 분석)
Planning (설계 / 계획)
Implementation (구현)
Testing / Validation (테스트 / 검증)
Documentation (문서화)
Efficiency (작업 효율)
```

를 함께 확인했습니다.

즉 연구 목적은 단순한 Winner(승자) 선정이 아니라,

```text
Codex vs Claude
        ↓
실제 작업 방식 비교
        ↓
상대적인 강점 / 약점 확인
        ↓
개발 Workflow에서의 적절한 활용 방법 탐색
```

이었습니다.

---

# 실험 환경 및 실행 방식 (Environment & Execution)

이번 연구는 CLI(Command Line Interface, 명령줄 인터페이스) 기반 실험이 아닙니다.

ChatGPT에서 실험을 설계하고, MCP(Model Context Protocol)로 연결된 Repository / GitHub / 실행 도구를 통해 각 Agent가 실제 작업을 수행하도록 했습니다.

```text
ChatGPT
GPT-5.6 Sol Medium
→ 연구 질문 정리
→ Task / Prompt 설계
→ 실험 조건 정리
→ 결과 비교 및 해석
→ README 작성

        ↓ MCP 연결

Codex 5.5 Medium
→ 독립 실행 Agent

Claude Opus 5 High
→ 독립 실행 Agent

        ↓

Repository 수정
Test 실행
Diff 확인
결과 산출
```

즉 이 연구에서 `Codex`와 `Claude`는 **터미널에서 CLI를 직접 조작해 비교한 것이 아니라, MCP로 연결된 Agent 실행 환경에서 비교**했습니다.

README 역시 실험 종료 후 별도로 수작업 작성한 문서가 아니라, **실험 설계와 결과를 알고 있는 ChatGPT와의 대화를 통해 정리·수정했습니다.**

따라서 본 결과는 다음 조건에 종속됩니다.

- GPT-5.6 Sol Medium이 구성한 Task와 Prompt
- Codex 5.5 Medium / Claude Opus 5 High
- MCP로 연결된 당시의 도구 및 Repository 환경
- 각 Agent에 허용된 도구와 권한
- 실험 당시의 모델 버전과 reasoning level(추론 수준)

모델이나 도구 환경이 달라지면 결과도 달라질 수 있습니다.

---

# 연구 질문 (Research Questions)

이번 실험에서는 다음 질문을 확인하고자 했습니다.

1. 동일한 요구사항에서 두 Agent의 결과물은 얼마나 달라지는가?
2. 실제 구현 능력에는 의미 있는 차이가 있는가?
3. 요구사항이 모호하거나 baseline과 충돌할 때 어떻게 판단하는가?
4. 테스트 작성과 검증 방식에는 어떤 차이가 있는가?
5. 깊은 분석이 항상 더 완전한 구현으로 이어지는가?
6. 작업 속도와 결과 품질 사이에는 어떤 차이가 있는가?
7. 실제 개발에서는 각 Agent를 어떤 역할에 배치하는 것이 적절한가?

---

# 실험 방식 (Method)

실험은 ChatGPT가 전체 비교 구조를 설계하고, MCP로 연결된 Agent가 실제 Repository 작업을 수행하는 방식으로 진행했습니다.

```text
ChatGPT
→ Task / Prompt 작성
→ 동일 조건 정의

        ↓

MCP-connected Agent
(MCP 연동 Agent)

Codex / Claude
→ Repository 읽기
→ 파일 수정
→ Test
→ Diff 확인
→ 결과 작성

        ↓

ChatGPT
→ 결과 비교
→ 평가 결과 종합
→ README 정리
```

**CLI에서 사람이 명령을 직접 입력해 Agent를 구동한 실험은 아닙니다.**

가능한 한 동일한 조건을 유지했습니다.

```text
Same Requirement (동일 요구사항)
Same Repository (동일 저장소)
Same Baseline (동일 기준 상태)
Independent Execution (독립 실행)
Separate Result Directory (결과 분리)
Same Evaluation Criteria (동일 평가 기준)
Cross Evaluation (교차 평가)
```

## 1. 독립 실행

각 Agent는 상대 Agent의 결과를 보지 않은 상태에서 같은 기준 코드에서 독립적으로 작업했습니다.

```text
Baseline
├── Codex Experiment
└── Claude Experiment
```

## 2. 실제 Repository 수정

채팅 답변만 비교하지 않았습니다.

각 Agent가 실제 파일을 수정하고 테스트를 실행하도록 했습니다.

## 3. 결과물 분리

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

## 4. 교차 평가

구현 결과가 완료된 뒤에는 각 결과물을 동일한 기준으로 비교했습니다.

```text
독립 실행
→ 결과물 교환
→ 동일 기준 평가
→ 교차 검증
→ 종합 판단
```

평가자는 평가가 완료되기 전 상대 평가자의 결론을 보지 않도록 분리했습니다.

---

# Task 001 — AI Coding Agent Research & Strategy
### AI 코딩 에이전트 활용 조사 및 전략

## 목적

첫 번째 Task는 코드 구현이 아니라 **AI Coding Agent와 관련 도구의 활용 전략을 조사하고 문서화하는 능력**을 비교하는 것이었습니다.

조사 내용에는 Coding CLI의 특성도 포함되었지만, **실험 자체를 CLI로 실행한 것은 아닙니다.**

주요 관점은 다음과 같습니다.

- 일반 Chat 기반 AI와 Coding CLI의 차이
- Repository 문맥 활용
- 파일 수정 / Shell 실행 / 테스트 / Git 작업 연결
- 권한 및 통제 방식
- 실제 개발 Workflow 적용
- Multi-Agent / CI/CD 확장 가능성

## 결과

### ChatGPT 평가

```text
Codex  : 92 / 100
Claude : 97 / 100
```

### Claude 평가

```text
Codex  : 85 / 100
Claude : 90 / 100
```

### 해석

**Claude 우세**

Claude는 공식 문서 기반의 기술 설명, 위험요소, 권한 구조, 설정 및 운영 통제를 더 상세하게 다뤘습니다.

Codex는 상대적으로 짧고 핵심이 빠르게 보이는 문서를 만들었습니다.

```text
상세 기술 조사 / 검증 가능한 문서
→ Claude

간결한 실무 요약
→ Codex
```

---

# Task 002 — Bug Fix & Test
### 버그 수정 및 테스트

## 목적

기존 FastAPI 프로젝트에서 명확한 버그를 수정하도록 했습니다.

주요 요구사항:

```text
Case-insensitive duplicate email prevention
(대소문자를 구분하지 않는 중복 이메일 방지)

Safe user ID generation after deletion
(사용자 삭제 후에도 안전한 ID 생성)

Tests
(테스트)

README update
(문서 수정)
```

## 결과

### ChatGPT 평가

```text
Codex  : 96 / 100
Claude : 96 / 100
Result : Draw (무승부)
```

### Claude 평가

```text
Codex  : 87 / 100
Claude : 89 / 100
```

핵심 Implementation(구현) 능력은 **실질적으로 동급**으로 판단했습니다.

### Codex 특징

- 요구사항 중심의 최소 변경
- 작은 patch(패치)
- 단순한 구현
- 리뷰하기 쉬운 변경 범위

### Claude 특징

- 더 넓은 테스트 범위
- 데이터 불변성 확인
- 상세한 설계 설명
- 추가 검증이 많음

```text
Minimal Implementation (최소 변경 구현)
→ Codex

Broader Validation (넓은 검증)
→ Claude

Core Coding Ability (핵심 구현 능력)
→ 실질 동급
```

---

# Task 003 — Planning + Feature Development
### 계획 및 기능 개발

## 목적

Task 003에서는 단순 버그 수정보다 **설계 판단이 필요한 기능 추가**를 비교했습니다.

새 API:

```text
GET /users/search?email=<keyword>
```

주요 요구사항:

- `email` query parameter(쿼리 파라미터) 필수
- 최소 2글자
- case-insensitive(대소문자 무시)
- 부분일치 검색
- 여러 사용자 반환
- 결과 없음 → `200 []`
- 기존 API 유지
- Task 002 기능 유지
- README 반영
- 구현 전 `plan.md` 작성

## 핵심 변수

Task 문서에는 **Task 002의 동작을 유지**해야 한다고 명시되어 있었지만 실제 baseline에는 해당 기능이 빠져 있었습니다.

```text
Specification (요구사항)
→ Task 002 behavior 유지

Actual Baseline (실제 기준 코드)
→ Task 002 behavior 없음
```

여기서 두 Agent의 판단이 갈렸습니다.

### Codex

Task 002 기능이 없다면 함께 복원한다는 조건부 계획을 세웠고 실제 구현에도 반영했습니다.

- 이메일 중복 방지
- 안전한 사용자 ID 생성
- 관련 테스트

### Claude

요구사항과 baseline의 불일치를 더 깊게 분석했습니다.

그러나 최종적으로 baseline을 우선 해석했고 Task 002 기능을 구현에 포함하지 않았습니다.

즉 **분석은 Claude가 더 깊었지만, 최종 산출물은 Codex가 전체 요구사항을 더 완결적으로 충족했습니다.**

## 평가 결과

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

## 실행 효율

```text
Modified Files (수정 파일 수)

Codex  : 4
Claude : 4

Added Lines (추가 라인 수)

Codex  : 163
Claude : 162

Test Runs (테스트 실행 횟수)

Codex  : 2
Claude : 7
```

변경량은 거의 동일했지만 Codex는 더 적은 테스트 실행으로 Task 003 기능과 Task 002 기능 복원까지 완료했습니다.

이 Task에서는 **품질 대비 실행 효율도 Codex 우세**로 판단했습니다.

---

# 역할별 관찰 결과

이번 3개 Task만을 기준으로 한 잠정적인 판단입니다.

| 역할 | 관찰 결과 |
|---|---|
| Researcher (기술 조사) | **Claude 우세** |
| Requirement Analyst (요구사항 분석) | **Claude가 더 깊은 분석 경향** |
| Planner (설계 / 계획) | **단순 우열 보류 — 서로 다른 장점** |
| Coder (구현 / 개발) | **Codex 근소 우세** |
| Fast Fix Agent (빠른 수정) | **Codex 우세** |
| Tester (테스트 / 검증) | **실질 동급, 스타일 차이** |
| Deep Validator (심층 검증) | **Claude 성향 강함** |
| Technical Writer (기술 문서) | **Claude 우세** |
| Concise Reporter (간결한 보고) | **Codex 우세** |
| Reviewer (코드 리뷰) | **이 실험에서는 판단 보류** |
| Debugger (디버깅) | **이 실험에서는 판단 보류** |

중요한 점은 **깊은 분석과 최종 실행 완결성은 같은 의미가 아니었다**는 것입니다.

Task 003에서 Claude는 문제를 더 깊게 분석했지만 최종 요구사항 충족도에서는 Codex가 더 좋은 결과를 만들었습니다.

---

# 속도 (Execution Speed)

실험 과정에서 가장 크게 체감된 차이는 **Codex의 작업 속도**였습니다.

Codex가 Claude보다 훨씬 빠르게 결과를 완성하는 경향이 있었습니다.

다만 모든 Task에서 시작/종료 시각을 동일한 자동화 방식으로 기록하지 않았기 때문에:

```text
Codex가 Claude보다 X배 빠르다
```

와 같은 정량적 결론은 내리지 않습니다.

따라서 속도 차이는 **Qualitative Observation(정성적 관찰)**으로만 기록합니다.

---

# 이 실험에서 얻은 활용 전략

이번 결과만 놓고 보면 다음과 같은 선택이 가능했습니다.

## 명확한 구현 작업

```text
Issue / Requirement
        ↓
Codex
        ↓
Implementation
        ↓
Test
        ↓
Human Review
```

예:

- 작은 API 추가
- 명확한 버그 수정
- 반복적인 코드 변경
- 기존 테스트가 존재하는 작업
- 빠른 patch가 필요한 작업

## 분석이 먼저 필요한 작업

```text
Issue / Requirement
        ↓
Claude
        ↓
Requirement Analysis
Technical Research
Alternative Comparison
        ↓
Human Decision
        ↓
Implementation
```

예:

- 요구사항이 모호한 기능
- 여러 설계 대안이 존재하는 문제
- 기술 조사
- 위험요소 검토
- 상세 문서 작성

---

# 중요한 구분 — 후속 연구는 이 역할 배치를 그대로 적용한 실험이 아님

이 연구에서 다음과 같은 가설을 세울 수 있었습니다.

```text
분석 / 조사
→ Claude

명확한 구현
→ Codex

깊은 검증
→ Claude 또는 별도 Review Agent

최종 승인
→ Human
```

하지만 **후속 연구인 `AI PR Review Agent`는 이 조합의 성능을 검증하는 Multi-Agent 실험으로 바로 이어지지 않았습니다.**

첫 번째 연구를 진행하면서 새롭게 생긴 질문은 다음이었습니다.

> **“AI가 코드를 잘 작성하는 것과 별개로, AI Reviewer가 실제 Pull Request를 제대로 검증할 수 있는가?”**

따라서 두 번째 연구에서는 Codex와 Claude의 Coding 성능을 다시 비교하지 않고, **PR Review 자체의 유효성을 독립된 주제로 분리**했습니다.

이 때문에 후속 연구에서는 실행 환경을 Claude Code로 통일하고:

```text
Claude 기반 Coding / Execution Agent
(MCP 연동)
        ↓
Pull Request
        ↓
별도의 Claude Reviewer Session
(MCP 연동)
        ↓
Review Decision
        ↓
Human Final Decision
```

구조를 사용했습니다.

즉,

```text
1번 연구의 결과를 그대로 적용한 실험
X

1번 연구에서 발견한 새로운 문제를 분리해 검증한 후속 연구
O
```

입니다.

이 구분은 두 Repository의 관계를 이해하는 데 중요합니다.

---

# 후속 연구 — AI PR Review Agent

첫 번째 연구를 통해 Coding Agent마다 다른 강점이 있다는 점을 확인했지만, 동시에 더 근본적인 질문이 남았습니다.

AI가 빠르게 코드를 작성하더라도:

- 요구사항을 제대로 구현했는가?
- 기존 동작을 깨뜨리지 않았는가?
- 테스트가 통과하면 정말 안전한가?
- 변경 범위가 적절한가?
- 최종 Merge 판단까지 AI에게 맡겨도 되는가?

를 별도로 확인할 필요가 있었습니다.

그래서 다음 프로젝트에서는 **Agent 간 Coding 성능 비교가 아니라 AI Code Review 자체**를 실험했습니다.

### AI PR Review Agent

`https://github.com/kimseongmin0301/ai-pr-review-agent`

연구 흐름은 다음과 같습니다.

```text
연구 1
AI Coding Agent Benchmark
“어떤 Agent가 어떤 개발 업무에 강한가?”

        ↓
새로운 질문 발생

연구 2
AI PR Review Agent
“AI Reviewer는 실제 PR을 어디까지 검증할 수 있는가?”

        ↓

Human-in-the-loop
“어디까지 AI에게 맡기고 어디서부터 사람이 판단해야 하는가?”
```

---

# 실험 기록과 README 작성 방식

두 연구에서 ChatGPT는 단순한 문서 작성 도구만으로 사용되지 않았습니다.

연구 과정에서 다음 역할을 담당했습니다.

```text
Research Question 정리
→ 실험 구조 설계
→ Task / Prompt 작성
→ 실행 결과 비교
→ 결과 해석
→ README 작성 및 수정
```

따라서 README는 연구가 끝난 뒤 제3자가 결과만 보고 작성한 문서가 아니라, **실험 계획부터 결과 정리까지 함께 진행한 ChatGPT를 통해 작성된 연구 기록**입니다.

다만 실제 코드 변경과 테스트 결과는 README 문장 자체가 아니라 Repository의 commit, diff, test 결과 및 benchmark 산출물을 기준으로 확인할 수 있도록 구성했습니다.

---

# 한계 (Limitations)

이번 결과는 다음 범위 안에서 해석해야 합니다.

- Task는 3개입니다.
- 특정 FastAPI Repository와 문제 유형을 사용했습니다.
- 사용한 모델 및 reasoning level에 따라 결과가 달라질 수 있습니다.
- 모든 Task의 wall-clock time을 동일하게 기록하지 않았습니다.
- Reviewer와 Debugger 역할은 이 연구에서 독립적으로 충분히 검증하지 않았습니다.
- 따라서 결과는 모든 상황에서의 절대적인 모델 우열을 의미하지 않습니다.

> **이번 결과는 이 실험 조건에서 관찰한 Codex와 Claude Code의 상대적인 작업 특성입니다.**

---

# Final Summary (최종 요약)

이번 실험에서 확인한 것은 단순한 모델 순위가 아니었습니다.

```text
Codex
→ 빠른 구현
→ 간결한 결과
→ 작은 변경
→ 높은 실행 효율

Claude
→ 깊은 조사
→ 넓은 분석
→ 상세한 검증
→ 상세한 문서
```

따라서 현재 실험 범위에서의 결론은:

> **명확한 구현 작업에는 Codex가 효율적이었고, 요구사항 분석·기술 조사·깊은 검토가 필요한 작업에서는 Claude가 강점을 보였습니다.**

그리고 이 연구의 가장 중요한 후속 질문은 **“어떤 Agent가 더 좋은가?”에서 “AI가 만든 결과물을 어떻게 검증할 것인가?”로 이동했습니다.**

그 질문을 별도의 `AI PR Review Agent` 프로젝트에서 검증했습니다.

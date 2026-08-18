# Task 001 — AI Coding CLI 활용 전략 문서 작성

## 1. 과제 목적

AI Coding Agent를 실제 소프트웨어 개발 업무에 적용하기 전에,
터미널 기반 AI Coding CLI 도구를 어떤 방식으로 사용할 수 있는지 조사하고
실무 적용 전략을 문서화한다.

이번 과제에서는 다음 두 도구를 중심으로 다룬다.

- OpenAI Codex CLI
- Anthropic Claude Code

단순한 설치 방법이나 명령어 나열이 아니라,

> 개발자가 AI Coding CLI를 실제 개발 프로세스에서 어떻게 활용할 수 있는가

를 중심으로 문서를 작성한다.

---

## 2. 공통 실행 환경

Codex CLI와 Claude Code는 **동일한 Repository 디렉터리**를 사용한다.

두 Agent를 위해 Repository를 별도로 복제하거나,
서로 다른 프로젝트 구조를 만들지 않는다.

예시:

```text
ai-coding-agent-benchmark/
```

두 Agent 모두 위 동일 Repository Root에서 작업한다.

다만 결과물이 서로 덮어써지지 않도록,
결과 파일은 Agent별 하위 디렉터리로 구분한다.

```text
benchmark/results/task-001/
├── codex/
└── claude/
```

Agent 식별자는 다음 값만 사용한다.

```text
Codex CLI   -> codex
Claude Code -> claude
```

---

## 3. 작성 목표

다음 질문에 답할 수 있는 문서를 작성한다.

1. AI Coding CLI란 무엇인가?
2. 일반적인 Chat 기반 AI 사용 방식과 무엇이 다른가?
3. Codex CLI는 어떤 방식으로 개발 업무에 활용할 수 있는가?
4. Claude Code는 어떤 방식으로 개발 업무에 활용할 수 있는가?
5. 두 도구의 공통점과 차이점은 무엇인가?
6. 실제 개발 Workflow에서는 어느 단계에 활용할 수 있는가?
7. 어떤 작업을 AI Agent에게 맡기고 어떤 작업은 사람이 직접 판단해야 하는가?
8. AI Coding CLI를 사용할 때 발생할 수 있는 위험과 한계는 무엇인가?
9. 안전하고 효율적으로 사용하기 위해 어떤 운영 규칙이 필요한가?
10. 향후 Multi-Agent 및 CI/CD 자동화로 확장하려면 어떤 구조가 적절한가?

---

## 4. 반드시 다뤄야 할 내용

### 4.1 AI Coding CLI 개념

- AI Coding CLI의 역할
- Repository Context 활용
- 파일 탐색 및 수정
- Shell Command 실행
- 테스트 실행
- Git 작업
- Agentic Coding의 의미

### 4.2 Codex CLI

- 주요 사용 목적
- 기본적인 작업 방식
- Repository를 이해하는 방식
- 코드 수정 과정
- 명령 실행 방식
- 개발자가 통제할 수 있는 요소
- 실제 개발 Workflow에서 활용 가능한 영역

### 4.3 Claude Code

동일한 기준으로 정리한다.

- 주요 사용 목적
- 기본적인 작업 방식
- Repository를 이해하는 방식
- 코드 수정 과정
- 명령 실행 방식
- 개발자가 통제할 수 있는 요소
- 실제 개발 Workflow에서 활용 가능한 영역

### 4.4 Codex CLI와 Claude Code 비교

최소한 다음 기준으로 비교한다.

- 초기 사용 난이도
- 코드베이스 이해
- 코드 생성 및 수정
- Shell / Tool 실행
- Context 관리
- 사용자 통제 가능성
- 반복 작업 자동화
- 테스트 및 검증
- Git Workflow 활용
- 대규모 Repository 활용 가능성
- 실무 적용성

필요하다면 추가 비교 기준을 제안해도 된다.

---

## 5. 실제 개발 Workflow 설계

다음 개발 단계에서 Agent를 어떻게 활용할 수 있는지 설명한다.

```text
요구사항 확인
    ↓
구현 계획
    ↓
코드 탐색
    ↓
코드 작성 / 수정
    ↓
테스트
    ↓
코드 리뷰
    ↓
Git Commit
    ↓
Pull Request
```

각 단계에서 다음을 구분한다.

- AI에게 맡기기 적합한 작업
- 사람이 확인해야 하는 작업
- 자동화하면 위험한 작업

---

## 6. 운영 및 안전성

최소한 다음 내용을 검토한다.

- 명령 실행 권한
- 파일 수정 범위
- Secret / 환경변수 접근
- Production 접근
- 위험 명령어
- Git push / merge 권한
- 자동 테스트
- Human Review
- 작업 로그 및 추적성

---

## 7. 연구해야 할 핵심 질문

### Question 1

AI Coding CLI는 기존 ChatGPT / Claude 웹 채팅을 이용한
코드 작성 방식보다 실제 개발 생산성을 높일 수 있는가?

### Question 2

AI Agent가 Repository 내부에서 직접 작업하도록 만드는 것이
어떤 장점과 위험을 발생시키는가?

### Question 3

개발자는 Agent에게 어느 수준까지 권한을 부여해야 하는가?

### Question 4

AI Coding Agent가 작성한 코드를 어떤 방식으로 검증해야 하는가?

### Question 5

Codex CLI와 Claude Code를 경쟁 관계로만 볼 것인지,
아니면 역할을 나누어 함께 사용할 수 있는지 검토한다.

---

## 8. 향후 확장 구조

```text
AI Coding CLI 조사
        ↓
Codex CLI 실습
        ↓
Claude Code 실습
        ↓
동일 Task 비교
        ↓
Agent 개발 규칙 정의
        ↓
Single Agent Workflow
        ↓
Multi-Agent Workflow
        ↓
GitHub Issue / Pull Request 연동
        ↓
GitHub Actions
        ↓
CI 자동화
        ↓
Human Approval
        ↓
CD 자동화
```

---

## 9. 문서 작성 원칙

- 단순 제품 소개 문서로 작성하지 않는다.
- 단순 설치 가이드로 작성하지 않는다.
- 기능 목록만 나열하지 않는다.
- 실제 개발자가 적용할 수 있는 관점에서 작성한다.
- 장점뿐 아니라 한계와 위험도 다룬다.
- 확실하지 않은 기술적 사실은 단정하지 않는다.
- 가능하면 공식 문서를 기준으로 사실 관계를 확인한다.
- 현재 기능과 향후 아이디어를 명확히 구분한다.
- 특정 제품을 과도하게 옹호하지 않는다.
- 비교 결과에는 근거를 포함한다.

---

## 10. 이번 과제에서 하지 않는 것

- 실제 Multi-Agent 구현
- GitHub Actions 구현
- CI/CD Pipeline 구현
- Agent Orchestrator 개발
- 자동 Pull Request 생성 시스템 구현

이번 과제는 구현 전에 활용 전략을 정의하는 단계이다.

---

## 11. 실제 파일 작성 요구사항

이 과제는 **채팅 응답으로 문서를 출력하는 것만으로 완료되지 않는다.**

현재 Repository 내부에 실제 Markdown 파일을 생성해야 한다.

### Codex CLI 실행 시

```text
benchmark/results/task-001/codex/
└── ai-coding-cli-strategy.md
```

정확한 경로:

```text
benchmark/results/task-001/codex/ai-coding-cli-strategy.md
```

### Claude Code 실행 시

```text
benchmark/results/task-001/claude/
└── ai-coding-cli-strategy.md
```

정확한 경로:

```text
benchmark/results/task-001/claude/ai-coding-cli-strategy.md
```

자신이 어떤 Agent인지 확인하여 해당 경로를 사용한다.

폴더가 없다면 직접 생성한다.

다른 Agent의 결과 폴더나 파일은 읽거나 수정하지 않는다.

예:

```text
Codex는 benchmark/results/task-001/claude/ 접근 금지
Claude는 benchmark/results/task-001/codex/ 접근 금지
```

---

## 12. 완료 조건

- 동일 Repository Root에서 작업한다.
- 자신의 Agent 전용 결과 디렉터리를 사용한다.
- 결과 Markdown 파일이 실제로 생성되어 있다.
- Task 001 요구사항 전체가 해당 파일에 작성되어 있다.
- 상대 Agent의 결과물을 읽거나 수정하지 않는다.
- 채팅에만 결과를 작성하고 파일을 생성하지 않은 경우 미완료로 간주한다.

---

## 13. 최종 응답

파일 작성을 완료한 뒤 채팅의 최종 응답에는 다음만 포함한다.

```text
- 작성 완료 여부
- 생성한 파일 경로
- 문서의 주요 구성 요약
```

문서 전체 내용을 채팅에 다시 복사할 필요는 없다.

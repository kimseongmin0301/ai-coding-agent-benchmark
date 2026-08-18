# AI Coding CLI 활용 전략

## 1. 개요

AI Coding CLI는 터미널에서 실행되는 AI Coding Agent로, 개발자의 Repository를 직접 탐색하고 파일을 수정하며 테스트, 빌드, 린트, Git 같은 개발 도구를 함께 사용할 수 있는 작업 환경이다.

일반적인 웹 채팅 기반 AI 사용은 개발자가 필요한 코드를 복사해 붙여넣고 결과를 다시 수동으로 반영하는 방식에 가깝다. 반면 AI Coding CLI는 Repository 내부에서 `탐색 -> 수정 -> 검증 -> 재수정` 루프를 수행할 수 있으므로, 실제 개발 Workflow에 더 직접적으로 연결된다.

이 문서는 OpenAI Codex CLI와 Anthropic Claude Code를 중심으로, AI Coding CLI를 실무 개발 프로세스에 어떻게 배치할지 정리한다.

## 2. AI Coding CLI란?

AI Coding CLI의 핵심 역할은 자연어 요청을 실제 개발 작업 단위로 변환하는 것이다. 단순히 코드 조각을 생성하는 도구가 아니라, 로컬 개발 환경 안에서 Repository Context를 읽고, 변경을 만들고, 명령을 실행하며, 결과를 바탕으로 반복할 수 있는 Agent 실행 환경이다.

### 핵심 기능

| 기능 | 설명 |
|---|---|
| Repository Context 활용 | 현재 프로젝트의 파일 구조, 코드, 설정, 테스트, Git 상태를 참고해 작업한다. |
| 파일 탐색 및 수정 | 관련 파일을 검색하고 읽은 뒤 필요한 파일을 직접 수정한다. |
| Shell Command 실행 | 테스트, 빌드, 린트, 타입체크, Git 명령 등 로컬 명령을 실행할 수 있다. |
| 테스트 실행 | 변경 후 테스트를 실행하고 실패 원인을 다시 분석한다. |
| Git 작업 보조 | diff 확인, 커밋 메시지 초안, PR 설명, 변경 요약을 지원한다. |
| Agentic Coding | 한 번의 답변이 아니라 여러 도구 호출과 검증을 반복하며 작업을 완료한다. |

AI Coding CLI는 특히 코드베이스 탐색, 버그 수정, 테스트 보강, 리팩터링, PR 준비처럼 “파일과 명령을 오가야 하는 작업”에서 효과가 크다.

## 3. Chat 기반 AI 사용과의 차이

| 구분 | 일반 Chat 기반 AI | AI Coding CLI |
|---|---|---|
| 실행 위치 | 브라우저 또는 채팅 앱 | 터미널, 로컬 Repository |
| Context 제공 | 사용자가 코드 일부를 붙여넣음 | Agent가 파일과 Git 상태를 직접 탐색 |
| 변경 반영 | 사용자가 수동 반영 | Agent가 파일을 직접 수정 가능 |
| 검증 | 사용자가 별도 실행 | Agent가 테스트/빌드/린트 실행 가능 |
| 반복 방식 | 질문과 답변 중심 | 탐색, 수정, 검증 루프 중심 |
| 주요 위험 | 부정확한 답변을 사람이 복사 | 잘못된 파일 수정 또는 위험 명령 실행 |
| 적합한 사용 | 설명, 설계 토론, 작은 코드 예시 | 실제 Repository 변경, 테스트, 리뷰 보조 |

AI Coding CLI가 웹 채팅보다 생산성을 높일 수 있는 이유는 Context 전달 비용과 수동 반영 비용을 줄이기 때문이다. 그러나 Agent가 직접 파일과 명령을 다루는 만큼, 권한과 검증 체계가 없으면 위험도 함께 커진다.

## 4. Codex CLI 활용 전략

Codex CLI는 OpenAI의 터미널 기반 Coding Agent다. 공식 문서와 GitHub Repository 기준으로 Codex CLI는 로컬 컴퓨터에서 실행되며, 코드 읽기, 수정, 명령 실행을 통해 기능 구현, 버그 수정, 코드 이해를 돕는 도구로 설명된다.

### 주요 사용 목적

Codex CLI는 다음 작업에 적합하다.

- 신규 코드베이스 구조 파악
- 작은 기능 구현
- 버그 원인 분석과 수정
- 테스트 실패 분석
- 테스트 케이스 추가
- 반복적인 리팩터링
- PR 전 변경 요약과 자체 리뷰
- CLI 기반 자동화 실험

### 기본 작업 방식

권장 작업 흐름은 다음과 같다.

```text
Repository Root에서 Codex 실행
    ↓
작업 목표, 범위, 금지사항, 검증 명령 전달
    ↓
Codex가 관련 파일 탐색
    ↓
수정 계획 또는 변경안 작성
    ↓
파일 수정
    ↓
테스트/린트/타입체크 실행
    ↓
실패 시 원인 분석 후 재수정
    ↓
개발자가 diff 검토
```

좋은 요청 예시는 다음과 같다.

```text
로그인 실패 시 에러 메시지가 표시되지 않는 문제를 원인 분석하고 수정해줘.
관련 테스트를 추가하고 `npm test`로 검증해줘.
인증 정책 파일과 production 설정 파일은 수정하지 마.
```

나쁜 요청 예시는 다음과 같다.

```text
전체 프로젝트를 알아서 개선해줘.
```

AI Coding CLI에는 목표가 구체적일수록 좋다. 특히 수정 범위, 금지 파일, 검증 명령, 기대 동작을 함께 전달해야 한다.

### Repository 이해 방식

Codex CLI는 현재 작업 디렉터리의 파일, 디렉터리 구조, 설정 파일, 테스트, Git 상태를 바탕으로 작업한다. 프로젝트 규칙은 `AGENTS.md`에 정리해 반복적으로 제공할 수 있다.

`AGENTS.md`에 둘 수 있는 내용은 다음과 같다.

```markdown
# Project Rules

## Commands
- Test: npm test
- Lint: npm run lint
- Typecheck: npm run typecheck

## Coding Rules
- Keep public API compatibility.
- Add regression tests for bug fixes.
- Do not add dependencies without approval.

## Safety
- Do not edit production config files.
- Do not run deploy commands.
- Do not read secret files.
```

### 코드 수정 과정

Codex CLI에는 작은 단위의 변경을 맡기는 것이 좋다.

적합한 작업:

- 특정 버그 수정
- 특정 테스트 실패 해결
- 타입 오류 수정
- 한 모듈 안의 리팩터링
- API 변경에 따른 호출부 수정
- 문서와 테스트 보강

주의가 필요한 작업:

- 인증/인가 로직 변경
- 결제/정산 로직 변경
- 데이터 삭제 로직 변경
- DB migration 작성
- 대규모 아키텍처 변경

### 명령 실행 방식

Codex CLI는 로컬 Shell 명령을 실행할 수 있으므로 명령 실행 권한을 단계적으로 부여해야 한다.

| 단계 | 권장 권한 |
|---|---|
| 탐색 | 파일 읽기, `git status`, 검색 명령 |
| 계획 | 수정 없이 계획 작성 |
| 구현 | 지정 범위 내 파일 수정 |
| 검증 | 테스트, 린트, 타입체크 실행 |
| 릴리스 | 사람 승인 전 자동 실행 금지 |

### 개발자가 통제할 수 있는 요소

개발자는 다음 요소를 명시적으로 통제해야 한다.

- 작업 디렉터리
- 수정 가능한 파일 범위
- 실행 가능한 명령
- 네트워크 접근 여부
- 모델과 추론 수준
- 자동 승인 범위
- Git push/merge 허용 여부
- Secret 파일 접근 여부

### Workflow 활용 영역

Codex CLI는 다음 개발 단계에서 활용 가치가 높다.

- 요구사항을 구현 계획으로 정리
- 관련 파일과 호출 흐름 탐색
- 작은 기능 구현
- 테스트 추가
- 실패 테스트 분석
- 변경 diff 요약
- PR 설명 초안 작성
- 반복 수정 자동화

## 5. Claude Code 활용 전략

Claude Code는 Anthropic의 Agentic Coding 도구다. 공식 문서 기준으로 Claude Code는 터미널에서 실행되며, 파일 작업, 검색, Shell 실행, Git, 테스트 실행, 웹 검색, MCP, hooks, subagents 등으로 확장될 수 있다.

### 주요 사용 목적

Claude Code는 다음 작업에 적합하다.

- 코드베이스 구조 파악
- 복잡한 코드 흐름 설명
- 다중 파일 수정
- 테스트 실패 분석
- 리팩터링
- Git workflow 보조
- PR 설명과 문서 작성
- MCP, hooks, subagents 기반 확장형 Workflow

### 기본 작업 방식

Claude Code의 작업 방식은 다음 루프로 이해할 수 있다.

```text
Context 수집
    ↓
작업 수행
    ↓
검증
    ↓
필요 시 반복
```

개발자는 중간에 개입해 방향을 바꿀 수 있다. 따라서 Claude Code에도 Codex CLI와 마찬가지로 목표, 범위, 금지사항, 검증 기준을 명확히 주는 것이 중요하다.

### Repository 이해 방식

Claude Code는 실행된 디렉터리의 프로젝트 파일, 하위 디렉터리, Git 상태, 프로젝트 지시 파일인 `CLAUDE.md`를 활용할 수 있다. 공식 문서에서는 `CLAUDE.md`를 프로젝트별 지시, 관례, Context를 저장하는 파일로 설명한다.

`CLAUDE.md` 예시는 다음과 같다.

```markdown
# Project Context

## Commands
- Test: npm test
- Lint: npm run lint
- Typecheck: npm run typecheck

## Rules
- Do not change database schema without approval.
- Add tests for bug fixes.
- Keep API response shape backward compatible.

## Review Checklist
- Tests pass.
- No secrets are printed.
- Public behavior is documented.
```

### 코드 수정 과정

Claude Code는 여러 도구를 사용해 파일을 읽고, 관련 코드를 찾고, 수정하고, 테스트를 실행하는 방식으로 작업한다.

좋은 요청 예시는 다음과 같다.

```text
결제 실패 시 재시도 로직이 정상 동작하지 않는 원인을 찾아줘.
관련 테스트를 먼저 확인하고, 필요한 경우 테스트를 추가한 뒤 수정해줘.
외부 결제 API 호출은 mock 기반으로만 검증해줘.
```

### 명령 실행 방식

Claude Code는 사용자의 터미널에서 실행 가능한 명령을 사용할 수 있다. 공식 문서 기준으로 권한 모드와 permission rule을 통해 파일 수정과 Shell 실행을 통제할 수 있으며, hooks를 통해 특정 시점에 규칙 검증 명령을 실행할 수도 있다.

### 개발자가 통제할 수 있는 요소

Claude Code 사용 시 통제해야 할 요소는 다음과 같다.

- Permission mode
- 파일 수정 승인 정책
- Shell 명령 승인 정책
- `CLAUDE.md` 기반 프로젝트 규칙
- `.claude/settings.json` 권한 규칙
- hooks 자동 실행 범위
- MCP 서버 연결 범위
- subagent 사용 범위
- checkpoint와 Git diff 검토

### Workflow 활용 영역

Claude Code는 다음 영역에 활용할 수 있다.

- 코드 흐름 설명
- 변경 영향 범위 탐색
- 테스트 작성과 실패 분석
- 다중 파일 리팩터링
- Git 충돌 분석 보조
- PR 설명 작성
- hooks 기반 자동 검증
- MCP 기반 외부 도구 연동
- subagent 기반 병렬 조사

## 6. Codex CLI와 Claude Code 비교

| 기준 | Codex CLI | Claude Code | 실무 판단 |
|---|---|---|---|
| 초기 사용 난이도 | 터미널 중심의 간결한 시작이 가능하다. | 터미널 외에도 IDE, 웹, 데스크톱 등 여러 인터페이스가 제공된다. | CLI 경험이 있는 개발자라면 둘 다 빠르게 시작 가능하다. |
| 코드베이스 이해 | Repository 파일, 설정, Git 상태, `AGENTS.md`를 활용한다. | Repository 파일, Git 상태, `CLAUDE.md`, memory, 확장 기능을 활용한다. | 프로젝트 규칙 파일을 두는 것이 공통적으로 중요하다. |
| 코드 생성 및 수정 | 작은 기능, 버그 수정, 테스트 보강에 적합하다. | 다중 파일 변경과 반복 검증 루프에 적합하다. | 작업 범위를 작게 나누면 두 도구 모두 실무 활용성이 높다. |
| Shell / Tool 실행 | 테스트, 빌드, 린트 등 로컬 명령 실행이 가능하다. | Shell, Git, 테스트, 웹, MCP 등 다양한 도구 사용이 가능하다. | 명령 실행은 항상 승인 정책과 함께 운영해야 한다. |
| Context 관리 | 세션, Repository, `AGENTS.md`, 설정을 활용한다. | 세션, Repository, `CLAUDE.md`, memory, subagents를 활용한다. | 대규모 Repository에서는 모듈 단위 작업 분리가 필요하다. |
| 사용자 통제 가능성 | 권한, sandbox, 승인 흐름, 설정으로 통제한다. | permission mode, settings, hooks, checkpoint로 통제한다. | 도구 기능보다 팀 운영 규칙이 더 중요하다. |
| 반복 작업 자동화 | CLI 기반 반복 실행과 non-interactive 활용 가능성이 있다. | hooks, MCP, subagents로 Workflow 확장이 가능하다. | 초기에는 테스트/리뷰 보조 자동화부터 시작한다. |
| 테스트 및 검증 | 테스트 실행 후 수정 루프에 적합하다. | 테스트 실패 분석과 재검증 루프에 적합하다. | 테스트 통과만으로 최종 승인을 대체하면 안 된다. |
| Git Workflow | diff 요약, 커밋 메시지, PR 준비 보조에 적합하다. | Git 상태 이해, 충돌 분석, 커밋/PR 보조에 적합하다. | push, merge는 사람 승인 영역으로 둔다. |
| 대규모 Repository | 명확한 범위와 검색 전략이 필요하다. | Context 관리와 역할 분리가 중요하다. | worktree, 모듈 범위, 체크리스트를 함께 사용한다. |
| 실무 적용성 | 터미널 중심 개발팀과 Codex 기반 자동화 실험에 적합하다. | 확장형 Agent workflow와 외부 도구 연동 실험에 적합하다. | 경쟁 관계뿐 아니라 역할 분리 방식으로 함께 쓸 수 있다. |

## 7. 실제 개발 Workflow 적용 방안

권장 Workflow는 다음과 같다.

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

| 단계 | AI에게 맡기기 적합한 작업 | 사람이 확인해야 하는 작업 | 자동화하면 위험한 작업 |
|---|---|---|---|
| 요구사항 확인 | 요구사항 요약, 모호한 지점 질문 도출 | 제품 의도, 우선순위, 수용 기준 확정 | 불명확한 요구사항을 임의 확정 |
| 구현 계획 | 영향 범위 후보, 구현 순서, 테스트 전략 초안 | 아키텍처 방향, API 호환성, 일정 판단 | 대규모 구조 변경 자동 결정 |
| 코드 탐색 | 관련 파일 검색, 호출 흐름 설명 | 도메인 의미와 정책 해석 | 보안/정책 로직을 추측으로 단정 |
| 코드 작성/수정 | 작은 기능, 버그 수정, 테스트 추가 | 변경 범위와 public behavior 확인 | DB, auth, billing 자동 변경 |
| 테스트 | 테스트 실행, 실패 로그 분석, 회귀 테스트 추가 | 테스트가 요구사항을 검증하는지 판단 | 실패 테스트 삭제 또는 완화 |
| 코드 리뷰 | diff 요약, 위험 지점 탐색 | 최종 승인, 설계 판단 | Agent 리뷰만으로 merge |
| Git Commit | 커밋 메시지 초안, 변경 요약 | 커밋 단위 확정 | 자동 commit/push |
| Pull Request | PR 설명 초안, 체크리스트 생성 | 리뷰어 지정, merge 판단 | 자동 merge/release |

## 8. 권한 및 안전성

AI Coding CLI 운영 원칙은 “읽기는 넓게, 쓰기는 좁게, 실행은 승인 기반”이다.

### 권한 정책

| 영역 | 권장 정책 |
|---|---|
| 명령 실행 권한 | 테스트, 린트, 타입체크 등 안전 명령부터 허용한다. |
| 파일 수정 범위 | 작업 대상 디렉터리와 테스트 파일 중심으로 제한한다. |
| Secret / 환경변수 | `.env`, credential, token, key 파일 접근을 금지한다. |
| Production 접근 | Production DB, cloud, deploy 명령은 금지한다. |
| 위험 명령어 | 삭제, 강제 reset, 배포, infra 변경 명령은 승인 없이는 차단한다. |
| Git push / merge | 자동 실행 금지, 사람 승인 필수로 둔다. |
| 자동 테스트 | Agent가 실행할 수 있게 하되 결과 해석은 사람이 확인한다. |
| Human Review | 모든 PR은 사람 리뷰를 통과해야 한다. |
| 작업 로그 | 작업 요청, 변경 파일, 실행 명령, 테스트 결과를 기록한다. |

### 기본 차단 명령

다음 명령은 기본적으로 Agent가 자동 실행하지 못하게 해야 한다.

```text
rm -rf
git reset --hard
git push
git merge
git rebase
npm publish
docker push
kubectl apply
kubectl delete
terraform apply
terraform destroy
aws/gcloud/az production 명령
production database migration
```

### Secret 보호 규칙

- Agent에게 Secret 값을 직접 입력하지 않는다.
- `.env`, `.env.production`, credential 파일은 읽기 금지한다.
- 로그에 API key, token, 인증 헤더가 출력되지 않도록 확인한다.
- 외부 API는 mock 또는 sandbox 환경으로 검증한다.
- Production Secret은 CI/CD Secret Store에서만 사용한다.

## 9. Human-in-the-loop 전략

AI Coding CLI는 작업자 역할을 맡고, 개발자는 의사결정자와 검토자 역할을 유지해야 한다.

### 사람이 반드시 판단해야 하는 영역

- 요구사항의 최종 의미
- 아키텍처 변경
- 인증/인가 정책
- 결제/정산 로직
- 데이터 삭제와 migration
- 외부 API 계약 변경
- 보안 정책
- 성능 trade-off
- 배포 여부
- 장애 대응 판단

### Agent에게 맡기기 좋은 영역

- 반복적인 코드 수정
- 테스트 보강
- 실패 로그 분석
- 문서 초안 작성
- 리팩터링 후보 탐색
- 코드 리뷰 체크리스트 생성
- 변경 영향 범위 조사
- 작은 버그 수정

### 검증 절차

1. Agent가 변경한 diff를 확인한다.
2. 테스트, 린트, 타입체크를 실행한다.
3. 핵심 요구사항은 수동 또는 통합 테스트로 확인한다.
4. 보안, 권한, 데이터 변경은 별도 리뷰어가 확인한다.
5. PR에는 Agent 사용 여부와 검증 명령을 기록한다.

PR 템플릿 예시는 다음과 같다.

```markdown
## Summary
- 

## Agent Usage
- Tool:
- Scope:
- Files changed by agent:

## Verification
- [ ] Unit tests
- [ ] Integration tests
- [ ] Typecheck
- [ ] Lint
- [ ] Manual review

## Risk Areas
- [ ] Auth
- [ ] Payment
- [ ] Database
- [ ] External API
- [ ] Deployment
```

## 10. 핵심 질문에 대한 판단

### Q1. AI Coding CLI는 웹 채팅보다 생산성을 높일 수 있는가?

높일 수 있다. 특히 Repository 탐색, 다중 파일 수정, 테스트 실행, 실패 원인 분석처럼 코드와 도구를 오가야 하는 작업에서 효과가 크다.

다만 생산성 향상은 Agent 권한을 넓게 주는 것만으로 발생하지 않는다. 작은 작업 단위, 명확한 검증 명령, 사람의 diff 리뷰가 함께 있어야 한다.

### Q2. Repository 내부에서 직접 작업하는 장점과 위험은 무엇인가?

장점:

- Context 누락이 줄어든다.
- 여러 파일에 걸친 변경을 처리할 수 있다.
- 테스트 결과를 바탕으로 수정 루프를 반복할 수 있다.
- 개발자의 복사/붙여넣기 비용이 줄어든다.

위험:

- 잘못된 파일을 수정할 수 있다.
- 테스트를 통과시키기 위해 잘못된 방향으로 코드를 바꿀 수 있다.
- Secret 또는 Production 리소스에 접근할 수 있다.
- 위험 명령을 실행할 수 있다.
- 변경 내용을 사람이 이해하지 못한 채 merge할 수 있다.

### Q3. 개발자는 Agent에게 어느 수준까지 권한을 부여해야 하는가?

권장 권한 단계는 다음과 같다.

| 단계 | 권한 | 사용 상황 |
|---|---|---|
| Level 1 | 읽기 전용 | 코드 탐색, 설명, 리뷰 |
| Level 2 | 제한된 파일 수정 | 작은 버그 수정, 테스트 추가 |
| Level 3 | 안전 명령 실행 | 테스트, 린트, 타입체크 |
| Level 4 | Git commit 보조 | 커밋 메시지 초안, 로컬 커밋 전 검토 |
| Level 5 | 외부 시스템 연동 | Issue, PR, MCP, CI 연동 |
| 금지 | Production 변경, 자동 merge, 자동 배포 | 사람 승인 필수 |

초기 도입은 Level 1 또는 Level 2로 시작하고, 프로젝트 신뢰도와 검증 체계가 갖춰진 뒤 단계적으로 확대해야 한다.

### Q4. AI Coding Agent가 작성한 코드는 어떻게 검증해야 하는가?

검증은 다음 순서로 진행한다.

1. 변경 diff 확인
2. 테스트 실행
3. 린트와 타입체크 실행
4. 핵심 요구사항 수동 확인
5. 보안/권한/데이터 영향 검토
6. PR 리뷰
7. CI 결과 확인

중요한 원칙은 “테스트 통과 = 정답”으로 보지 않는 것이다. 테스트가 부족하면 잘못된 코드도 통과할 수 있으므로, Agent가 테스트를 추가하더라도 테스트의 의미는 사람이 검토해야 한다.

### Q5. Codex CLI와 Claude Code는 경쟁 관계인가, 함께 사용할 수 있는가?

두 도구는 같은 범주의 제품이므로 경쟁 관계로 볼 수 있다. 그러나 실무에서는 역할을 나누어 함께 사용할 수도 있다.

가능한 역할 분리:

| 단계 | 사용 방식 |
|---|---|
| 코드 탐색 | 한 도구로 구조와 영향 범위 요약 |
| 구현 | 하나의 도구를 주 작업 Agent로 선택 |
| 검증 | 다른 도구를 리뷰 Agent처럼 사용 |
| 문서화 | 변경 요약, PR 설명, 운영 문서 작성 |
| 실험 | 동일 Task를 별도 브랜치 또는 worktree에서 비교 |

주의할 점은 같은 파일을 두 Agent가 동시에 수정하지 않도록 하는 것이다. 병렬 사용 시에는 별도 브랜치, worktree, 명확한 작업 범위를 사용해야 한다.

## 11. Multi-Agent 및 CI/CD 확장 구조

이번 단계에서는 Multi-Agent와 CI/CD를 구현하지 않는다. 다만 향후 확장을 고려하면 Agent 역할을 SDLC 단계별로 분리하는 구조가 적절하다.

### 권장 Agent 역할

| 역할 | 책임 | 자동화 가능 수준 |
|---|---|---|
| Requirement Agent | 이슈 요약, 수용 기준 정리 | 낮음 |
| Planning Agent | 구현 계획, 영향 범위 도출 | 중간 |
| Coding Agent | 코드 수정, 테스트 작성 | 중간 |
| Test Agent | 테스트 실행, 실패 분석 | 높음 |
| Review Agent | diff 리뷰, 위험 탐지 | 중간 |
| Security Agent | Secret, 권한, 취약점 점검 | 중간 |
| Release Agent | 릴리스 노트, 배포 체크리스트 | 낮음 |

### 확장 Workflow

```text
GitHub Issue
    ↓
Requirement Agent: 요구사항 정리
    ↓
Planning Agent: 구현 계획 작성
    ↓
Human Approval
    ↓
Coding Agent: 브랜치 또는 worktree에서 코드 수정
    ↓
Test Agent: 테스트/린트/타입체크 실행
    ↓
Review Agent: diff 리뷰
    ↓
Security Agent: 위험 영역 점검
    ↓
Human Review
    ↓
Pull Request 생성
    ↓
CI 실행
    ↓
Human Approval
    ↓
Merge
    ↓
CD는 별도 승인 후 실행
```

### 초기 자동화 대상

- 테스트 실행
- 린트 실행
- 타입체크 실행
- PR 요약 생성
- 변경 파일 목록 생성
- 위험 영역 체크리스트 생성
- 문서 업데이트 후보 제안

### 자동화하면 안 되는 대상

- Production 배포 자동 승인
- DB migration 자동 적용
- 보안 정책 자동 변경
- 결제/권한 로직 자동 merge
- 장애 상황 자동 판단
- Secret 조회 또는 출력

## 12. 운영 규칙 초안

팀에서 AI Coding CLI를 도입할 때 다음 규칙을 기본값으로 둔다.

1. 모든 Agent 작업은 Git branch 또는 worktree에서 수행한다.
2. 작업 전 `git status`를 확인한다.
3. Agent에게 요구사항, 범위, 금지사항, 검증 명령을 함께 전달한다.
4. Secret 파일과 Production 설정은 읽기/수정 금지한다.
5. 테스트 삭제 또는 완화는 사람 승인 없이는 금지한다.
6. DB migration, auth, payment 변경은 별도 리뷰를 요구한다.
7. `git push`, `merge`, 배포 명령은 자동 실행하지 않는다.
8. Agent 변경 사항은 PR에 명시한다.
9. CI 통과와 사람 리뷰를 모두 merge 조건으로 둔다.
10. 반복되는 작업 규칙은 `AGENTS.md`, `CLAUDE.md`, PR 템플릿으로 문서화한다.

## 13. 결론

AI Coding CLI는 단순한 코드 생성 도구가 아니라 개발 Workflow 안에서 탐색, 수정, 검증, 리뷰를 반복하는 Agent 실행 환경이다.

실무 적용의 핵심은 특정 도구를 선택하는 것보다 운영 방식을 설계하는 것이다. 작은 작업 단위, 명확한 권한, 검증 가능한 테스트, Human Review가 결합될 때 AI Coding CLI는 실제 개발 생산성을 높일 수 있다.

권장 도입 순서는 다음과 같다.

```text
1. 읽기 전용 코드 탐색
2. 테스트 실패 분석
3. 작은 버그 수정
4. 테스트 보강
5. PR 전 리뷰 보조
6. 반복 작업 자동화
7. Issue / PR 연동
8. Multi-Agent 역할 분리
9. CI 자동 검증
10. Human Approval 기반 CD 확장
```

최종 목표는 하나의 Agent가 모든 개발 단계를 대체하는 것이 아니다. Software Development Lifecycle의 각 단계에 적합한 Agent 역할과 권한을 배치하고, 사람이 중요한 판단을 유지하는 구조를 만드는 것이다.

## 참고 자료

- [OpenAI Codex CLI 공식 문서](https://learn.chatgpt.com/docs/codex/cli)
- [OpenAI Codex GitHub Repository](https://github.com/openai/codex)
- [Claude Code 공식 Overview](https://code.claude.com/docs/en/overview)
- [Claude Code 작동 방식](https://code.claude.com/docs/en/how-claude-code-works)
- [Claude Code 권한 문서](https://code.claude.com/docs/en/permissions)
- [Claude Code Hooks 문서](https://code.claude.com/docs/en/hooks)

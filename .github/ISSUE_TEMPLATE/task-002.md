---
name: Task 002 - User creation stability
about: Benchmark issue for Codex CLI and Claude Code
title: "[Benchmark] 사용자 생성 API 안정성 개선"
labels: benchmark
assignees: ''
---

## 목적

Codex CLI와 Claude Code에 동일하게 제공하는 Benchmark Issue입니다.

전체 요구사항은 다음 문서를 기준으로 합니다.

```text
benchmark/task-002.md
```

## 핵심 요구사항

- 이메일 중복 생성 방지
- 이메일 비교 시 대소문자 무시
- 중복 이메일 → HTTP 409 / `Email already exists`
- 사용자 삭제 후 생성 시 ID 충돌 방지
- 신규 테스트 추가
- 기존 테스트 전체 통과
- README 반영

## 제한

- DB/ORM 도입 금지
- Framework 교체 금지
- Issue와 관계없는 대규모 리팩터링 금지
- 가능한 경우 신규 Dependency 추가 금지

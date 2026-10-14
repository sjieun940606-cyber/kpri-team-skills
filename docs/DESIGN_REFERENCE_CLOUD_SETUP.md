# 클라우드 환경에서 공통 디자인 지침 사용

지침: plugins/kpri/skills/design-reference/SKILL.md
참고 자료: 같은 디렉터리의 references/sources.md
검토 브랜치: codex/design-reference-20261015

## Codex
이 브랜치를 체크아웃한 뒤 해당 실행 환경이 실제로 검색하는 스킬 디렉터리를 확인한다.
설치기는 명시한 디렉터리에만 로컬 파일을 복사하며 기존 내용이 다르면 중단한다.

```sh
git clone --branch codex/design-reference-20261015 --single-branch https://github.com/sjieun940606-cyber/kpri-team-skills.git /workspace/design-reference-skills
python3 /workspace/design-reference-skills/scripts/install-design-reference.py --skills-dir /workspace/.agents/skills
```

위 /workspace/.agents/skills 예시는 실행 환경에서 그 경로를 검색할 때 사용한다. 다른 경로를 사용하는 환경은 --skills-dir에 실제 경로를 지정한다. 설치 성공과 에이전트의 스킬 검색 성공은 별도로 확인한다.
필요하면 프로젝트 AGENTS.md에 아래 문장을 추가하고 기존 지침은 보존한다.

> 디자인 관련 작업은 설치된 design-reference 스킬을 읽고 수행한다. 최신 사용자 요청과 프로젝트의 확정된 디자인 규칙을 우선한다.

## Claude Code
이 브랜치의 플러그인에는 /kpri:design-reference 스킬이 포함된다. main의 마켓플레이스 설치에는 병합 전까지 포함되지 않는다. 해당 브랜치의 로컬 플러그인을 로드하거나 병합 후 기존 플러그인을 업데이트한다.

## 여러 클라우드 세션
클라우드 세션은 서로 다른 파일 시스템과 실행 환경을 쓸 수 있다. 한 세션에 복사했다고 다른 세션에 자동 설치되지는 않는다.
각 환경의 설정 스크립트에 검토한 버전의 설치 단계를 등록하고 다시 시작한 뒤 스킬이 검색되는지 확인한다. 이후에도 사용자 홈/설정 파일과 기존 스킬을 덮어쓰지 않는다.
현재 계정 전체 환경의 설정 스크립트 수정 및 다른 세션 파일 쓰기 도구는 제공되지 않았다. 따라서 GitHub 브랜치의 준비와 전체 세션 활성화를 구분해야 한다.

## 검증과 복구
설치 경로에 SKILL.md 및 references/sources.md가 있는지 확인하고 새 에이전트 턴에서 스킬 목록을 확인한다.
서로 다른 파일이 이미 있으면 설치기는 교체하지 않는다. 검토 후 버전별 별도 디렉터리를 사용한다.
적용을 취소하려면 이 설치 단계와 본인이 추가한 AGENTS.md 문장만 제거하고, 설치한 design-reference 폴더를 보관하거나 삭제한다.

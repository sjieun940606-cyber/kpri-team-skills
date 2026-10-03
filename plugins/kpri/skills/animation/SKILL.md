---
name: animation
description: 교육용 짧은 애니메이션 영상(MP4)을 유료 영상 구독 없이 내 PC에서 만든다. HyperFrames(HTML→MP4, 무료)로 캐릭터를 움직이고 자막·숨쉬기 원 같은 안내를 넣는다. Canva 캐릭터 시트를 오려 쓰거나, 템플릿의 SVG 캐릭터(하루)로 시작한다. "애니메이션 만들어줘", "교육 영상 만들어줘", "캐릭터 움직이는 영상", "감정조절 영상", "이 장면을 영상으로" 같은 요청에 사용.
argument-hint: "[대상] [길이] [주제] (예: 초등 저학년 1분 화날 때 숨쉬기)"
---

# 교육용 애니메이션 만들기

요청: `$ARGUMENTS`

HyperFrames(HeyGen, Apache-2.0, 무료)로 HTML 장면을 MP4로 렌더링한다. AI가 그림을 직접 움직이는 방식(Weave·Runway)이 아니라, 그림 조각을 종이인형처럼 움직이는 **컷아웃 애니메이션**이다. 이동·확대·통통 튀기·표정 바꾸기·화면 이동은 되지만 걷기처럼 팔다리가 자연스럽게 움직이는 장면은 어렵다. 처음에 이 점을 한 줄로 알린다.

## 0. 준비 (처음 한 번)
- **PowerShell**에서 확인: `node --version`(22 이상), `ffmpeg -version`. 없으면 `winget install OpenJS.NodeJS.LTS`, `winget install Gyan.FFmpeg` 후 PowerShell을 다시 연다.
- **PowerShell**에서 사용 통계 보내기 끄기: `npx hyperframes telemetry disable`
- (선택) HyperFrames 공식 스킬까지 쓰려면 **클로드코드 입력칸**에:
  ```
  /plugin marketplace add heygen-com/hyperframes
  /plugin install hyperframes@hyperframes
  ```
- Canva 그림을 오려 쓰면 **PowerShell**에서 `pip install pillow numpy`

## 1. 확인할 것 (한 번에 표로 묻기)
아직 정해지지 않은 것만 묻는다.

| 항목 | 예 | 기본값 |
|---|---|---|
| 대상 | 초등 저학년 / 중학생 / 교사 연수 | (꼭 물음) |
| 길이 | 10초 장면 하나 / 1분 이야기 | (꼭 물음) |
| 주제·메시지 | 화날 때 멈추기·숨쉬기·말하기 | (꼭 물음) |
| 캐릭터 | Canva 캐릭터 시트 PNG / 템플릿의 하루(SVG) | 템플릿의 하루 |
| 화면 | 16:9 수업 화면 / 9:16 세로 | 16:9 (1920×1080) |
| 소리 | 없음(자막만) / 직접 녹음한 목소리 파일 | 없음 |

## 2. 장면표 먼저 (승인 전에는 만들지 않는다)
장면표(장면 | 초 | 화면 | 자막 | 움직임)를 보여 주고, 맨 아래에 초 합계가 정한 길이와 맞는지 적는다. 자막은 대상 학년이 읽을 수 있는 낱말로, 한 번에 한 줄. 사용자가 "좋아" 하기 전에는 파일을 만들지 않는다.

## 3. 캐릭터 준비
- **템플릿의 하루(SVG)**: `template/index.html` 안에 그려져 있다. 옷 색·머리 모양은 `fill` 값과 머리 `path`만 바꾸면 된다.
- **Canva 캐릭터 시트**: Canva 무료 요금제는 투명 배경 PNG를 내보낼 수 없다. 흰 배경 PNG로 받은 뒤 오린다.
  ```
  python "${CLAUDE_SKILL_DIR}/scripts/cutout.py" 하루_시트.png -o 결과/[주제]/assets/haru
  ```
  `preview.png`의 번호를 보고 조각 이름을 바꾼다(예: `haru-front.png`, `haru-angry.png`). 두 그림이 한 조각으로 붙어 나오면 Canva에서 그림 사이를 띄운 뒤 다시 받는다. 장면에서는 `<img>`로 겹쳐 두고 표정은 얼굴 그림의 `opacity`를 바꿔 갈아 끼운다.

## 4. 만들기
1. `npx hyperframes init 결과/[주제]`로 프로젝트를 만든다.
2. `${CLAUDE_SKILL_DIR}/template/index.html`과 `template/fonts/`를 프로젝트에 복사하고 장면표대로 고친다. 템플릿은 "숨쉬기" 10초 장면(먹구름 → 들이마시기·내쉬기 → 해가 뜸)이다.
3. 지킬 규칙(어기면 렌더가 깨진다):
   - 타임라인은 하나: `gsap.timeline({ paused: true })`를 만들어 `window.__timelines["main"]`에 넣는다.
   - 루트 `data-duration`이 영상 길이다. 장면이 길어지면 같이 늘린다.
   - `Math.random()`·`Date.now()`를 쓰지 않는다. 반복 움직임은 `repeat` 횟수를 정한다(무한 반복 금지).
   - 처음 상태는 CSS `transform` 대신 `gsap.fromTo`로 준다.
   - 글꼴은 `fonts/` 안 파일을 `@font-face`로 불러온다(주아체 들어 있음).
   - 숫자 세기(1·2·3)처럼 글자가 바뀌는 곳은 글자마다 요소를 따로 두고 `tl.set(..., { opacity })`로 바꾼다.

## 5. 점검 → 미리보기 → 렌더
1. `npx hyperframes check` — 오류 0개가 될 때까지 고친다. 팔 들기처럼 어깨를 축으로 돌리는 곳의 `rotation_pivot` 경고는 의도한 것이면 넘어간다.
   - `request_failed ... gsap`가 나오면(회사 프록시 등) `curl -o lib/gsap.min.js https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`로 받아 `<script src="lib/gsap.min.js">`로 바꾼다.
2. `npx hyperframes snapshot --at 1,3,5,…`(장면마다 한 번) → `snapshots/contact-sheet.jpg`를 직접 보고 사용자에게도 보여 준다.
3. 사용자가 승인하면 렌더: `npx hyperframes render --quality looks --output 결과/[주제].mp4`
4. `ffprobe -v error -show_entries format=duration 결과/[주제].mp4`로 길이가 장면표와 맞는지 확인한다.

만든 뒤 표로 점검해 같이 보여 준다(항목 | 통과/확인 필요).
- 길이 = 장면표 합계
- 자막 맞춤법, 대상에게 어려운 낱말
- 학생·강사 실명, 학교 이름, 학생 사진·목소리가 들어가지 않았는지
- 남의 캐릭터(만화·애니메이션 주인공)를 흉내 내지 않았는지

## 지킬 것
- **내 PC에서만 렌더한다.** 자료를 외부로 보내는 HyperFrames 기능(`publish` 공유 링크, `cloud`·`lambda`·`cloudrun` 렌더, `auth`, `tts`, `feedback`, HeyGen·ElevenLabs·Gemini 키를 쓰는 기능)은 쓰지 않는다. 꼭 필요하면 무엇이 밖으로 나가는지 말하고 먼저 묻는다.
- 결과는 `결과` 폴더에만 저장한다. 원본 그림은 고치지 않는다.
- 다른 영상 도구(Remotion·Manim)와 비교한 결과는 `references/tools.md`에 있다.
- 마지막 줄에 다음 할 일을 한 줄로 안내한다. (예: `→ 다음 장면(말하기)도 만들까요?` / `→ 목소리 파일을 넣을까요?`)

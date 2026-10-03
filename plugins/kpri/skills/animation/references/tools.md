# 애니메이션 영상 도구 검증 결과

`/kpri:tool-check` 순서대로 확인하고, 클라우드 PC에서 같은 "숨쉬기" 장면을 실제로 만들어 비교했다.

## 한눈에

| 도구 | 판정 | 방식 | 비용 | 시험 결과 |
|---|---|---|---|---|
| HyperFrames (HeyGen) | ✅ 우리 팀 추천 | HTML·SVG·GSAP → MP4 | 무료(Apache-2.0), 상업용 제한 없음 | 10초 1080p를 13초에 렌더. 기존 웹 애니메이션 코드를 그대로 옮김. 점검 명령이 글자 대비 문제까지 잡아 줌 |
| Remotion | ⚠️ 필요한 사람만 | React 코드 → MP4 | 개인·3명 이하 팀·비영리만 무료, 4명 이상 회사는 유료(좌석당 월 $25~) | 6초 1080p를 12초에 렌더. 결과는 비슷하지만 회사 규모에 따라 라이선스 필요 |
| Manim (Yusuke710/manim-skill) | ⛔ 이 용도엔 깔지 않음 | 파이썬 수학 애니메이션 | 무료(MIT) | 렌더는 되지만 도형·수식용이라 캐릭터 이야기 영상에 맞지 않음. 설치에 Pango 개발 라이브러리 필요 |

## 카드

```
HyperFrames — HTML로 장면을 쓰면 MP4 영상이 나오는 도구          [✅ 우리 팀 추천]
무엇을 하나: HTML·CSS·SVG와 GSAP 애니메이션을 한 장씩 찍어 MP4로 만든다. 자막·도형·그림 조각을 움직이는 교육 영상에 맞다.
설치: (PowerShell) npx hyperframes telemetry disable
      (클로드코드 입력칸, 선택) /plugin marketplace add heygen-com/hyperframes → /plugin install hyperframes@hyperframes
우리 팀: 감정조절·진로 캠프 도입 영상, 숨쉬기 안내 영상, 강의 PPT에 넣을 짧은 장면.
주의: 사용 통계가 기본으로 켜져 있어 위 명령으로 끈다. publish·cloud 렌더·TTS는 자료를 HeyGen 등 외부로 보내므로 쓰지 않는다. 스킬이 20개가 넘어 큰 편.
확인 기준일: 2026-10-03
```

```
Remotion — React로 영상을 만드는 도구                            [⚠️ 필요한 사람만]
무엇을 하나: React 컴포넌트로 장면을 만들고 MP4로 렌더한다. 공식 스킬 모음(remotion-dev/skills)이 있다.
설치: (PowerShell) npx create-video@latest --yes --blank --no-tailwind 프로젝트이름
      스킬: npx skills add remotion-dev/skills
우리 팀: HyperFrames로 충분하다. 회사 인원이 4명 이상이면 Company License가 필요하다.
주의: 라이선스 조건(remotion.dev/docs/license/pricing)을 먼저 확인한다.
확인 기준일: 2026-10-03
```

```
Manim 스킬 — 3Blue1Brown식 수학 애니메이션                         [⛔ 이 용도엔 깔지 않음]
무엇을 하나: 파이썬으로 도형·수식·그래프가 움직이는 영상을 만든다.
설치: (PowerShell) pip install manim  ※ 윈도우는 MiKTeX 등 추가 설치가 필요할 수 있음
우리 팀: 수학·통계 설명 영상이 필요할 때만. 캐릭터 이야기 영상에는 맞지 않는다.
주의: 개인 저장소(Yusuke710/manim-skill, MIT). 훅·외부 전송은 없음.
확인 기준일: 2026-10-03
```

## 확인한 것
- 세 저장소 모두 클로드코드 훅(`hooks.json`)과 `curl | bash` 설치가 없다.
- HyperFrames 저장소는 Anthropic 공식 플러그인 목록(`claude-plugins-official`)에 `hyperframes` 항목으로 올라 있고, 마켓 이름·플러그인 이름(`hyperframes@hyperframes`)이 설치 명령과 맞다.
- HyperFrames에서 API 키를 요구하는 곳은 모두 선택 기능이다(HeyGen 클라우드 렌더·TTS, ElevenLabs TTS, Gemini 이미지 설명, Figma 가져오기). 내 PC 렌더에는 키가 필요 없다.
- Canva 무료 요금제는 투명 배경 PNG 내보내기가 막혀 있어 `scripts/cutout.py`로 흰 배경을 지운다.

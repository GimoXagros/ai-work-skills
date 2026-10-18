# v2026.10.18.1 — 외부 스킬·플러그인 통합 관리

요청한 23개 링크(22개 저장소)를 검토하고, 기존 33개에서 **독립 스킬 64개**로 관리 범위를 확장했습니다. 공식 Codex 플러그인 5개와 GSD 생성 스킬 72개는 별도 설치 체계로 함께 관리합니다.

## 주요 변경

- task-observer, UI UX Pro Max, agent-browser, Firecrawl build 5개를 Codex 환경에 맞춰 보완했습니다.
- Karpathy, taste, find-skills, mcp-builder, frontend-design, Claude 자동화 추천, Remotion 12개를 원본 커밋으로 고정했습니다.
- Headroom, Graphify, yt-dlp, Whisper, FFmpeg용 독립 안내 스킬을 추가했습니다. 원본 프로젝트의 공식 스킬로 표시하지 않습니다.
- ECC 2.2.3, Claude-Mem 14.0.1, Ponytail 5.3.2, Superpowers 7.0.0, HyperFrames 0.8.171의 공식 플러그인을 고정 커밋 marketplace로 관리합니다.
- GSD Core 1.17.0은 공식 Codex 변환 설치기로 설치하고 기존 설정·에이전트·훅을 백업합니다.
- Windows 실행 도구 설치기, npm 의존성 lock, Node·FFmpeg 다운로드 SHA-256 검증, 기존 사용자 PATH 보존을 추가했습니다.
- kr-patch-qa 원본 HEAD는 기존 pin과 같아 기존 래퍼를 유지했습니다.

## 설치·업데이트

```powershell
git pull --ff-only
python -X utf8 install.py
python -X utf8 setup_tools.py
python -X utf8 setup_integrations.py --install --plugins --user-path
```

변경 후 Codex와 터미널을 다시 시작합니다. ZIP은 실행 파일·가상환경·모델·인증 정보를 포함하지 않으며 최초 설치에 인터넷이 필요합니다. 실행 도구 자동 설치는 Windows x64 기준입니다.

## 검증

- 단위·회귀 검사 53개 통과.
- 현재 PC 독립 스킬 64개와 저장소/고정 캐시의 파일 해시 일치.
- 공식 플러그인 5개 설치·활성 등록 확인, GSD 생성 스킬 72개 확인.
- 기존 Codex 설정값 제거·변경 없음.
- UI/UX 로컬 검색, taste 데이터 목록 조회, Graphify 합성 코드 분석 성공.
- FFmpeg 합성 영상 1초 인코딩·길이 확인·전체 디코딩 성공.
- Headroom, agent-browser, Firecrawl, HyperFrames, yt-dlp 버전 확인. Whisper CLI import/help 성공.

## 사용 조건

플러그인 등록과 메모리 수집·훅 실행은 다릅니다. Firecrawl 인증, Claude-Mem provider/훅 신뢰, Headroom 프록시 전환, Whisper 모델 다운로드는 별도이며 자동으로 완료했다고 표시하지 않습니다. 실제 웹 자동화·영상 렌더·음성 인식 품질·게임 호환성까지 검증한 릴리스가 아닙니다.

전체 요청별 결과와 제한 사항: [통합 관리 안내](docs/INTEGRATIONS.md). 기존 Remotion 플러그인과 직접 설치 스킬 등은 중복 노출될 수 있습니다.

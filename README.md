# YouTube Auto Summarizer (Agent-Assisted)

유튜브 영상의 대본을 추출하여, **ChatGPT용 최적화 프롬프트 파일**을 자동으로 생성해주는 도구입니다.

## 주요 기능
- **자동 모니터링**: 
    1. **로컬 실행**: `python main.py` (간단한 루프)
    2. **Airflow 자동화**: `dags/youtube_summary_dag.py` (엔터프라이즈급 스케줄링)
- **대본 추출**: 영상의 영어 자막을 자동으로 다운로드합니다.
- **프롬프트 생성**: `SYSTEM_PROMPT.md`에 정의된 페르소나와 대본을 결합하여, 바로 사용할 수 있는 `.txt` 파일을 만듭니다.

## 폴더 구조
- `src/`: 핵심 소스 코드 (`monitor.py`, `transcript.py`, `generator.py`)
- `config/`: 설정 파일 (`config.yaml`)
- `prompts/`: 프롬프트 템플릿 (`SYSTEM_PROMPT.md`)
- `output/`: 생성된 프롬프트 파일이 저장되는 곳 (`prompt_[videoId].txt`)
- `dags/`: Airflow DAG 파일 (`youtube_summary_dag.py`)

## 사용 방법

### 1. 설정
`config/config.yaml` 파일에 모니터링할 **Channel ID**가 입력되어 있습니다.
(기본값: `@loresowhat`의 Channel ID `UCtoNXlIegvxkvf5Ji8S57Ag`)

### 2. 실행 (두 가지 방법)

#### A. 로컬 실행 (간단)
터미널에서 바로 실행하면 1시간마다 확인합니다.
```bash
python main.py
```

#### B. Airflow 연동 (추천)
Airflow를 사용 중이라면 아래 DAG 파일을 Airflow DAG 폴더로 복사(또는 링크)하세요.
- 원본: `C:\vscode\eng_youtube_transfer\eng_youtube_transfer\dags\youtube_summary_dag.py`
- 대상: `C:\vscode\airflow\dags\` (사용자 환경에 맞게 조정)

**주의**: DAG 파일 내 `PROJECT_PATH` 변수가 이 프로젝트의 경로(`C:\vscode\eng_youtube_transfer\eng_youtube_transfer`)를 정확히 가리키고 있는지 확인하세요.

## 결과 활용
- `output/` 폴더에 생성된 `prompt_[VIDEO_ID].txt` 내용을 복사해서 **ChatGPT**에 붙여넣으세요.

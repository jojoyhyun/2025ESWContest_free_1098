# 🚀 2025 ESWContest 자유공모 1098_찌리리공
> 본 프로젝트는 팀 찌리리공 1098의 2025 임베디드 소프트웨어 경진대회 출품작입니다.

<br>

# 💡 Sent-Light : AI 기반 실시간 음성 감정 분석 및 시각화 시스템
✨
'Sent-Light'는 사용자의 감정을 섬세하게 분석하고, 이를 직관적인 '빛'의 형태로 시각화하여 응답합니다. 사용자는 이를 통해 자신의 감정을 객관적으로 바라보며 스스로를 이해하고, 따뜻한 연결감을 느끼게 됩니다.
## 📖 프로젝트 소개
 현대 사회, 특히 대한민국은 OECD 국가 중 우울감과 정신 건강 문제에서 가장 높은 수치를 기록하는 등, 마음의 감기를 앓고 있습니다. 급격한 사회 변화와 경쟁 속에서 많은 사람들이 일상적인 스트레스와 고립감을 느끼지만, 정작 자신의 속마음을 터놓을 곳을 쉽게 찾을 수 없는 것이 현실입니다.
 
 이러한 상황 속에서 저희는 일본의 반려 로봇 'LOVOT' 사례에 주목하였습니다. LOVOT은 단순한 기계를 넘어 사용자와 정서적 교감을 나누며 큰 사랑을 받고 있습니다. 이를 통해 기술이 인간의 외로움을 달래고 따뜻한 위로를 줄 수 있다는 확신과 함께, 임베디드 소프트웨어를 통해 이 문제를 해소할 수 있다는 가능성을 발견하였습니다.

 내 이야기를 털어놓는 것만으로도 상대방에게 부담이 될까봐 망설였던 경험을 통해, 저희의 프로젝트는 이 심리적 장벽을 낮추는 것에서 시작되었습니다. 언제 어디서든, 가만히 들어주고 나를 위해 반응해주는 존재, 내 이야기를 듣고 그 감정에 따라 빛으로 응답해주는 친구를 기술로 구현하고자 하였습니다.
<br>
<br>

## ✅ 프로젝트 목표
- 라즈베리파이5 기반의 임베디드 시스템 구축
- 사용자의 한국어 음성 입력 및, 음성을 인식하여 텍스트로 변환(STT) 후 서버로 전송
- 서버의 AI언어 모델(LM)을 통해 7가지 핵심 감정(행복함, 화남, 슬픔 등)을 분석
- 감정 분석 결과를 LED 빛의 색상과 패턴으로 시각화하여 사용자에게 전달
<br>

## ⚙️ Sent-Light 시스템 아키텍처
<img width="1780" height="1000" alt="image" src="https://github.com/user-attachments/assets/653379ee-a263-41e4-b87e-a28b03f18743" />




## 🛠️ HW 구성 및 기능

| 구분 | 부품명 | 역할 및 기능 |
| :--- | :--- | :--- |
| **메인보드** | 라즈베리파이5 | OS구동, 코드 실행, 서버 통신, 음성 입력 제어, STT AI 구동, LED 출력 제어 |
| **입력장치** | USB 연결 마이크 (헤드셋) | 사용자의 발화 음성 수집 |
| **출력장치** | SEENGREAT RGB LED 매트릭스 디스플레이 패널 (64x64) | AI가 분석한 감정 결과와 7가지를 설정된 색상과 패턴으로 시각화 |
| **기타장치** | 원격지원 laptop | 라즈베리파이 OS에 원격접속하여 시스템 모니터링 |
<br>

## 💻 SW 구성 및 기술 스택

| 구분 | 소프트웨어 / 라이브러리 | 역할 및 기능 |
| :--- | :--- | :--- |
| **OS** | Ubuntu | Linux기반 운영체제, 라즈베리파이5 구동 환경 구성. |
| **음성 입력 모듈** | | 음성 인코딩 및 파일 저장 모듈 |
| **STT 모듈** | faster-whisper | 음성 파일(.m4a)을 텍스트로 변환하는 Speech-To-Text 모듈. |
| **LM sentiment analysis 모듈**| bert-base-cased-korean-sentiment | 변환된 텍스트를 분석하여 7가지 감정으로 분류<br>0: 감정 없음, 1: 화남, 2: 혐오, 3: 두려움, 4: 행복함, 5: 슬픔, 6: 놀람. |
| **LED 출력 모듈** | | 감정분석 결과 데이터를 받아 LED 디코딩 및 출력 모듈 |
| **서버** | Ubuntu 22.04 LTS | 라즈베리파이와 ssh 통신. LM 감정 분석 모델 구동 |
| **원격지원** | Anydesk | 라즈베리파이 OS에 원격접속하여 시스템 모니터링 |
| **데이터 번역** | m2m100_418M_PTT | ijcnlp - dailydialog 데이터 한국어 번역 전처리. |

### 개발 환경 (Development Environmnet)
- **Main processor**: Raspberry Pi 5 – 8 GB RAM
- **OS**: Ubuntu 22.04
- **Programming Languages**: Python 3.11
- **Programming Tool**: VS code
- **Virtual environment**: mini conda
- **AI Model / training**: pytorch, faster whisper
- **Network**: Raspberry Pi 5 <-> server
- **Libraries & Tools**: whisper, faster whisper, ffmpeg
- **Monitoring**: Anydesk


<br>

## 📋 메인 실행 파일 및 주요 함수 기능
<img width="1888" height="732" alt="image" src="https://github.com/user-attachments/assets/0d7d1988-f095-4b18-a1c5-d6b75c7604a6" />
<img width="1854" height="616" alt="image" src="https://github.com/user-attachments/assets/ac095302-7868-41be-a1be-0a4e97bd777d" />
<img width="1894" height="698" alt="image" src="https://github.com/user-attachments/assets/ed4075c3-be9e-448a-a822-20245e149fbe" />
<br>

## 📊 향후 발전 방향
- **3D프린터를 활용하여 커스텀 외장 케이스 디자인 구현 가능**
- **GPIO 환경 불일치 해결 -> 향샹된 디스플레이로 더욱 더 동적이고 다양한 감정표현 출력**
- **별도의 on/off 동작 없이 호출로 동작할 수 있도록 '음성 활성화' 기능 추가**
- **개인화된 감정 분석 결과를 바탕으로 맞춤형 정신 건강 케어 구독형 서비스 상업화**
## 🔥 기대 효과
- **고립감 및 외로움을 완화 시켜 주어 정서적 교감 제공**
- **완전 음성 조작으로 고령층과의 디지털 격차 완화**
- **1인 가구 및 독거 노인층 정서 모니터링으로 조기 경고 신호 포착 가능**

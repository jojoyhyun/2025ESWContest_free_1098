실시간 음성 감정 분석 및 LED 반응 시스템

이 프로젝트는 라즈베리 파이에서 실시간으로 음성을 입력받아 감정을 분석하고, 그 결과를 RGB LED 매트릭스에 시각적으로 표현하는 시스템입니다. fast-whisper를 이용한 음성 인식(STT)과 7개 클래스의 감정 분석 모델이 핵심 기능입니다.
📂 프로젝트 구조

.
├── rpi-rgb-led-matrix/

├── audio_source.wav

├── emotion_reaction.py

├── main_pipeline_with_audio.py

├── main_pipeline.py

├── requirements.txt

├── transcript.txt

├── whisper_test_speed_x1.m4a

└── whisper_test.py

⚙️ 주요 스크립트 설명

    main_pipeline_with_audio.py

        메인 실행 파이프라인입니다.

        마이크를 통해 실시간으로 음성을 입력받습니다.

        fast-whisper 모델을 사용하여 음성을 텍스트로 변환(STT)합니다.

        변환된 텍스트를 7개의 클래스로 분류하는 감성 분석을 수행합니다.

        분석된 감정 결과에 따라 라즈베리 파이의 LED 조명을 제어하여 시각적으로 표현합니다.
    emotion_reaction.py

        원격 서버와의 SSH 연결을 테스트하기 위한 스크립트입니다.

        라즈베리 파이와 서버 간의 통신이 원활한지 확인할 때 사용됩니다.
    whisper_test.py

        Whisper STT 모델의 성능을 독립적으로 테스트하기 위한 스크립트입니다.

        음성 인식의 정확도나 속도를 확인할 때 사용됩니다.

🏁 실행 방법

메인 파이프라인을 실행하려면 다음 명령어를 사용하세요:

python main_pipeline_with_audio.py

🔧 요구사항

필요한 라이브러리는 requirements.txt 파일에 명시되어 있습니다. 다음 명령어로 설치할 수 있습니다.

pip install -r requirements.txt


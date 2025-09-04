한국어 분류 프로젝트

이 프로젝트는 jicnlp-dailydiagonal 데이터셋을 분류하는 데 중점을 둡니다. 전체 작업 흐름은 원본 영어 데이터셋을 한국어로 번역하고, 텍스트를 전처리한 후, 한국어 특화 BERT 모델을 학습시켜 분류 작업을 수행하는 과정을 포함합니다.

🚀 프로젝트 작업 흐름

이 프로젝트는 명확한 다단계 파이프라인을 따릅니다:

    번역: 원본 영어 jicnlp-dailydiagonal 데이터셋을 한국어로 먼저 번역합니다.

    데이터 로딩: 번역된 한국어 데이터셋을 메모리로 불러옵니다.

    전처리: 언어 모델과 호환되도록 텍스트 데이터를 정제하고 토큰화합니다.

    모델 학습: 전처리된 데이터를 사용하여 bert-uncased-korean 모델을 화행 분류 작업에 맞게 미세 조정(fine-tuning)합니다.

    평가: 학습된 모델의 성능을 평가하기 위해 테스트를 진행합니다.

📂 Project Structure

Here is a breakdown of the key files and their roles in this project:

.

├── data_loader.py      # Loads the translated dataset for use. (번역된 데이터셋 로딩)

├── process.py          # Preprocesses text data for the language model. (언어 모델을 위한 텍스트 데이터 전처리)

├── process_test.py     # Unit tests for the processing script. (전처리 스크립트 유닛 테스트)

├── test.py             # Evaluates the performance of the trained model. (학습된 모델 성능 평가)

├── training_setup.py   # Handles the training and fine-tuning of the BERT model. (BERT 모델 학습 및 미세 조정)

├── translation.py      # Translates the jicnlp-dailydiagonal dataset to Korean. (jicnlp-dailydiagonal 데이터셋 한국어 번역)

└── transcript.txt      # Example text file, likely for input or output. (입력 또는 출력을 위한 예시 텍스트 파일)


⚙️ 파일 설명

    translation.py:

        jicnlp-dailydiagonal 데이터셋을 영어에서 한국어로 번역하는 스크립트입니다.

        데이터 준비 파이프라인의 첫 번째 단계입니다.

    data_loader.py:

        번역된 한국어 데이터셋을 디스크에서 불러오는 역할을 합니다.

        전처리 스크립트에 입력될 수 있는 형태로 데이터를 준비합니다.

    process.py:

        불러온 한국어 데이터를 받아 필요한 전처리 단계를 수행합니다.

        언어 모델(LM)을 위해 토큰화, 정제, 데이터 형식 맞추기 등의 작업을 포함합니다.

    training_setup.py:

        모델 학습을 위한 핵심 스크립트입니다.

        전처리된 데이터셋을 사용하여 bert-uncased-korean 모델을 설정, 구성 및 미세 조정합니다.

    test.py / process_test.py:

        test.py는 학습된 모델로 추론을 실행하고 분류 정확도를 평가하는 데 사용됩니다.

        process_test.py는 데이터 처리 로직이 예상대로 작동하는지 확인하기 위한 유닛 테스트를 포함할 가능성이 높습니다.


🏁 실행 방법

전체 파이프라인을 실행하려면 다음 순서대로 스크립트를 실행하십시오:

    데이터 번역:

    python translation.py

    모델 학습:
    (training_setup.py가 내부적으로 데이터 로딩 및 전처리를 처리한다고 가정)

    python training_setup.py

    결과 평가:

    python test.py


import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# 1. LED 매트릭스 설정
options = RGBMatrixOptions()
options.rows = 64  # 패널의 행 수
options.cols = 64  # 패널의 열 수
options.chain_length = 1 # 연결된 패널 수
options.parallel = 1 # 병렬로 연결된 패널 수
options.hardware_mapping = 'adafruit-hat'  # 사용하는 하드웨어에 맞게 설정 ('regular', 'adafruit-hat' 등)
# options.gpio_slowdown = 4 # GPIO 속도 조절 (필요시 주석 해제)

matrix = RGBMatrix(options = options)

# 2. 이미지 불러오기
try:
    # 여기에 준비하신 64x64 이미지 파일 경로를 입력하세요.sudo git clone https://github.com/hzeller/rpi-rgb-led-matrix
cd rpi-rgb-led-matrix
sudo make
cd examples-api-use
sudo ./demo -D 9 --led-no-hardware-pulse --led-rows=64 --led-cols=64
    image = Image.open("my_image.png") 
except FileNotFoundError:
    print("오류: 이미지 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    exit()

# 3. 이미지 리사이즈 (혹시 모를 크기 조정을 위해)
image.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)

# 4. 매트릭스에 이미지 표시
# 매트릭스 버퍼에 이미지를 복사한 후, SwapOnVSync()를 통해 화면에 실제로 표시합니다.
matrix.SetImage(image.convert('RGB'))

# 5. 프로그램이 바로 종료되지 않도록 대기
try:
    print("이미지를 표시합니다. Ctrl-C를 눌러 종료하세요.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
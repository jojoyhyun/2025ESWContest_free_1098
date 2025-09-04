#import sounddevice as sd
from scipy.io.wavfile import write
import paramiko
import os
from faster_whisper import WhisperModel

audio_file_path = "whisper_test_speed_x1.m4a"

# --- 1. CONFIGURATION ---
# --- You MUST change these variables ---

# Audio Recording Settings
RECORDING_DURATION = 5  # seconds
SAMPLE_RATE = 44100
AUDIO_FILENAME = "whisper_test_speed_x1.m4a"
TRANSCRIPT_FILENAME = "transcript.txt"

# SSH Server Details
SSH_HOST = "192.168.0.138"  # e.g., "192.168.1.100"
SSH_PORT = 22
SSH_USER = "sangbaek-lee"
PRIVATE_KEY_PATH = os.path.expanduser('~/.ssh/id_rsa')

# Remote Server File Paths and Commands
REMOTE_UPLOAD_PATH = f"/home/{SSH_USER}/uploads"
REMOTE_DOWNLOAD_PATH = REMOTE_UPLOAD_PATH # Path of the file to download back

CONDA_PYTHON_PATH = "/home/sangbaek-lee/miniconda3/envs/sent_anal/bin/python"
SCRIPT_PATH = "/home/sangbaek-lee/uploads/process_test.py"

# 2. 전체 경로를 사용하여 원격 명령어 재구성
REMOTE_PROCESS_COMMAND = f"{CONDA_PYTHON_PATH} {SCRIPT_PATH}"

# Local Path to save the downloaded file
LOCAL_DOWNLOAD_PATH = f"./processed_{TRANSCRIPT_FILENAME}"


# --- 2. MOCK STT MODEL ---
# --- Replace this function with your actual STT model's code ---
def transcribe_audio_with_your_model(audio_file_path): #"whisper_test_speed_x0.75.m4a"
    audio_file = audio_file_path
    model_size = "tiny" #option : tiny, base, small, medium, large-v2, large-v3
    
    #Run with cpu, int8
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    print("Model uploaded. STT running...")
    
    segments, info = model.transcribe(audio_file, beam_size=5, language="ko")
    
    full_text_for_txt = "" #string
    
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        full_text_for_txt += segment.text + " " #txt
        
    text_result = full_text_for_txt
    print("-> Transcription complete.")
    return text_result

def send_file_to_server(local_file_path):
    """지정된 파일을 SFTP를 통해 서버로 전송합니다."""
    if not os.path.exists(local_file_path):
        print(f"오류: {local_file_path} 파일이 존재하지 않습니다.")
        return

    try:
        # SSH 클라이언트 설정
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"{SSH_HOST}에 연결 중...")
        # SSH 키를 사용하여 연결
        private_key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
        ssh_client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, pkey=private_key)

        # SFTP 세션 열기
        sftp_client = ssh_client.open_sftp()
        print("SFTP 연결 성공!")

        # 원격 경로 설정
        remote_file_path = os.path.join(REMOTE_UPLOAD_PATH, os.path.basename(local_file_path))
        
        # 파일 전송
        print(f"파일 전송 시작: {local_file_path} -> {remote_file_path}")
        sftp_client.put(local_file_path, remote_file_path)
        print("파일 전송 성공!")

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        # 연결 종료
        if 'sftp_client' in locals() and sftp_client:
            sftp_client.close()
        if 'ssh_client' in locals() and ssh_client:
            ssh_client.close()
        print("연결 종료.")


# --- 3. THE MAIN WORKFLOW SCRIPT ---
def main():
    print("🚀 Starting the workflow...")

    # == STEP 1: Record voice in Raspberry Pi 5 ==
    # print(f"1. Recording {RECORDING_DURATION} seconds of audio...")
    # try:
    #     recording = sd.rec(int(RECORDING_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    #     sd.wait()  # Wait until recording is finished
    #     write(AUDIO_FILENAME, SAMPLE_RATE, recording)  # Save as WAV file
    #     print(f"   Audio saved to {AUDIO_FILENAME}")
    # except Exception as e:
    #     print(f"❌ ERROR during recording: {e}")
    #     print("   Please ensure a microphone is connected and configured.")
    #     return

    # == STEP 2: Process it with STT model ==
    transcript = transcribe_audio_with_your_model(AUDIO_FILENAME)

    # == STEP 3: Save it to a txt file ==
    with open(TRANSCRIPT_FILENAME, 'w') as f:
        f.write(transcript)
    print(f"3. Transcript saved to {TRANSCRIPT_FILENAME}")

    send_file_to_server(TRANSCRIPT_FILENAME)
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"\nConnecting to SSH server at {SSH_HOST}...")
    ssh_client.connect(hostname=SSH_HOST, port=SSH_PORT, username=SSH_USER, key_filename=PRIVATE_KEY_PATH)
    
    print("5. Executing remote processing script...")
    stdin, stdout, stderr = ssh_client.exec_command(REMOTE_PROCESS_COMMAND)
    result = stdout.read().decode('utf-8').strip()
    print("emotion processed. : ", result)
    print("\n🎉 Workflow complete.")


if __name__ == "__main__":
    main()
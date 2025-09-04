import sounddevice as sd
from scipy.io.wavfile import write as write_wav
import paramiko
import os
from faster_whisper import WhisperModel
from emotion_reaction import *
audio_file_path = "audio_source.wav"

# --- 1. CONFIGURATION ---

# Audio Recording Settings
RECORDING_DURATION = 10  # seconds
SAMPLE_RATE = 44100
AUDIO_FILENAME = "audio_source.wav"
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

# ---  MODEL LOADING (모델을 스크립트 시작 시 한 번만 로드) ---
print("🚀 파이프라인 시작: Whisper 모델 로드...")
try:
    WHISPER_MODEL = WhisperModel("tiny", device="cpu", compute_type="int8")
    #option : tiny, base, small, medium, large-v2, large-v3
    print("   모델 로드 완료.")
except Exception as e:
    print(f"❌ 모델 로드 실패: {e}")
    WHISPER_MODEL = None


# --- 1. AUDIO MODEL ---
def record_audio(duration, rate, filename):
    print(f"🎤 {duration}초 동안 녹음을 시작합니다...")
    try:
        recording = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='int16')
        sd.wait()
        
        write_wav(filename, rate, recording) # WAV 파일로 저장
        
        print(f"👍 녹음 완료! '{filename}' 파일로 저장되었습니다.")
        return True
    except Exception as e:
        print(f"❌ 녹음 중 오류 발생: {e}")
        return False


# --- 2. STT MODEL ---
def transcribe_audio(model, audio_file):
    if not os.path.exists(audio_file):
        print(f"❌ STT 오류: '{audio_file}' 파일을 찾을 수 없습니다.")
        return None
    print(f"오디오 파일을 텍스트로 변환...")
    
    segments, info = model.transcribe(audio_file, beam_size=5, language="ko")
    full_text = "" #string
    
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        full_text += segment.text + " " #txt
        
    print("-> Transcription complete.")
    return full_text 

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

    if WHISPER_MODEL is None:
        return
    
    # == STEP 1: Record voice in Raspberry Pi 5 ==
    # 음성을 녹음하고 파일로 저장.
    if not record_audio(RECORDING_DURATION, SAMPLE_RATE, AUDIO_FILENAME):
        return # 녹음 실패 시 중단

    # == STEP 2: Process it with STT model ==
    transcript = transcribe_audio(WHISPER_MODEL,AUDIO_FILENAME)

    # == STEP 3: Save it to a txt file ==
    with open(TRANSCRIPT_FILENAME, 'w') as f:
        f.write(transcript)
    print(f"Transcript saved to {TRANSCRIPT_FILENAME}")

    send_file_to_server(TRANSCRIPT_FILENAME)
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"\nConnecting to SSH server at {SSH_HOST}...")
    ssh_client.connect(hostname=SSH_HOST, port=SSH_PORT, username=SSH_USER, key_filename=PRIVATE_KEY_PATH)
    
    print("Executing remote processing script...")
    stdin, stdout, stderr = ssh_client.exec_command(REMOTE_PROCESS_COMMAND)
    result = stdout.read().decode('utf-8').strip()
    result = int(result)
    
    if result == 0:
        txt = "no emotion :|"
    elif result == 1:
        txt = "anger!! -3-"
    elif result == 2:
        txt = "digust... OTL"
    elif result == 3:
        txt = "fear! ㅇoㅇ"
    elif result == 4:
        txt = "happy! :)"
    elif result == 5:
        txt = "sad :("  
    elif result == 6: 
        txt = "surprised!!"

    print("emotion processed. : ", txt)
    print("\n🎉 Workflow complete.")
    
    emotion_reaction(result)
    

if __name__ == "__main__":
    main()
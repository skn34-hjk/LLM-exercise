# STT(음성 -> 텍스트) + GPT 응답 + TTS(텍스트 -> 음성) 파이프라인 함수
import base64
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI()

# 오디오 객체를 Whisper로 STT(Speach-To-Text)하는 함수
def stt(audio):
    output_filepath = 'input.mp3'  # 임시 저장할 파일명
    audio.export(output_filepath, format='mp3')  # 오디오 객체를 mp3 파일로 저장

    with open(output_filepath, 'rb') as f:  # 오디오 파일을 바이너리 읽기 모드로 열기
        # STT API 호출
        transcription = client.audio.transcriptions.create(
            model='whisper-1',
            file=f
        )

    os.remove(output_filepath)  # 임시 mp3파일 삭제

    return transcription.text

# 메시지 히스토리를 받아서 GPT API로 응답을 생성해서 반환하는 함수
def ask_gpt(messages, model):
        return client.chat.completions.create(
            model = model,
            messages = messages,
            temperature = 1,
            top_p = 1,
            max_completion_tokens = 4096  # 최대 출력 토큰 수 (응답 길이 제한)
        ).choices[0].message.content

# 텍스트를 받아 TTS(Test-To-Speach)로 mp3 생성후 base64 문자열로 반환하는 함수
# base64 : json의 값으로써 멀티미디어 파일을 전송하고 싶은 경우, base64 인코딩 -> 확인하는 측에서는 base64 디코딩
def tts(response: str):
    filename = 'output.mp3'  # base64로 인코딩할 임시파일명

    # 스트리밍 방식 TTS 요청
    with client.audio.speech.with_streaming_response.create(
        model = 'tts-1',
        voice = 'coral',
        input = input
    ) as resp:
        resp.stream_to_file(filename)  # 스트리밍한 결과를 mp3 파일로 저장

    with open(filename, 'rb') as f:  # mp3파일을 바이너리로 읽음
        data = f.read  # mp3파일의 이진데이터(바이너리) 형식
        b64_encoded = base64.b64encode(data).decode()  # 이진 -> base64(이진) -> 문자열로 디코딩
    os.remove(filename)  # 임시 mp3파일 삭제

    return b64_encoded  # base64 인코딩 문자열 (웹/앱에서 바로 재생가능)

# ffmpeg 미설치시 업로드된 파일을 텍스트로 변환해 반환하는 함수
def stt_file(uploaded_file) -> str:
    transcription = client.audio.transcriptions.create(
        model = 'whisper-1',
        # (파일명, 파일바이트) 튜플형식으로 업로드
        file = (uploaded_file.name, uploaded_file.getvalue())
    )

    return transcription.text
from openai import OpenAI
from utils import record_audio, play_audio
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 从环境变量中获取API密钥
api_key = os.getenv("OPENAI_API_KEY")

# 确保API密钥已经被设置
if not api_key:
    raise ValueError("请设置你的Openai API Key")

client = OpenAI(api_key=api_key)

while True:
  record_audio('test.wav')
  audio_file= open('test.wav', "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
  )

  print(transcription.text)

  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "你是我的女朋友。请用简短的句子回答，并且要温柔。"},
      {"role": "user", "content": f"请回答: {transcription.text}"},
    ]
  )

  print(response.choices[0].message.content)

  response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=response.choices[0].message.content
  )

  response.stream_to_file('output.mp3')
  play_audio('output.mp3')

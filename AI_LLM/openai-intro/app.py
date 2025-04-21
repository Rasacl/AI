from openai import OpenAI
import os
from dotenv import load_dotenv
from openai.types.responses import response
# 指定 .env 文件的路径
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(env_path)
load_dotenv(env_path)
api_key = os.getenv('OPENAI_API_KEY')
print(api_key,111)
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",  # 使用正确的模型名称
  messages=[
      {
          "role": "system",
          "content": "You are a helpful assistant."
      },
    {
      "role": "user",
      "content": "你好"
    } 
  ]

)

print(response.choices[0].message.content)
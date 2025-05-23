import ollama

response = ollama.list()

res = ollama.chat(
    model="llama3.2", 
    messages=[
        {"role": "user", "content": "为什么天空是蓝色的."},
    ]         
     )

print(res['message']['centent']) 
##  自定义
ollama create james -f ./Modelfile

```txt
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt":"Why is the sky blue?"
}'
```
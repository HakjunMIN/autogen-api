# Simple FastAPI for Autogen

Powered by `autogen-fastapi` project

## Get started

### 환경구성
```sh
conda create -n autogen python=3.10
conda activate autogen
pip install -r requirements.txt
```

### Azure OpenAI설정
```sh
mv OAI_CONFIG_LIST_yours.json OAI_CONFIG_LIST.json
```

* api-key와 base-url 수정
```json
[
    {
      "model": "gpt-4o",
      "api_type": "azure",
      "api_key": "<your-api-key>",
      "base_url": "<your-base-url>", 
      "api_version": "2024-02-01"
    },
    {
      "model": "gpt-4",
      "api_type": "azure",
      "api_key": "<your-api-key>",
      "base_url": "<your-base-url>", 
      "api_version": "2024-02-01"
    }
  ]
  
```

### fastAPI구동
```sh
uvicorn --reload app.main:app --host 0.0.0.0 
```
### 테스트

You can query the autogen agents using the following command: 
```sh
curl -X 'POST' \
  'http://localhost:8000/autogen/api/v1/chat/completions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "messages": [
    {
      "role": "user",
      "content": "최근 마이크로소프트 주식 분석좀 해줘"
    }
  ]
}'
```

### Swagger

브라우저에서 아래 URL접속

```
http://localhost:8081/autogen/api/v1/docs
```

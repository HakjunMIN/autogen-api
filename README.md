# Simple FastAPI for Autogen

Powered by [`autogen-fastapi`](https://github.com/LineaLabs/autogen-fastapi/) project

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
cd app
uvicorn --reload main:app --host 0.0.0.0 
```
### 테스트

You can query the autogen agents using the following command: 
```sh
curl -X 'POST' \
  'http://localhost:8000/autogen/api/v1/completions/autogen-workflow' \
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
### Sample Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "마이크로소프트 주가"
    }
  ],
  "stream": true
}
```

### Sample Response (스트리밍 켰을때)

```
	
data: {"id": "c5077338-09b8-4a3f-ac51-6d5cbadef2ba", "object": "chat.completion.chunk", "created": 1722843584, "choices": [{"index": 0, "delta": {"role": "assistant", "content": "UserProxy (to chat_manager):\nMicrosoft stock price\n\n--------------------------------------------------------------------------------\n"}, "finish_reason": "stop"}]}

data: {"id": "d68ceabf-d8a3-4f06-91ef-3ae42cf89d94", "object": "chat.completion.chunk", "created": 1722843584, "choices": [{"index": 1, "delta": {"role": "assistant", "content": "UserProxy (to chat_manager):\nHello everyone! It's great to see such a capable team here. Let's get started. Does anyone have any questions or tasks at hand?\n\n--------------------------------------------------------------------------------\n"}, "finish_reason": "stop"}]}

data: {"id": "12164e0c-7351-4755-a88f-0e166813a6df", "object": "chat.completion.chunk", "created": 1722843584, "choices": [{"index": 2, "delta": {"role": "assistant", "content": "code assistant (to chat_manager):\nHello UserProxy! It's great to be here and ready to assist. We don't have any questions or tasks at hand yet, but you mentioned the Microsoft stock price earlier. If you need real-time stock prices, you'll typically need to use a financial data API or check a financial news website. How can we assist you further with this or any other tasks you have in mind?\n\n--------------------------------------------------------------------------------\n"}, "finish_reason": "stop"}]}

data: {"id": "288c0aff-06b5-442f-8151-5c616d3c0f6b", "object": "chat.completion.chunk", "created": 1722843584, "choices": [{"index": 3, "delta": {"role": "assistant", "content": "code assistant (to chat_manager):\nHello UserProxy! It's great to see all agents ready to assist. If you need specific programming or code-related help, feel free to ask!\n\n--------------------------------------------------------------------------------\n"}, "finish_reason": "stop"}]}

data: {"id": "521fd90f-54a3-4c3c-926e-4e041e369383", "object": "chat.completion.chunk", "created": 1722843584, "choices": [{"index": 4, "delta": {"role": "assistant", "content": "critic assistant (to chat_manager):\nHello UserProxy, as your critic assistant, I'm here to support you in\n\n--------------------------------------------------------------------------------\n"}, "finish_reason": "stop"}]}

data: {"id": "d951db13-17e9-45f7-8308-762cdbb7479c", "object": "chat.completion.chunk", "created": 1722843584, "choices": [{"index": 5, "delta": {"role": "assistant", "content": "critic assistant (to chat_manager):\nanalyzing or providing feedback on various subjects. If you have any content, ideas\n\n--------------------------------------------------------------------------------\n"}, "finish_reason": "stop"}]}

data: {"id": "7d9f632d-a84e-4c82-b580-0cadf2c8877a", "object": "chat.completion.chunk", "created": 1722843584, "choices": [{"index": 6, "delta": {"role": "assistant", "content": "UserProxy (to chat_manager):\n, or tasks that require a critical evaluation or review, please feel free to share\n\n--------------------------------------------------------------------------------\n"}, "finish_reason": "stop"}]}

...
```

### API Spec in Swagger

브라우저에서 아래 URL접속

```
http://localhost:8000/autogen/api/v1/completions/docs
```

## Workflow추가 방법

- `workflow` 디렉토리에 파일 추가 후 `AutogenWorkFlow`를 상속받아 구현. 
- `__init()__`에서 실제 workflow구현.
- `self.chat_manager`가 기본적으로 UserProxyAgent가 대화할 상대이므로 반드시 지정
- 필요 시 `run()` 오버라이드

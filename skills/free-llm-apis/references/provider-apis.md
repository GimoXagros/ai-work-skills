# Provider APIs - Setup Guides

> Setup starting points, reviewed 2026-10-11. Provider UI, endpoints, permission labels and free-tier eligibility must be verified against current official documentation before use. No provider API was called during this repository update.

APIs run by the companies that train or fine-tune the models themselves.

## Google Gemini


### Get your API key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with a Google account.
3. Click "Create API Key" and select or create a Google Cloud project.
4. Copy the generated key.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

Set `LLM_API_KEY` locally from your provider key and `LLM_MODEL` from its current eligible model catalog. The provider-specific names below are alternatives; map them explicitly if using the generic example.

### Environment variable

```bash
export GEMINI_API_KEY="your-key-here"
# Or for OpenAI-compatible usage:
export OPENAI_API_KEY="your-key-here"
export OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
```

---

## Cohere


### Get your API key

1. Go to the [Cohere Dashboard](https://dashboard.cohere.com/api-keys).
2. Create an account or sign in.
3. Go to API Keys and generate a trial key.
4. Copy the key.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://api.cohere.com/v2/"
)

response = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

Set `LLM_API_KEY` locally from your provider key and `LLM_MODEL` from its current eligible model catalog. The provider-specific names below are alternatives; map them explicitly if using the generic example.

### Environment variable

```bash
export CO_API_KEY="your-key-here"
```

---

## Mistral AI


### Get your API key

1. Go to the [Mistral Console](https://console.mistral.ai/api-keys).
2. Create an account or sign in.
3. Go to API Keys and create a new key.
4. Copy the key.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://api.mistral.ai/v1/"
)

response = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

Set `LLM_API_KEY` locally from your provider key and `LLM_MODEL` from its current eligible model catalog. The provider-specific names below are alternatives; map them explicitly if using the generic example.

### Environment variable

```bash
export MISTRAL_API_KEY="your-key-here"
```

---

## Zhipu AI


### Get your API key

1. Go to [Zhipu AI](https://open.bigmodel.cn/usercenter/apikeys).
2. Sign up (a Chinese phone number may be required).
3. Go to API Keys and create a new key.
4. Copy the key.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

response = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

Set `LLM_API_KEY` locally from your provider key and `LLM_MODEL` from its current eligible model catalog. The provider-specific names below are alternatives; map them explicitly if using the generic example.

### Environment variable

```bash
export ZHIPU_API_KEY="your-key-here"
```

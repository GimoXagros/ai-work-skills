# Inference Providers - Setup Guides

> Setup starting points, reviewed 2026-10-11. Provider UI, endpoints, permission labels and free-tier eligibility must be verified against current official documentation before use. No provider API was called during this repository update.

Third-party platforms that host open-weight models from various sources.

## GitHub Models


### Get your API key

1. Go to [GitHub Models Marketplace](https://github.com/marketplace/models).
2. Sign in with your GitHub account.
3. Pick any model and click "Get API key" or go to your GitHub settings > Developer settings > Personal access tokens.
4. Generate a fine-grained token with the "Models" permission.
5. Copy the token.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://models.inference.ai.azure.com/"
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
export GITHUB_TOKEN="your-token-here"
```

---

## NVIDIA NIM


### Get your API key

1. Go to [NVIDIA NIM](https://build.nvidia.com/explore/discover).
2. Create an NVIDIA account or sign in.
3. Pick any model and click "Get API Key."
4. Copy the key.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://integrate.api.nvidia.com/v1/"
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
export NVIDIA_API_KEY="your-key-here"
```

---

## Groq


### Get your API key

1. Go to the [Groq Console](https://console.groq.com/keys).
2. Create an account or sign in.
3. Click "Create API Key."
4. Name it and copy the key.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://api.groq.com/openai/v1/"
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
export GROQ_API_KEY="your-key-here"
```

---

## Cerebras


### Get your API key

1. Go to [Cerebras Cloud](https://cloud.cerebras.ai/).
2. Create an account or sign in.
3. Go to API Keys and create a new one.
4. Copy the key.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://api.cerebras.ai/v1/"
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
export CEREBRAS_API_KEY="your-key-here"
```

---

## Cloudflare Workers AI


### Get your API key

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens).
2. Sign in or create a Cloudflare account.
3. Create an API token with the "Workers AI" permission.
4. Note your Account ID from the dashboard sidebar.
5. Copy both the token and account ID.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/v1/"
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
export CLOUDFLARE_API_TOKEN="your-token-here"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
```

---

## LLM7.io


### Get your API key

1. Go to [LLM7 Token page](https://token.llm7.io).
2. Register or sign in to get a token.
3. Copy the token.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://api.llm7.io/v1/"
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
export LLM7_API_KEY="your-token-here"
```

---

## Kluster AI


### Get your API key

1. Go to [Kluster AI Platform](https://platform.kluster.ai/apikeys).
2. Create an account or sign in.
3. Generate a new API key.
4. Copy the key.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://api.kluster.ai/v1/"
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
export KLUSTER_API_KEY="your-key-here"
```

---

## OpenRouter


### Get your API key

1. Go to [OpenRouter Keys](https://openrouter.ai/keys).
2. Create an account or sign in.
3. Click "Create Key."
4. Copy the key.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://openrouter.ai/api/v1/"
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
export OPENROUTER_API_KEY="your-key-here"
```

---

## Hugging Face


### Get your API key

1. Go to [Hugging Face Tokens](https://huggingface.co/settings/tokens).
2. Create an account or sign in.
3. Create a new access token with "Make calls to Inference Providers" permission.
4. Copy the token.

### Example structure (verify endpoint and SDK first)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url="https://router.huggingface.co/v1/"
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
export HF_TOKEN="your-token-here"
```

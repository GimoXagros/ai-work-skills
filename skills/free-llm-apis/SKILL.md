---
name: free-llm-apis
description: Guide users through obtaining and configuring free API keys for LLM providers. Use when the user wants to set up a free LLM API, get a free API key, connect to a free model provider, configure an OpenAI-compatible endpoint at no cost, or asks about free tiers for AI models. Triggers on "free API key", "free LLM", "set up Gemini/Groq/Mistral/etc.", "which free provider", "how to get an API key", "free model access", "configure LLM for free".
---

# Free LLM API Setup

Help users select and configure a currently available no-cost tier. Provider catalogs, model IDs, regional eligibility, quotas and trial conditions change independently of this skill. Never promise permanent free access or infer that every listed provider or model is free.

## Provider Selection

1. Use the user's stated model, latency, region and volume needs; ask only for missing constraints that affect the choice.
2. Treat the reference files as setup starting points. Before recommending a provider, check its official pricing, model/deprecation documentation and account-specific quota page. Record the check date and distinguish recurring free quota, trial credits, paid models and unverified claims.
3. Verify the exact endpoint, supported API/SDK and model ID before generating runnable code. If current evidence is unavailable, label the option unverified instead of quoting old limits.
4. Recommend one or two options supported by those checks. Do not create accounts, add billing, obtain secrets, or change a running agent's provider merely by installing this skill.

### Provider categories

**Provider APIs** -- run by the companies that train the models:
- Google Gemini, Cohere, Mistral AI, Zhipu AI
- See [references/provider-apis.md](references/provider-apis.md) for setup instructions.

**Inference providers** -- third-party platforms hosting open-weight models:
- GitHub Models, NVIDIA NIM, Groq, Cerebras, Cloudflare Workers AI, LLM7.io, Kluster AI, OpenRouter, Hugging Face
- See [references/inference-providers.md](references/inference-providers.md) for setup instructions.

## Workflow

1. Ask what models, rate limits, or features the user cares about. If they already know which provider they want, skip to step 3.
2. Match their priorities against currently verified provider documentation. Suggest 1-2 options with a short reason.
3. Load the right reference file and walk through the setup steps for that provider (API key, code example, env var).
4. Offer a quick test script or curl command so they can confirm the key works.

## Quick Test Template

After setup, use this to verify any provider:

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])

response = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
    max_tokens=50
)
print(response.choices[0].message.content)
```

Set these environment variables locally from the verified provider setup. Use this template only after OpenAI chat-completions compatibility is confirmed. Do not ask the user to paste a key into chat.

## Key Notes

- SDK compatibility must be checked for the selected endpoint; use the native SDK when required.
- RPM = requests per minute. RPD = requests per day.
- Check current regional eligibility in official documentation; do not reuse historical region exclusions.
- "Limits undocumented" = the provider doesn't publish rate limits.
- Don't hardcode API keys. Use environment variables or a secrets manager.

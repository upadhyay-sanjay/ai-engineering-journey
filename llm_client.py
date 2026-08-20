# llm_client.py
# Day 6 — Object-Oriented Programming
#
# A multi-provider AI client built with inheritance.
# One base class holds shared logic.
# Each provider class only defines what is different.


# ── Base Class ────────────────────────────────────────────────────────────────

class LLMClient:
    """Base class for all AI provider clients."""

    def __init__(self, api_key: str, model: str, max_tokens: int = 1024):
        if not api_key:
            raise ValueError("api_key cannot be empty")
        self.api_key    = api_key
        self.model      = model
        self.max_tokens = max_tokens

    def build_payload(self, user_message: str, system: str = None) -> dict:
        """Build a request payload for the provider."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user_message})
        return {
            "model":      self.model,
            "max_tokens": self.max_tokens,
            "messages":   messages,
        }

    def build_headers(self) -> dict:
        """Build request headers. Override in each provider."""
        raise NotImplementedError("Each provider must implement build_headers()")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model='{self.model}', max_tokens={self.max_tokens})"


# ── Provider Classes ──────────────────────────────────────────────────────────

class OpenAIClient(LLMClient):
    """Client for OpenAI models (GPT-4o, GPT-4o-mini, etc.)"""

    def __init__(self, api_key: str, model: str = "gpt-4o", max_tokens: int = 1024):
        super().__init__(api_key=api_key, model=model, max_tokens=max_tokens)

    def build_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
        }


class AnthropicClient(LLMClient):
    """Client for Anthropic models (Claude, etc.)"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", max_tokens: int = 1024):
        super().__init__(api_key=api_key, model=model, max_tokens=max_tokens)

    def build_headers(self) -> dict:
        return {
            "x-api-key":         self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type":      "application/json",
        }


# ── Demo ──────────────────────────────────────────────────────────────────────

USER_MESSAGE = "What is Retrieval-Augmented Generation?"
SYSTEM       = "You are an expert in AI Engineering. Be concise."

clients = [
    OpenAIClient(api_key="sk-openai-test-key"),
    AnthropicClient(api_key="sk-ant-test-key"),
]

print("=" * 60)
print("  MULTI-PROVIDER AI CLIENT")
print("  Same message. Two providers. Different structure.")
print("=" * 60)

for client in clients:
    print(f"\n{client}")
    print(f"\n  HEADERS")
    for key, value in client.build_headers().items():
        # Mask the API key for display
        display_value = value if "key" not in key.lower() and "authorization" not in key.lower() else "sk-***masked***"
        print(f"    {key}: {display_value}")

    payload = client.build_payload(USER_MESSAGE, system=SYSTEM)
    print(f"\n  PAYLOAD")
    print(f"    model      : {payload['model']}")
    print(f"    max_tokens : {payload['max_tokens']}")
    print(f"    messages   : {len(payload['messages'])} message(s)")
    for msg in payload["messages"]:
        print(f"      [{msg['role']}] {msg['content'][:60]}...")

print("\n" + "=" * 60)
print("  INHERITANCE IN ACTION")
print("=" * 60)
print(f"\n  Both clients share build_payload() from LLMClient.")
print(f"  Each defines its own build_headers() for their API.")
print(f"\n  Adding a new provider = one new class.")
print(f"  No changes needed to existing code.")
print("=" * 60)



## Predict Before You Measure

### Qwen2.5-0.5B-Instruct, generating on CPU in the lab container.
#### How many tokens per second do you expect: 1, 10, 100, or 1000?

- Because it'll be running on a CPU that'll make it slower than GPU, so it would be **10 tokens per second** but it depends on the HW and framework.

---

### Predictions

1. After you send one chat request with a 10-word user message and ask for 32 tokens back, usage.prompt_tokens will be about 32 and usage.completion_tokens will be about 10.

explanation:
because the  model will generate 32 tokens so the `completion_tokens` = **32 tokens**
10-word will be **10 prompt tokens** but it is based on the text itself.


2. Which of the three routes will pass its test first, with the least code? /health
because it'll check if the server is running.

3. Will an unmodified openai Python client work against your server with only a base_url change, no other edits? Yes (why or why not)
 because as mentioned in the slides the openai Python client is against the same endpoint.

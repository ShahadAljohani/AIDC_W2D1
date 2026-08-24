## Predict Before You Measure

### Qwen2.5-0.5B-Instruct, generating on CPU in the lab container.

#### How many tokens per second do you expect: 1, 10, 100, or 1000?

- Because it will be running on a CPU, it will be slower than running on a GPU, so I expect approximately **10 tokens per second**, but the actual performance depends on the hardware and framework.

---

### Predictions

1. After you send one chat request with a 10-word user message and ask for 32 tokens back, `usage.prompt_tokens` will be more than 10 because token count is different from word count and includes the formatted chat prompt. `usage.completion_tokens` will be **up to 32**, because `max_tokens=32` is the maximum number of tokens the model can generate. The model may generate fewer than 32 tokens if it finishes earlier.

2. Which of the three routes will pass its test first, with the least code?

   `/health` because it only checks if the server is running and the model is loaded. It does not need to run the model.

3. Will an unmodified OpenAI Python client work against your server with only a `base_url` change, no other edits?

   **Yes**, because the server implements OpenAI-compatible endpoints and response formats, so the OpenAI Python client can communicate with the server by changing the `base_url`.

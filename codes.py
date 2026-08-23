

CATALOG = {
    "Qwen2.5-0.5B-Instruct": {"hidden_size": 896, "num_hidden_layers": 24, "num_attention_heads": 14, "num_key_value_heads": 2, "intermediate_size": 4864, "vocab_size": 151936, "tie_word_embeddings": True},
    "Qwen2.5-1.5B-Instruct": {"hidden_size": 1536, "num_hidden_layers": 28, "num_attention_heads": 12, "num_key_value_heads": 2, "intermediate_size": 8960, "vocab_size": 151936, "tie_word_embeddings": True},
    "Qwen2.5-3B-Instruct": {"hidden_size": 2048, "num_hidden_layers": 36, "num_attention_heads": 16, "num_key_value_heads": 2, "intermediate_size": 11008, "vocab_size": 151936, "tie_word_embeddings": True},
    "Llama-3.2-1B-Instruct": {"hidden_size": 2048, "num_hidden_layers": 16, "num_attention_heads": 32, "num_key_value_heads": 8, "intermediate_size": 8192, "vocab_size": 128256, "tie_word_embeddings": True},
    "Llama-3.2-3B-Instruct": {"hidden_size": 3072, "num_hidden_layers": 28, "num_attention_heads": 24, "num_key_value_heads": 8, "intermediate_size": 8192, "vocab_size": 128256, "tie_word_embeddings": True},
}


def count_params(cfg):
    h = cfg["hidden_size"]
    L = cfg["num_hidden_layers"]
    n_heads = cfg["num_attention_heads"]
    n_kv = cfg["num_key_value_heads"]
    inter = cfg["intermediate_size"]
    vocab = cfg["vocab_size"]
    tied = cfg.get("tie_word_embeddings", False)
    head_dim = h // n_heads

    # attention: q and o are full hidden_size x hidden_size; k and v are
    # narrower because of grouped-query attention (fewer kv heads than query heads)
    q = h * h
    k = h * (n_kv * head_dim)
    v = h * (n_kv * head_dim)
    o = h * h
    attn = q + k + v + o

    # gated MLP (SwiGLU-style): three matrices, not two
    gate = h * inter
    up = h * inter
    down = inter * h
    mlp = gate + up + down

    per_layer = attn + mlp
    embed_matrices = 1 if tied else 2   # tied models reuse one matrix for input+output
    total = L * per_layer + embed_matrices * vocab * h
    return total


for name, cfg in CATALOG.items():
    p = count_params(cfg)
    print(f"{name}: {p/1e9:.2f}B params")


def count_params(cfg):
    h = cfg["hidden_size"]
    L = cfg["num_hidden_layers"]
    n_heads = cfg["num_attention_heads"]
    n_kv = cfg["num_key_value_heads"]
    inter = cfg["intermediate_size"]
    vocab = cfg["vocab_size"]
    tied = cfg.get("tie_word_embeddings", False)
    head_dim = h // n_heads

    # attention: q and o are full hidden_size x hidden_size; k and v are
    # narrower because of grouped-query attention (fewer kv heads than query heads)
    q = h * h
    k = h * (n_kv * head_dim)
    v = h * (n_kv * head_dim)
    o = h * h
    attn = q + k + v + o

    # gated MLP (SwiGLU-style): three matrices, not two
    gate = h * inter
    up = h * inter
    down = inter * h
    mlp = gate + up + down

    per_layer = attn + mlp
    embed_matrices = 1 if tied else 2   # tied models reuse one matrix for input+output
    total = L * per_layer + embed_matrices * vocab * h
    return total


for name, cfg in CATALOG.items():
    p = count_params(cfg)
    print(f"{name}: {p/1e9:.2f}B params")

#It showed that 3b is an approximation and not the exact count of parameters 

def kv_bytes_per_token(cfg, kv_dtype_bytes=2):
    h = cfg["hidden_size"]
    L = cfg["num_hidden_layers"]
    n_kv = cfg["num_key_value_heads"]
    n_heads = cfg["num_attention_heads"]
    head_dim = h // n_heads
    return 2 * L * n_kv * head_dim * kv_dtype_bytes


PRECISIONS = {"fp16": 2.0, "int8": 1.0, "int4": 0.5}
OVERHEAD_GB = 1.5   # fixed CUDA/allocator overhead, midpoint of W2D1's 1-2 GB range

def solve(budget_gb, concurrent_users, context_tokens):
    rows = []
    for name, cfg in CATALOG.items():
        params = count_params(cfg)
        kv_per_tok = kv_bytes_per_token(cfg)
        for prec, bytes_per_param in PRECISIONS.items():
            weight_gb = params * bytes_per_param / 1e9
            kv_gb = kv_per_tok * context_tokens * concurrent_users / 1e9
            total_gb = weight_gb + kv_gb + OVERHEAD_GB
            fits = total_gb <= budget_gb
            rows.append({
                "model": name, "precision": prec, "params": params,
                "weight_gb": round(weight_gb, 2), "kv_gb": round(kv_gb, 2),
                "total_gb": round(total_gb, 2), "fits": fits,
            })
    fitting = [r for r in rows if r["fits"]]
    best = max(fitting, key=lambda r: r["params"]) if fitting else None
    return rows, best

rows, best = solve(budget_gb=16, concurrent_users=4, context_tokens=4096)
for r in sorted(rows, key=lambda r: -r["params"]):
    mark = "FITS" if r["fits"] else "----"
    print(f"{mark}  {r['model']:25s} {r['precision']:5s}  total={r['total_gb']:6.2f}GB")
print("BEST:", best)


import json
budget_gb, concurrent_users, context_tokens = 16, 4, 4096
rows, best = solve(budget_gb, concurrent_users, context_tokens)
out = {
    "budget_gb": budget_gb, "concurrent_users": concurrent_users,
    "context_tokens": context_tokens, "best": best,
    "all_combinations": rows,
}
with open("budget_solution.json", "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(best, indent=2))
## Configuration

The solver uses the following configuration:

* **GPU memory budget:** 16 GB
* **Concurrent users:** 4
* **Context length:** 4096 tokens
* **Runtime overhead:** 1.5 GB

## Results

### Calculated Parameter Counts

| Model                 | Calculated Parameters |
| --------------------- | --------------------: |
| Qwen2.5-0.5B-Instruct |                0.494B |
| Qwen2.5-1.5B-Instruct |                1.544B |
| Qwen2.5-3B-Instruct   |                3.086B |
| Llama-3.2-1B-Instruct |                1.236B |
| Llama-3.2-3B-Instruct |                3.213B |

### Estimated Total Memory

The estimated total GPU memory required for each model and precision is:

| Model                 |    FP16 |    INT8 |    INT4 |
| --------------------- | ------: | ------: | ------: |
| Qwen2.5-0.5B-Instruct | 2.69 GB | 2.20 GB | 1.95 GB |
| Qwen2.5-1.5B-Instruct | 5.06 GB | 3.51 GB | 2.74 GB |
| Qwen2.5-3B-Instruct   | 8.28 GB | 5.19 GB | 3.65 GB |
| Llama-3.2-1B-Instruct | 4.51 GB | 3.27 GB | 2.65 GB |
| Llama-3.2-3B-Instruct | 9.80 GB | 6.59 GB | 4.99 GB |

All 15 model and precision combinations fit within the 16 GB memory budget under the assumptions used in this lab.

### Best Combination

The largest model by parameter count that fits within the 16 GB budget is:

* **Model:** Llama-3.2-3B-Instruct
* **Precision:** FP16
* **Parameters:** ~3.213B
* **Estimated memory:** ~9.80 GB
* **Budget:** 16 GB
* **Result:** FITS

> **Best combination: Llama-3.2-3B-Instruct at FP16.**

### Solved the prediction questions before applying, you can find it in `lab_README.md` file 

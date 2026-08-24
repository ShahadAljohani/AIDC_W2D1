- fp16 is 2 bytes per parameter. 1.5B times 2 bytes is **3 GB** of weights.

- int8 is 1 byte per parameter, so **1.5 GB** of weights.

- int4 is about 0.5 bytes per parameter, so **0.75 GB** of weights.

- Loaded and resident on the GPU, add roughly **1.7–2.7 GB** of overhead to each.

- Would this model fit at fp32 (4 bytes per parameter) on a 15 GB T4? **Yes. FP32 would be about 6 GB of weights, plus the runtime overhead, so it should fit within 15 GB.**

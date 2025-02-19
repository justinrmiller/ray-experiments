import ray
from ray.data.llm import build_llm_processor, vLLMEngineProcessorConfig

config = vLLMEngineProcessorConfig(
    model="unsloth/Llama-3.2-1B-Instruct",
    engine_kwargs=dict(
        enable_prefix_caching=True,
        enable_chunked_prefill=True,
        max_num_batched_tokens=4096,
    ),
    concurrency=1,
    batch_size=1,
)

processor = build_llm_processor(
    config,
    preprocess=lambda row: dict(
        messages=row["question"],
        sampling_params=dict(
            temperature=0.3,
            max_tokens=10,
        )
    ),
    postprocess=lambda row: dict(
        answer=row["generated_text"]
    ),
)

# input_ds = ray.data.read_parquet(...)
input_ds = ray.data.from_items([
    {"question": "What is your name?"}
] * 1)

input_ds.show()

output_ds = processor(input_ds)
output_ds.write_parquet("test.parquet")
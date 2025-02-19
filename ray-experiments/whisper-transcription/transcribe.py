import pandas as pd
import ray
import torch
from datasets import Dataset
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


class SpeechRecognitionActor:
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "openai/whisper-large-v3-turbo"
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            torch_dtype=self.torch_dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True
        )
        self.model.to(self.device)

        self.processor = AutoProcessor.from_pretrained(model_id)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            chunk_length_s=30,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_dtype,
            device=self.device
        )

    def __call__(self, batch):
        dataset = Dataset.from_pandas(batch)

        def iterate_data(dataset):
            for _, item in enumerate(dataset):
                yield item["bytes"]

        batch_size = 1

        print(f"Batch Size: {batch_size}")

        results = []

        for i, out in enumerate(self.pipe(iterate_data(dataset), batch_size=batch_size)):
            results.append(
                {
                    "path": dataset[i]["path"],
                    "transcript": out['text']
                }
            )

        print(results)

        return pd.DataFrame.from_dict(results)


if __name__ == '__main__':
    ray.init()

    path = './input_parquet'
    ds = ray.data.read_parquet(path).limit(1)

    results = ds.map_batches(
        SpeechRecognitionActor,
        concurrency=1,
        batch_format="pandas",
        batch_size=64,
        num_cpus=6,
        num_gpus=1 if torch.cuda.is_available() else None,
        zero_copy_batch=True,
    ).materialize()

    print(results.show(10))
    print(results.schema())

    results.write_parquet("output")
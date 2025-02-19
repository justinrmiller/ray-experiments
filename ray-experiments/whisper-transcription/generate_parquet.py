import ray

if __name__ == '__main__':
    ray.init()

    path = './input_audio'

    ds = ray.data.read_binary_files(path, include_paths=True)

    print(f"Generated parquet with the following schema:\n{ds.schema()}")

    for row in ds.take(10):
        print(f"Processed file: {row['path']}")

    ds.write_parquet("input_parquet/", min_rows_per_file=10)
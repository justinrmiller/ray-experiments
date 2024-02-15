import argparse
import vertex_ray
import ray

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Destroy Cluster")
    parser.add_argument(
        "--cluster", required=True, help="Cluster Name"
    )
    parser.add_argument(
        "--region", required=True, help="Region"
    )
    parser.add_argument(
        "--project_number", required=True, help="Project Number"
    )

    args, _ = parser.parse_known_args()

    cluster_resource_name=f"projects/{args.project_number}/locations/{args.region}/persistentResources/{args.cluster}"

    print(f"""
        Deleting cluster with the following parameters:
            cluster_resource_name={cluster_resource_name}
            project_number={args.project_number}
            region={args.region}
            cluster={args.cluster}
    """)
    
    ray.shutdown()

    vertex_ray.delete_ray_cluster(cluster_resource_name)

    print(f"Cluster {args.cluster} deleted.")
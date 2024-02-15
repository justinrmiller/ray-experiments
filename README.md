Ray Experiments
===

This project encapsulates some of my experiments running Ray w/VertexAI on GCP.

If you run into the error `python(59220,0x1e3215000) malloc: Corruption of free object 0x14f617910` when running in the VS Code terminal, prepend your commands with: `MallocNanoZone=1`

Train MNIST
---

Note from the docs: To connect to the Ray on Vertex AI cluster using the Ray on Vertex AI SDK, the connecting environment must be on the same peered VPC network.

Execute the following to train an MNIST model using PyTorch:

```
python main.py  --cluster <cluster name> --region <region name> --project_number <project number (not ID)> 
```

Create Cluster
---

Execute the following to create a cluster:
```
python create_cluster.py --cluster <cluster name> --network projects/<project_number>/global/networks/<vpc_name>
```

You should see the following:

```
Creating cluster with arguments cluster=<cluster name> - network=<network address>
[Ray on Vertex AI]: Cluster State = State.PROVISIONING
Waiting for cluster provisioning; attempt 1; sleeping for 0:02:30 seconds
[Ray on Vertex AI]: Cluster State = State.PROVISIONING
Waiting for cluster provisioning; attempt 2; sleeping for 0:01:54.750000 seconds
...
[Ray on Vertex AI]: Cluster State = State.PROVISIONING
Waiting for cluster provisioning; attempt 12; sleeping for 0:00:30.064907 seconds
[Ray on Vertex AI]: Cluster State = State.RUNNING
Cluster create-cluster-test created.

```

Delete Cluster
---

Execute the following to delete a cluster:
```
python delete_cluster.py --cluster <cluster name> --region <region name> --project_number <project number (not ID)> 
```
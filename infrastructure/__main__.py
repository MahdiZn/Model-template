"""An AWS Python Pulumi program"""
import sys
sys.path.append("C:/Users/loli/AppData/Local/Programs/Python/Python310/Lib/site-packages/")

import pulumi
import pulumi_aws as aws
from pulumi_aws import s3
import pulumi_eks as eks
import pulumi_random as random


# Create an EKS cluster with the default configuration.
cluster = eks.Cluster('my-cluster',create_oidc_provider=True)

# Export the cluster's kubeconfig.
pulumi.export('kubeconfig', cluster.kubeconfig)

#create database postgresql for model metadata in mflow
#create a random pass with pulumi
password = random.RandomPassword("password",
    length=16,
    special=True,
    override_special="_%@")


mlflowDB = aws.rds.Instance("mlflow-db",
    allocated_storage=10,
    db_name="mlflow",
    engine="postgres",
    engine_version="11.10",
    instance_class="db.t3.micro",
    #parameter_group_name="default.mysql5.7",
    password=password.result,
    skip_final_snapshot=True,
    username="postgres",
    vpc_security_group_ids=[cluster.cluster_security_group.id,cluster.node_group_options.id]
    #asegurara que el cluster eks tiene acceso a la db por alli donde se levanta mlflow ,
    # vpc_security_group_ids: Optional[Sequence[str]] = None,
    )




# Create an AWS resource (S3 Bucket)
#bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
#pulumi.export('bucket_name', bucket.id)

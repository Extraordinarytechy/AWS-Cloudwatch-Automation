import boto3
from datetime import datetime, timedelta

#Initilize S3 & cloudwatch clients
s3 = boto3.client("s3")
cloudwatch = boto3.client("cloudwatch")

#Fetch and list available S3 buckets 
buckets = s3.list_buckets()["Buckets"]

if not buckets:
    print("No S3 buckets found in your account:")
    exit()


print("\nAvailable S3 Buckets:")
for idx, bucket in enumerate(buckets, start=1):
    print(f"{idx}. {bucket['Name']}")

#Let the user select a bucket
user_input = input("\nEnter the number of the bucket to monitor:").strip()

if user_input.isdigit():
    index = int(user_input) - 1

    if 0 <= index < len(buckets):
        bucket_name = buckets[index]["Name"]

    else:
        print("Invalid selection. Existing.")
        exit()
else: 
    print("Invalid input. Please enter a number.")
    exit()

print(f"\nSelecte Bucket: {bucket_name}")

#Fetch storage metrics from cloudwatch
response = cloudwatch.get_metric_statistics(
    Namespace="AWS/S3",
    MetricName="BucketSizeBytes",
    Dimensions=[
        {"Name": "BucketName", "Value": bucket_name},
        {"Name": "StorageType", "Value": "StandardStorage"}
    ],
    StartTime=datetime.utcnow() - timedelta(days=1),
    EndTime=datetime.utcnow(),
    Period=86400,
    Statistics=["Average"]
)

#Fetch object count metrics

response_objects = cloudwatch.get_metric_statistics(
    Namespace="AWS/S3",
    MetricName="NumberOfObjects",
    Dimensions=[
        {"Name": "BucketName", "Value": bucket_name},
        {"Name": "StorageType", "Value": "AllStorageTypes"}
    ],
    StartTime=datetime.utcnow() - timedelta(days=1),
    EndTime=datetime.utcnow(),
    Period=86400,
    Statistics=["Average"]
)


# Extract and display results
if response["Datapoints"]:
    size_bytes = response["Datapoints"][0]["Average"]
    print(f"\nStorage Size: {size_bytes / (1024 ** 3):.2f} GB")
else:
    print("\nNo storage data available. Ensure CloudWatch metrics are enabled.")

if response_objects["Datapoints"]:
    object_count = response_objects["Datapoints"][0]["Average"]
    print(f"Number of Objects: {int(object_count)}")
else:
    print("No object count data available. Ensure CloudWatch metrics are enabled.")

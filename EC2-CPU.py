import boto3

from datetime import datetime, timedelta



#Initialize AWS clients

ec2 = boto3.client('ec2',region_name='ap-south-1')
cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')


#Function to list all EC2 instances (both running & stopped)

def list_instances(): 
    instances = ec2.describe_instances()
    instance_list = []
    print("\nAvailable Instances:")
    
    for idx, reservation in enumerate(instances['Reservations']):
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            print(f"{idx+1}. Instance ID: {instance_id}, State: {state}")
            instance_list.append((instance_id, state))

    return instance_list

# Fetch instances and Let user choose one
print("Fetching EC2 instances...")
instances = list_instances()  # Fetches instances as [(instance_id, state), ...]

if not instances:
    print("No instances found. Exiting.")
    exit()

# Display instances in a numbered list
print("\nAvailable EC2 Instances:")
for idx, (instance_id, state) in enumerate(instances, 1):
    print(f"{idx}. {instance_id} ({state})")

# Ask user to select an instance by number or enter ID manually
user_input = input("\nEnter the number of the instance (or type the full Instance ID): ").strip()

# If the user enters a number, map it to the correct instance ID
if user_input.isdigit():
    index = int(user_input) - 1  # Convert to 0-based index
    if 0 <= index < len(instances):
        chosen_instance, instance_state = instances[index]  # Unpack tuple (ID, State)
        chosen_instance = chosen_instance.strip()  # Remove unwanted characters
    else:
        print("Invalid selection. Exiting.")
        exit()
else:
    chosen_instance = user_input.strip()  # Fix missing parentheses

# Validate instance ID format
if not chosen_instance.startswith("i-"):
    print("Error: Invalid EC2 instance ID format.")
    exit()

print(f"\nYou selected: {chosen_instance}")

# Fetch CPU Utilization for the selected instance
response = cloudwatch.get_metric_statistics(
    Namespace="AWS/EC2",
    MetricName="CPUUtilization",
    Dimensions=[{"Name": "InstanceId", "Value": chosen_instance}],
    StartTime=datetime.utcnow() - timedelta(minutes=30),  # Changed from 5 to 30 minutes
    EndTime=datetime.utcnow(),
    Period=300,
    Statistics=["Average"]
)

# Debugging Output
print(f"DEBUG: Chosen Instance ID -> {repr(chosen_instance)}")

# Check if CloudWatch returned data
if "Datapoints" not in response or not response["Datapoints"]:
    print("No CloudWatch data available. Ensure CloudWatch monitoring is enabled for this instance.")
    exit()

print("\nCPU Utilization Data:", response["Datapoints"])



#Fetch CPU Utilization for the selected instance

response = cloudwatch.get_metric_statistics(
    Namespace="AWS/EC2",
    MetricName="CPUUtilization",
    Dimensions=[{"Name": "InstanceId", "Value": chosen_instance.strip()}],
    StartTime=datetime.utcnow() - timedelta(minutes=5),
    EndTime=datetime.utcnow(),
    Period=300,
    Statistics=["Average"]
)


#Print the result

if instance_state == "stopped":
    print("\nWarning: The selected instance is STOPPED. CloudWatch will only show past metrics, not real-time data.")
else:
    print("\nFetching real-time CPU Utilization...")


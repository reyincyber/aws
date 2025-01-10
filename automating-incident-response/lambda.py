import boto3
import json
from botocore.exceptions import ClientError
ec2 = boto3.client('ec2')
def lambda_handler(event, context):
    try:
        # Log the incoming event to see its structure
        print(f"Received event: {json.dumps(event)}")
        # Extract instance ID from the event details
        if 'detail' in event and 'resource' in event['detail'] and 'instanceDetails' in event['detail']['resource']:
            instance_id = event['detail']['resource']['instanceDetails']['instanceId']
        else:
            return {
                'statusCode': 400,
                'body': json.dumps("Error: Event structure is not as expected.")
            }
        # Isolate the instance by modifying its security group
        response_sg = ec2.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=['sg-01234....fg']  # Replace with your IsolatedSecurityGroup ID
        )
        print(f"Instance {instance_id} isolated: {response_sg}")
        # Stop the compromised instance
        response_stop = ec2.stop_instances(
            InstanceIds=[instance_id]
        )
        print(f"Instance {instance_id} stopped: {response_stop}")
        return {
            'statusCode': 200,
            'body': json.dumps(f"Instance {instance_id} successfully isolated and stopped.")
        }
    except ClientError as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }

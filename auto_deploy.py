import boto3
import time
import base64
import subprocess
import json

# === CONFIG ===
REGION = 'us-east-1'
ASG_NAME = 'my-app-asg'
S3_BUCKET = 'my-app-bucket'
S3_APP_ZIP = 'latest-app.zip'
INSTANCE_TYPE = 't3.medium'
KEY_NAME = 'my-key-pair'
MIN_HEALTHY_PERCENT = 90

# AWS Clients
ec2 = boto3.client('ec2', region_name=REGION)
asg = boto3.client('autoscaling', region_name=REGION)
ssm = boto3.client('ssm', region_name=REGION)
elb = boto3.client('elbv2', region_name=REGION)

def run_terraform():
    print("Applying Terraform IaC...")
    result = subprocess.run(["terraform", "init"], cwd="terraform", capture_output=True)
    result = subprocess.run(["terraform", "apply", "-auto-approve"], cwd="terraform", capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Terraform failed: {result.stderr.decode()}")
    
    output = subprocess.run(["terraform", "output", "-json"], cwd="terraform", capture_output=True, text=True)
    tf_output = json.loads(output.stdout)
    return tf_output

def get_instance_id():
    response = asg.describe_auto_scaling_groups(AutoScalingGroupNames=[ASG_NAME])
    for inst in response['AutoScalingGroups'][0]['Instances']:
        if inst['LifecycleState'] == 'InService':
            return inst['InstanceId']

def patch_and_harden(instance_id):
    print(f"Patching & hardening {instance_id} via SSM...")
    patch_cmd = "Install-Module PSWindowsUpdate -Force; Get-WUList | Install-WUUpdate -AcceptAll -AutoReboot"
    ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunPowerShellScript', Parameters={'commands': [patch_cmd]})
    # Wait logic simplified for brevity

def create_ami(instance_id):
    ami = ec2.create_image(InstanceId=instance_id, Name=f"hardened-ami-{int(time.time())}", NoReboot=True)
    ec2.get_waiter('image_available').wait(ImageIds=[ami['ImageId']])
    return ami['ImageId']

def main():
    try:
        # 1. Apply Terraform (VPC, ASG, ALB)
        tf = run_terraform()
        ami_id = create_ami(get_instance_id())
        
        # 2. Update Launch Template with new AMI
        ec2.create_launch_template_version(
            LaunchTemplateName=tf['launch_template_name']['value'],
            SourceVersion='$Latest',
            LaunchTemplateData={'ImageId': ami_id}
        )
        
        # 3. Trigger ASG Refresh
        asg.start_instance_refresh(
            AutoScalingGroupName=ASG_NAME,
            Strategy='Rolling',
            Preferences={'MinHealthyPercentage': MIN_HEALTHY_PERCENT}
        )
        print("Automation complete! Zero-downtime rollout in progress.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

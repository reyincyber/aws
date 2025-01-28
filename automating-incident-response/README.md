# Automating EC2 Instance Isolation with AWS Lambda and GuardDuty

![image alt](https://github.com/reyincyber/aws/blob/a62ca55ed1a79838400d853ac95882f37a783510/automating-incident-response/architectural%20diagrams/automating_idr_bc.drawio.png)

This repository provides a detailed guide for setting up an automated workflow to isolate compromised EC2 instances in response to AWS GuardDuty findings. The workflow uses EC2, GuardDuty, S3, EventBridge, and Lambda to detect, mitigate, and notify about security threats while adhering to the **principle of least privilege** for IAM roles and policies.

---

## Table of Contents
1. [Project Overview](#project-overview)
   - [🔗 Code and Documentation:](#🔗-Code-and-documentation:)
3. [Setup Instructions](#setup-instructions)
   - [Create IAM Role](#1-create-an-iam-role)
   - [Enable GuardDuty](#2-enable-guardduty)
   - [Launch EC2 Instances](#3-launch-two-ec2-instances)
   - [Create Restricted Security Group](#4-create-a-restricted-security-group)
   - [Add Threat List to S3](#5-add-threat-list-file-to-s3-and-configure-guardduty-threat-list)
   - [Set Up Lambda Function](#6-set-up-the-lambda-function)
   - [Configure EventBridge Rule](#7-configure-eventbridge-rule)
   - [Create SNS Topic for Notifications](#8-create-sns-topic-for-notifications)
4. [Testing the Workflow](#testing-the-workflow)
5. [Cleanup](#cleanup)
6. [Real-World Considerations](#real-world-considerations)
7. [References](#references)

---

## Project Overview

This project automates the process of detecting and isolating compromised EC2 instances in real-time, minimizing security risks. It is designed for AWS users of all levels, including beginners, and includes step-by-step instructions to deploy the required resources and configurations. Features:
- **Real-time Threat Detection:** Utilize Amazon GuardDuty to monitor malicious activities.
- **Automated Instance Isolation:** Use AWS Lambda to stop and isolate compromised instances.
- **Customizable Workflow:** Integrate a custom threat list using S3.
- **Notifications:** Receive real-time email alerts via SNS.

🔗 Code and Documentation:
[GitHub Repository](https://github.com/reyincyber/aws-security/tree/861c663e487afa7e966cab4069c6db1d76fa8ace/automating-incident-response)
[Medium Walkthrough](https://cyberrey.medium.com/automating-ec2-instance-isolation-with-aws-lambda-and-guardduty-33a34fc88177)
[Youtube](https://youtu.be/RCmdjOjsGUw)

---

## Setup Instructions

### 1. Create an IAM Role

**Purpose:** Enable Lambda to manage security groups, stop instances, and interact with GuardDuty.

1. Navigate to the **IAM Console** → **Roles** → **Create Role**.
2. Select **AWS Service** → **Lambda** under trusted entities.
3. Attach the following policies:
   - `AmazonEC2FullAccess`
   - `AWSLambdaFullAccess`
4. Name the role (e.g., `LambdaSecurityRole`) and create it.

---

### 2. Enable GuardDuty

**Purpose:** Monitor for malicious activities in your AWS environment.

1. Open the **GuardDuty Console**.
2. Click **Enable GuardDuty** if not already enabled.

---

### 3. Launch Two EC2 Instances

**Purpose:** Simulate a malicious actor (`MaliciousEC2`) and a compromised instance (`CompromisedEC2`).

1. In the **EC2 Console**, click **Launch Instance**.
2. Configure the instances:
   - **AMI:** Amazon Linux 2
   - **Type:** `t2.micro`
   - **User Data Script:**
     ```bash
     #!/bin/bash
     yum update -y
     yum install nmap -y
     ```
3. Name the instances `MaliciousEC2` and `CompromisedEC2`.

---

### 4. Create a Restricted Security Group

**Purpose:** Restrict traffic to isolate compromised instances.

1. In **Security Groups**, create a new group:
   - **Name:** `IsolatedSecurityGroup`
   - **Inbound Rules:** SSH (Port 22) from your IP.
   - **Outbound Rules:** Default.

---

### 5. Add Threat List File to S3 and Configure GuardDuty Threat List

**Purpose:** Simulate threats using an S3-hosted IP list.

1. Create an **S3 Bucket** (e.g., `threat-list-bucket`).
2. Upload a `threatlist.txt` file containing `MaliciousEC2`'s IP.
3. Configure GuardDuty to use the S3 threat list:
   - Navigate to **GuardDuty** → **Settings** → **Threat Lists**.
   - Add the S3 URL of your threat list file.

---

### 6. Set Up the Lambda Function

**Purpose:** Automate the response to GuardDuty findings.

1. Create a Lambda function (`IsolateInstance`) with Python 3.8+ as the runtime.
2. Add the [Python code](https://github.com/reyincyber/aws/blob/e2619c4c47ea91bdf671186a4abbc0d18a86380f/automating-incident-response/lambda.py).
3. Assign the `LambdaSecurityRole` to the function.
4. Deploy and test the function.

---

### 7. Configure EventBridge Rule

**Purpose:** Trigger Lambda on GuardDuty findings.

1. Create a new rule in **EventBridge**:
   - **Name:** `GuardDutyToLambdaRule`
   - **Event Source:** GuardDuty
   - Use the [event pattern JSON](https://github.com/reyincyber/aws/blob/65bc7573964be2e71d8c3fbaa0159592a62f65be/automating-incident-response/event_pattern.json).
   - **Target:** Lambda function (`IsolateInstance`).

---

### 8. Create SNS Topic for Notifications

**Purpose:** Notify users of security events.

1. Create an SNS Topic (`GuardDutyNotifications`).
2. Subscribe your email to the topic and confirm via email.

---

## Testing the Workflow
![image alt](https://github.com/reyincyber/aws/blob/main/automating-incident-response/architectural%20diagrams/automating_idr_ac.drawio.png)
1. Connect to `CompromisedEC2` via SSH.
2. Execute a payload script to simulate malicious activity. Script reference: [test.sh](https://github.com/reyincyber/aws/blob/95e71ee372768d4f1e1f3c556d28d03c79a9220a/automating-incident-response/test.sh).
3. Verify:
   - GuardDuty findings.
   - Isolation and stopping of `CompromisedEC2`.
   - SNS notifications.

---

## Cleanup

1. Delete all resources:
   - EC2 instances
   - Lambda functions
   - S3 bucket
   - IAM roles
   - EventBridge rules
   - SNS topics
2. Verify that no resources are left to avoid unnecessary costs.

---

## Real-World Considerations

1. **Instance Availability:** Use severity-based isolation strategies to avoid unnecessary disruptions.
2. **Minimizing False Positives:** Fine-tune GuardDuty and use suppression rules.
3. **Enhanced Security Practices:** Implement comprehensive logging and multi-layer security.

---

## References

1. [Cloud4DevOps](https://www.youtube.com/watch?v=ZRpLrPjvNkk)
2. [AWS Incident Response Blog](https://aws.amazon.com/blogs/security/how-to-automate-incident-response-to-security-events-with-aws-systems-manager-incident-manager/)
3. [Automatically Isolate EC2 Instances](https://perd1x.medium.com/automatically-isolate-compromised-ec2-instances-with-guardduty-d4080e8b039a)

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contributing**
Contributions are welcome! Feel free to open an issue or submit a pull request for improvements or fixes.

---

## **Author**
Created by [reyincyber](https://github.com/reyincyber). Follow for more cloud security projects!

Automating Incident Detection and Response in AWS Using GuardDuty, EventBridge, and Lambda


Project Overview

This project leverages AWS GuardDuty, Lambda, EventBridge, and SNS to automate incident response for potential security threats detected in Amazon EC2 instances. The goal is to isolate compromised instances, store findings for investigation, and notify the security team — all while adhering to the AWS Well-Architected Framework and security best practices.

 Tools & Technologies Used

![image alt](https://github.com/reyincyber/aws/blob/a62ca55ed1a79838400d853ac95882f37a783510/automating-incident-response/architectural%20diagrams/automating_idr_bc.drawio.png)
Before Compromise
1. AWS IAM (Identity and Access Management): To manage permissions and roles securely.
2. AWS GuardDuty: For continuous monitoring and detection of security threats.
3. AWS Lambda: To execute automated functions in response to detected threats.
4. Amazon EventBridge: To manage event-driven workflows and trigger Lambda functions.
5. Amazon SNS (Simple Notification Service):  For sending notifications regarding security events.
6. Amazon EC2: Compute service where instances are monitored and managed.

Methods
1. An IAM role was set up with `AmazonEC2FullAccess` and `AWSLambda_FullAccess` permissions, allowing the Lambda function to control EC2 instances and handle necessary AWS service interactions.
2. GuardDuty was enabled to monitor EC2 instances, focusing on identifying unauthorized access attempts or potential malware infections.
3. An `IsolatedSecurityGroup` was created to restrict network access for compromised instances, with minimal inbound rules for internal control only.
4. An EventBridge rule was created to trigger the Lambda function when GuardDuty detects a Medium or High-severity finding. The rule pattern specifically focuses on findings related to EC2 instances.
5. A Lambda function was created with Python code to: Stop the compromised EC2 instance; and attach the isolated security group to the instance. The IAM role from Step 2 was attached to this Lambda function to allow it to manage EC2 instance attributes.
6. Two SNS subscriptions were set up to receive notifications for: Medium to low-severity findings in GuardDuty; and Lambda function execution to alert administrators when an instance has been isolated and stopped.
7. An S3 bucket was set up with a threatlist.txt file containing the IP address of a malicious instance. This file was added to the GuardDuty ThreatList configuration to simulate real-world threat scenarios.

Testing the Setup:

![image alt](https://github.com/reyincyber/aws/blob/main/automating-incident-response/architectural%20diagrams/automating_idr_ac.drawio.png)
After Compromise
1. Simulate Threats with Malicious Activity: SSH was used to connect to a CompromisedEC2 instance, from which a port scan was conducted against a MaliciousEC2 instance to simulate a network attack.
2. Observe GuardDuty Findings: GuardDuty findings were monitored to confirm the detection of the malicious activity, resulting in a High or Medium severity alert.
3. Validate Automated Response: Upon detecting the simulated attack, EventBridge triggered the Lambda function, which: Stopped the CompromisedEC2 instance and Applied the IsolatedSecurityGroup to remove it from the main network.
4. This response was verified in the EC2 dashboard, where the instance’s status was shown as stopped, and the security group was updated.

Real World Application

It is important to note the following while deploying this set up in real life:
1. Ensuring Instance Availability: Adopt a severity-based response strategy where high-severity threats trigger immediate isolation, while medium and low-severity threats prompt monitoring and alerts without disrupting instance operations. Instead of stopping instances outright, consider reassigning them to a quarantine security group with restricted access, allowing continued operation for investigation purposes. Automate security best practices to enhance scalability and reduce manual intervention.
2. Minimizing False Positives: Implement suppression rules in AWS GuardDuty to filter out non-critical findings, focusing on actionable threats. Regularly update threat intelligence sources to maintain detection accuracy. Fine-tune detection thresholds to balance sensitivity and specificity, reducing the likelihood of false alarms.
3. Incorporating Feedback and Best Practices: Enable traceability by configuring comprehensive logging and monitoring across all layers of the workload. Apply security controls at every layer, including network, instance, and application levels, to implement a defense-in-depth strategy. Regularly conduct security reviews and audits to ensure compliance with evolving best practices and organizational requirements.

Conclusions

Automating the isolation of compromised EC2 instances in response to AWS GuardDuty findings enhances security by reducing response times and limiting potential damage from security incidents. By implementing the recommended improvements, such as minimizing false positives and ensuring instance availability, and adhering to the AWS Well-Architected Framework's security principles, organizations can achieve a robust and resilient security posture in their AWS environments.

References

1. Cloud4DevOps. (2022, November 9). Security Hub remediations with GuardDuty Detection | Hands-on walkthrough | Cloud4DevOps [Video]. YouTube. https://www.youtube.com/watch?v=ZRpLrPjvNkk 
2. How to automate incident response to security events with AWS Systems Manager Incident Manager | Amazon Web Services. (2021, September 17). Amazon Web Services. https://aws.amazon.com/blogs/security/how-to-automate-incident-response-to-security-events-with-aws-systems-manager-incident-manager/ 
3. Perd1x. (2024, July 27). Automatically Isolate Compromised EC2 Instances with GuardDuty. Medium. https://perd1x.medium.com/automatically-isolate-compromised-ec2-instances-with-guardduty-d4080e8b039a 

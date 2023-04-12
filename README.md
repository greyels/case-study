### Proposed Solution

To design a cloud-native service with AWS resources that receives a lot of JSON messages, transforms, enriches them with data from an external data source and upload to a database, we are going to use the following architecture and services: 
 
![Solution Architecture](https://github.com/greyels/drawio/blob/main/aws_de_challenge.png)

1.	Amazon API Gateway: This will be the entry point for the messages that are sent to the service. The API Gateway can handle large amounts of traffic and can be easily scaled to handle more requests as the traffic increases.
2.	AWS Lambda: There are three Lambda functions utilized:
a.	First one is used to transform, enrich the incoming messages that are received by the API Gateway/SQS reading the user data from RDS, and write results to DynamoDB service.
b.	Second one is used to backup source messages from API Gateway/SQS to S3.
c.	Third one is used to trigger a Glue job on new data written to DynamoDB.
3.	Amazon Simple Queue Service (SQS): SQS is a managed message queuing service. We use SQS to buffer messages between the API Gateway and the Lambda function, ensuring that messages are not lost if there is a spike in traffic or if the Lambda functions are temporarily unavailable.
4.	AWS DynamoDB: We use DynamoDB to store the enriched messages before writing them to the Event Database via Glue job triggered by third Lambda function.
5.	Amazon S3: S3 is used to store the messages that are received from the API Gateway. This can serve as a backup and provide a way to access the messages for auditing purposes in future. Messages are read from SQS and processed by second Lambda function.
6.	AWS Glue: There are two services used in the architecture:
a.	First one is used to extract and load data from the external User Database into AWS RDS for further usage by first Lambda function. The Glue job can be scheduled to run at regular intervals to keep the data in RDS up to date.
b.	Second one is used to copy final event data from DynamoDB to the external Event Database. The job is triggered by third Lambda function. It updates entries in DynamoDB in case they are successfully processed.
7.	Amazon RDS: RDS is used to store user related data to be utilized by first Lambda function on messages enrichment process. It can be easily scaled to handle large amounts of user data.
8.	Amazon Athena: Athena could be useful for querying and examine source data stored on S3 or final data stored in DynamoDB.

This architecture provides a scalable, reliable, and cost-effective solution for receiving, transforming, and storing large amounts of messages in a cloud-native environment.
To ensure that the designed service is scalable and resilient against common error cases, we can take the following measures (not shown in the architecture diagram above):
1.	Connection problems with one of the databases: In case of a connection problem with the User Database (RDS in cloud), we can enable Amazon RDS Multi-AZ deployment. This will automatically create a replica of the primary database in a different availability zone. If the primary database becomes unavailable, Amazon RDS will automatically promote the replica to the primary database. In case of external DBs are unreachable - we already have replica DB (RDS) for User Database, which is used for messages enrichment, and DynamoDB where all final messages are stored, so we can update external Event Database with the latest entries when it becomes available again.
2.	Network issues: We can deploy the service across multiple availability zones to ensure high availability and fault tolerance. We can also utilize Amazon CloudFront to distribute traffic across multiple regions and reduce latency.
3.	Outage of an AWS resource: In case of an outage of an AWS resource, we can use Amazon CloudWatch alarms to monitor the health of the resources and notify if there are issues with our resources. Also, AWS Auto Scaling feature automatically adjusts the capacity of the resources based on the demand.
4.	Downtimes during deployment: We can use AWS CodeDeploy to automate the deployment of new versions of the Lambda functions and the API Gateway. This ensures that there is no downtime during the deployment process. It deploys the new version of the function in a rolling manner.

In addition to the above measures, we can also implement automated backups and disaster recovery procedures. We can use Amazon CloudFormation to create templates of the infrastructure, which can be used to deploy the service to a different region in case of a disaster. We can also use Amazon Route 53 to redirect traffic to the new region.
Overall, these measures will ensure that the service is scalable and resilient against the most common error cases.

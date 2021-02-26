"""
Local Measure
Bennett Borofka, Solutions Architect - bennett@getlocalmeasure.com

This Python script is intended for use in a Python 3.8 Lambda Function,
invoked by a Contact Flow in Amazon Connect. It accepts the following
function input attributes: to, subject, message, cc.

References:
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html
https://docs.aws.amazon.com/connect/latest/adminguide/connect-lambda-functions.html
"""

import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    sender = event["Details"]["Parameters"]["from"]

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    recipient = event["Details"]["Parameters"]["to"]
    cc = event["Details"]["Parameters"]["cc"]

    # If necessary, replace us-west-2 with the AWS Region you're using for
    # Amazon SES.
    aws_region = "us-east-1"

    # The subject line for the email.
    subject = event["Details"]["Parameters"]["subject"]

    # The email body for recipients with non-HTML email clients.
    body_text = event["Details"]["Parameters"]["message"]

    # The character encoding for the email.
    charset = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=aws_region)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
                'ccAddresses': [
                    cc,
                ],
            },
            Message={
                'Body': {

                    'Text': {
                        'charset': charset,
                        'Data': body_text,
                    },
                },
                'subject': {
                    'charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

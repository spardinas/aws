import boto3
import random
from botocore.exceptions import NoCredentialsError

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    bucket_name = 'your-bucket-name'  # replace with your bucket name

    try:
        # Get the list of objects in the bucket
        objects = s3_client.list_objects(Bucket=bucket_name)['Contents']

        # Select a random object
        random_object = random.choice(objects)

        # Get the URL of the random object
        url = "{}/{}/{}".format(s3_client.meta.endpoint_url, bucket_name, random_object['Key'])

        # Generate the HTML for the website
        html = f"""
            <!DOCTYPE html>
            <html>
            <body>
                <img src="{url}" alt="Random Image">
            </body>
            </html>
        """

        return {
            'statusCode': 200,
            'headers': { 'Content-Type': 'text/html' },
            'body': html
        }
    except NoCredentialsError:
        return {
            'statusCode': 500,
            'body': 'Error in getting credentials'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'An error occurred: ' + str(e)
        }


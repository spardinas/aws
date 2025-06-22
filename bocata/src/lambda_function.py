import boto3
import os
import random

s3 = boto3.client('s3')
BUCKET = os.environ.get('BUCKET_NAME')
KEYS = os.environ.get('IMAGE_KEYS', '').split(',')

def lambda_handler(event, context):
    if not BUCKET or not KEYS or KEYS == ['']:
        return {
            'statusCode': 500,
            'headers': { 'Content-Type': 'text/plain' },
            'body': 'Bucket not configured'
        }

    image_key = random.choice(KEYS).strip()
    url = s3.generate_presigned_url('get_object',
                                    Params={'Bucket': BUCKET, 'Key': image_key},
                                    ExpiresIn=300)

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Bocata aleatorio</title>
        <style>
            body {{ font-family: sans-serif; text-align: center; padding: 2rem; }}
            img {{ max-width: 90%; height: auto; margin-top: 2rem; border: 1px solid #ccc; }}
            button {{ margin-top: 2rem; padding: 0.5rem 1.2rem; font-size: 1rem; }}
        </style>
    </head>
    <body>
        <h1>¡Bocata aleatorio servido!</h1>
        <img src="{url}" alt="Bocata sorpresa">
        <br>
        <button onclick="window.location.reload()">🔄 Otro bocata</button>
    </body>
    </html>
    """

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
            'Cache-Control': 'no-store'
        },
        'body': html
    }

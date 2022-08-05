import requests
import json
import boto3

s3 = boto3.client('s3')

def extract_title(url, context):
    ''' Receives url, get title and create json. Upload to s3 bucket and returns json '''
    bucket = 'aws-test-bucket'
    response = None
    try: 
        # gets title 
        html = requests.get(url).text
        title = html.split('</title>')[0].split('<title>')[1]
        # creates dict with values
        url_to_title = dict(
            url = url,
            title = title
        )
        file_name = f'{title[:4]}.json'
        json_response = json.dumps(url_to_title)
        # to bytes 
        byte_stream = bytes(json_response.encode('UTF-8'))
        # put in s3 bucket
        s3.put_object(Bucket=bucket, Key=file_name, Body=byte_stream)
        response = {
            'statusCode' : 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json_response
        }
    except requests.exceptions.RequestException as error:
        print("Error: ", error)
    finally:
        return response



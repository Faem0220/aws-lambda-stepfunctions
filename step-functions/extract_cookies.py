import requests
import json
import boto3

s3 = boto3.client('s3')

def extract_cookies(url, context):
    ''' Receives url, get cookies and create json. Upload to s3 bucket and returns json '''
    bucket = 'aws-test-bucket'
    response = None
    try: 
        # gets title 
        r = requests.get(url)
        cookies = r.cookies.get_dict()
        sess = cookies['_gh_sess']
        file_name = f'{sess[:5]}.json'
        json_response = json.dumps(cookies)
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
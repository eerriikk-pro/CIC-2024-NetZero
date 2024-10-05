import json
import boto3
import os

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')
def lambda_handler(event, context):
    # Initialize the Bedrock Runtime client]
    query_string = event['query-string']
    # Define the request parameters
    model_id = "amazon.titan-embed-text-v2:0"
    content_type = "application/json"
    accept = "*/*"
    body = {
        "inputText": query_string,
        "dimensions": 1024,
        "normalize": False
    }
    
 
    # Invoke the model
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    
    # Read the response
    response_body = response['body'].read().decode('utf-8')
    
    print(response_body)
    return {
        'statusCode': 200,
        'body': response_body
    }
    
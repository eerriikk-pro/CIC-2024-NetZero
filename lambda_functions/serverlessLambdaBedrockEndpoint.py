import json
import os
import boto3
import urllib3

# client = boto3.client('bedrock-runtime',
#     region_name='us-west-2',# def lambda_handler(event, context):
#     body = json.loads(event.get('body', '{}'))
#     #setting defult prompt if none provided
#     prompt = body.get('prompt', 'Write a text to be posted on my social media channels about how Amazon Bedrock works')
    
#     body = json.dumps({
#         'prompt': "\n\nHuman:" + prompt + "\n\nAssistant:",
#         "temperature": 0.5,
#         "top_p": 1,
#         "top_k": 250,
#         "max_tokens_to_sample": 200,
#         "stop_sequences": ["\n\nHuman:"]
#     }) #all parameters (except for prompt) are set to default values

#     modelId = "us.meta.llama3-2-3b-instruct-v1:0"
#     accept = 'application/json'
#     contentType = 'application/json'

#     response = client.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
#     response_body = json.loads(response.get('body').read())

#     return {
#         'statusCode': 200,
#         'body': json.dumps({
#             'generated-text': response_body
#         })
#     }

       

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id=os.getenv('CHARITY_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('CHARITY_AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('CHARITY_AWS_SESSION_TOKEN'))
    
def invoke_bedrock_summary(content):
    prompt = content
    # Call the Bedrock model to generate the summary
    summary = invoke(prompt, temperature=0.7, max_tokens=4096)
    return summary


def invoke(prompt, temperature, max_tokens):
    # Configuration for the Bedrock model invocation
    prompt_config = {
        "prompt": f'\n\nHuman: {prompt} \n\nAssistant:',
        "temperature": temperature
    }

    response = bedrock_runtime.invoke_model(
        body=json.dumps(prompt_config),
        modelId="us.meta.llama3-2-3b-instruct-v1:0")
        

    response_body = json.loads(response['body'].read())
    print(response_body)

    return {
            'statusCode': 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allo`w-Methods": "*",
            },
            'body': json.dumps(response_body)
    }


     
def lambda_handler(event, context):
    return invoke_bedrock_summary(event['prompt'])
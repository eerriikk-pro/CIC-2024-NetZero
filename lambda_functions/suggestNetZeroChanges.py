import json
import os
import boto3
import urllib3

       

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id=os.getenv('CHARITY_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('CHARITY_AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('CHARITY_AWS_SESSION_TOKEN'))
    
def invoke_bedrock_summary(content):
    prompt = content
    prompt = """<instruction>
You are a <persona>Climate Action and Sustainability Analyst </persona>.

If the generative AI project given in the description below can be accomplished via non-generative methods, please suggest one or more non-generative-ai algorithms that can accomplish the task in the output and how the described project can be solved using these non-generative-ai algorithmns.
The description of the project is <description>""" + content + """</description>.
</instruction>"
<instruction>
Your are also to provide the response that "Since 90% of the energy used by a large, scalable project, by hosting it in a data center or on a cloud, you can reduce the amount of emissions by hosting within cloud". Please vary the text to have the same meaning but different wording.
</instruction> <instruction>Ensure you return the result as a string</instruction>"""
    # Call the Bedrock model to generate the summary
    summary = invoke(prompt, temperature=1, max_tokens=4096)
    return summary


def invoke(prompt, temperature, max_tokens):
    # Configuration for the Bedrock model invocation
    prompt_config = {
        "prompt": prompt,
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
    return invoke_bedrock_summary(event['description'])
import boto3
import json

# Initialize clients
kendra_client = boto3.client('kendra', region_name='us-east-1')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def query_kendra(query_text, index_id):
    """Query Kendra index and return relevant results."""
    response = kendra_client.query(
        IndexId=index_id,
        QueryText=query_text
    )
    
    # Extract and format relevant passages from results
    context = ""
    for result in response['ResultItems']:
        if result['Type'] == 'DOCUMENT':
            if 'DocumentExcerpt' in result:
                context += result['DocumentExcerpt']['Text'] + "\n\n"
    
    return context

def query_bedrock(query, context):
    """Query Bedrock's Titan G1 Express model with context from Kendra."""
    prompt = f"""
    Context information:
    {context}
    
    Based on the above context, please answer the following question: {query}
    """
    
    # Payload for Titan G1 Express model following your exact format
    payload = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 8192,
            "stopSequences": [],
            "temperature": 0,
            "topP": 1
        }
    }
    
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-text-express-v1",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload)
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['results'][0]['outputText']

def kendra_bedrock_query(user_query, index_id):
    """End-to-end process to query Kendra and use results with Bedrock."""
    # Get context from Kendra
    context = query_kendra(user_query, index_id)
    
    # Get response from Bedrock using the context
    response = query_bedrock(user_query, context)
    
    return response

# Example usage
if __name__ == "__main__":
    INDEX_ID = "7689ec60-07ce-4a78-a993-38033404789d"
    # user_question = "What is cost cap administration?"
    # user_question = "How much is a team eligible to spend each year?"
    # user_question = "What is the punishment for cost cap breach?"
    user_question = "What are the sanctions for cost cap breach?"

    answer = kendra_bedrock_query(user_question, INDEX_ID)
    print(answer)
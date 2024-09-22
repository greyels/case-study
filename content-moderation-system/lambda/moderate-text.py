import json

import boto3

# Initialize the Amazon Comprehend client
comprehend = boto3.client('comprehend')


def lambda_handler(event, context):
    try:
        if event['requestContext']['http']['method'] == 'POST':
            # Call Amazon Comprehend to detect the sentiment of the text
            text = event["body"]
            sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
            entities = comprehend.detect_entities(Text=text, LanguageCode='en')
            key_phrases = comprehend.detect_key_phrases(Text=text, LanguageCode='en')

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'Sentiment': sentiment_response['Sentiment'],
                    'SentimentScore': sentiment_response['SentimentScore'],
                    'Entities': entities['Entities'],
                    'Key phrases': key_phrases['KeyPhrases']
                })
            }

    except Exception as e:
        # Handle errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

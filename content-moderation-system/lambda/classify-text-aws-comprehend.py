import json

import boto3

# Initialize the Amazon Comprehend client
comprehend = boto3.client('comprehend')


def lambda_handler(event, context):
    try:
        if event['requestContext']['http']['method'] == 'POST':
            # Call Amazon Comprehend to detect the sentiment of the text
            text = event['body']
            sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
            toxic_content_response = comprehend.detect_toxic_content(TextSegments=[{'Text': text}], LanguageCode='en')

            toxicity = toxic_content_response['ResultList'][0]['Toxicity'] * 100
            sentiment = sentiment_response['Sentiment']

            response = f'Your comment/post has {sentiment} sentiment and toxicity level = {toxicity:.2f}%. '

            if sentiment in ('POSITIVE', 'NEUTRAL') and toxicity < 45:
                verdict = "It has been automatically approved."
            elif sentiment == 'NEGATIVE' or toxicity > 55:
                verdict = "It has been automatically rejected."
            else:
                verdict = "It has been queued for manual moderation."

            return {
                'statusCode': 200,
                'body': f'{response}{verdict}'
            }

    except Exception as e:
        # Handle errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

import json
import boto3

translate = boto3.client('translate')


def lambda_handler(event, context):
    try:
        if event['requestContext']['http']['method'] == 'POST':
            text = event["body"]
            translation = translate.translate_text(
                Text=text,
                SourceLanguageCode='auto',
                TargetLanguageCode='en',
                Settings={'Profanity': 'MASK'}
            )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'InitialText': text,
                    'CorrectedText': translation['TranslatedText']
                })
            }

    except Exception as e:
        # Handle errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

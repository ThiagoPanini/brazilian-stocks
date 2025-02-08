# Configurações necessárias para mockar um DynamoDB para fins de testes
MOCKED_DYNAMODB_TABLE_NAME = "mocked_br_stocks_active_tickers"
MOCKED_DYNAMODB_TABLE_KEY_SCHEMA = [
    {
        "AttributeName": "code",
        "KeyType": "HASH"
    },
    {
        "AttributeName": "dt_extracted",
        "KeyType": "RANGE"
    }
]
MOCKED_DYNAMODB_TABLE_ATTRIBUTE_DEFINITIONS = [
    {
        "AttributeName": "code",
        "AttributeType": "S"
    },
    {
        "AttributeName": "dt_extracted",
        "AttributeType": "S"
    }
]
MOCKED_DYNAMODB_TABLE_BILLING_MODE = "PAY_PER_REQUEST"
MOCKED_BOTO3_CLIENT_REGION = "us-east-1"

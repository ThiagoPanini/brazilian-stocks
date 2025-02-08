import time
import pytest
import requests_mock
from moto import mock_aws

import boto3

from app.src.get_active_tickers.domain.entities.ticker import Ticker
from app.src.get_active_tickers.infra.adapters.fundamentus_adapter import (
    FundamentusGetTickersAdapter,
    RequestsAdapter,
    REQUESTS_ADAPTER
)

from app.src.get_active_tickers.infra.repositories.dynamodb_repository import (
    DynamodbTickersInfoRepository
)

from app.src.get_active_tickers.tests.mocks.mocked_fundamentus_adapter import (
    MOCKED_FUNDAMENTUS_GET_TICKERS_REQUESTS_RESPONSE
)

from app.src.get_active_tickers.tests.mocks.mocked_requests_adapter import (
    MOCKED_REQUESTS_URL,
    MOCKED_REQUESTS_TIMEOUT,
    MOCKED_REQUESTS_HEADERS,
    MOCKED_REQUESTS_NUM_RETRIES,
    MOCKED_REQUESTS_BACKOFF_FACTOR,
    MOCKED_REQUESTS_STATUS_FORCELIST
)

from app.src.get_active_tickers.tests.mocks.mocked_dynamodb_repository import (
    MOCKED_DYNAMODB_TABLE_NAME,
    MOCKED_DYNAMODB_TABLE_KEY_SCHEMA,
    MOCKED_DYNAMODB_TABLE_ATTRIBUTE_DEFINITIONS,
    MOCKED_DYNAMODB_TABLE_BILLING_MODE,
    MOCKED_BOTO3_CLIENT_REGION
)

from app.src.get_active_tickers.tests.mocks.mocked_entity_ticker import (
    MOCKED_TICKER
)


@pytest.fixture
@requests_mock.Mocker(kw="requests_mocker")
def fundamentus_get_tickers_response(**kwargs):
    # Mockando resposta do requests
    requests_mocker = kwargs["requests_mocker"]
    requests_mocker.get(
        url=REQUESTS_ADAPTER.get_url(),
        text=MOCKED_FUNDAMENTUS_GET_TICKERS_REQUESTS_RESPONSE
    )

    # Chamando método com requests mockado
    fundamentus_adapter = FundamentusGetTickersAdapter()
    ticker_objects = fundamentus_adapter.get_tickers()

    return ticker_objects


@pytest.fixture
def requests_adapter():
    return RequestsAdapter(
        url=MOCKED_REQUESTS_URL,
        timeout=MOCKED_REQUESTS_TIMEOUT,
        headers=MOCKED_REQUESTS_HEADERS,
        num_retries=MOCKED_REQUESTS_NUM_RETRIES,
        backoff_factor=MOCKED_REQUESTS_BACKOFF_FACTOR,
        status_forcelist=MOCKED_REQUESTS_STATUS_FORCELIST
    )


@pytest.fixture
@mock_aws
def mocked_dynamodb_client():
    return boto3.client("dynamodb", region_name=MOCKED_BOTO3_CLIENT_REGION)


@pytest.fixture
@mock_aws
def mocked_dynamodb_repository_setup(
    mocked_client = mocked_dynamodb_client,
    mocked_ticker: Ticker = MOCKED_TICKER
):
    def create_table_and_put_item():
        # Criando tabela mockada no DynamoDB
        r = mocked_client.create_table(
            TableName=MOCKED_DYNAMODB_TABLE_NAME,
            KeySchema=MOCKED_DYNAMODB_TABLE_KEY_SCHEMA,
            AttributeDefinitions=MOCKED_DYNAMODB_TABLE_ATTRIBUTE_DEFINITIONS,
            BillingMode=MOCKED_DYNAMODB_TABLE_BILLING_MODE
        )

        # Validando criação da tabela
        while True:
            r = mocked_client.describe_table(TableName=MOCKED_DYNAMODB_TABLE_NAME)
            status = r["Table"]["TableStatus"]

            if status == 'ACTIVE':
                break

            time.sleep(2)

        # Persistindo um item na tabela mockada
        mocked_dynamodb_repository = DynamodbTickersInfoRepository(
            table_name=MOCKED_DYNAMODB_TABLE_NAME,
            region_name=MOCKED_BOTO3_CLIENT_REGION
        )
        mocked_dynamodb_repository.persist(ticker=mocked_ticker)

    return create_table_and_put_item

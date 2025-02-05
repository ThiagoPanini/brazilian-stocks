import pytest
import requests_mock

from app.src.get_active_tickers.infra.adapters.fundamentus_adapter import (
    FundamentusGetTickersAdapter,
    RequestsAdapter,
    REQUESTS_ADAPTER
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

import pytest
import requests_mock

from app.src.get_active_tickers.infra.adapters.fundamentus_adapter import (
    FundamentusGetTickersAdapter,
    REQUEST_CONFIG_PARAMS
)

from app.src.get_active_tickers.tests.mocks.mocked_fundamentus_adapter import (
    MOCKED_FUNDAMENTUS_GET_TICKERS_REQUESTS_RESPONSE
)


@pytest.fixture
@requests_mock.Mocker(kw="requests_mocker")
def fundamentus_get_tickers_response(**kwargs):
    # Mockando resposta do requests
    requests_mocker = kwargs["requests_mocker"]
    requests_mocker.get(
        url=REQUEST_CONFIG_PARAMS["url"],
        text=MOCKED_FUNDAMENTUS_GET_TICKERS_REQUESTS_RESPONSE
    )

    # Chamando método com requests mockado
    adapter = FundamentusGetTickersAdapter()
    ticker_objects = adapter.get_tickers()

    return ticker_objects

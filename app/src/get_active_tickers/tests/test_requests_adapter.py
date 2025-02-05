from unittest.mock import patch
import requests
import pytest
import requests_mock

from app.src.get_active_tickers.infra.adapters.requests_adapter import RequestsAdapter

from app.src.get_active_tickers.tests.mocks.mocked_requests_adapter import (
    MOCKED_REQUESTS_URL
)



@pytest.mark.adapter
@pytest.mark.requests
def test_requests_adapter_raises_timeout_exception(requests_adapter: RequestsAdapter):
    """
    G: Dado que a aplicação necessita utilizar o adapter de requests para uma requisição HTTP
    W: Quando esta requisição extrapolar o tempo máximo de timeout
    T: Então uma exceção requests.Timeout precisa ser lançada
    """

    with patch("requests.sessions.Session.get", side_effect=requests.Timeout):
        with pytest.raises(requests.Timeout):
            _ = requests_adapter.get()


@pytest.mark.adapter
@pytest.mark.requests
def test_requests_adapter_raises_connection_error(requests_adapter: RequestsAdapter):
    """
    G: Dado que a aplicação necessita utilizar o adapter de requests para uma requisição HTTP
    W: Quando esta requisição retornar um erro de conexão
    T: Então uma exceção requests.Connectionerror precisa ser lançada
    """

    with patch("requests.sessions.Session.get", side_effect=requests.ConnectionError):
        with pytest.raises(requests.ConnectionError):
            _ = requests_adapter.get()


@pytest.mark.adapter
@pytest.mark.requests
def test_requests_adapter_raises_generic_error(requests_adapter: RequestsAdapter):
    """
    G: Dado que a aplicação necessita utilizar o adapter de requests para uma requisição HTTP
    W: Quando esta requisição retornar um erro genérico próprio do requests
    T: Então uma exceção requests.RequestException precisa ser lançada
    """

    with patch("requests.sessions.Session.get", side_effect=requests.RequestException):
        with pytest.raises(requests.RequestException):
            _ = requests_adapter.get()


@pytest.mark.adapter
@pytest.mark.requests
@pytest.mark.skip(reason="Avaliando a melhor forma de testar exceções do tipo requests.HTTPError")
def test_requests_adapter_raises_http_error(requests_adapter: RequestsAdapter):
    """
    G: Dado que a aplicação necessita utilizar o adapter de requests para uma requisição HTTP
    W: Quando esta requisição retornar um erro de HTTP
    T: Então uma exceção requests.HTTPError precisa ser lançada
    """

    with requests_mock.Mocker() as requests_mocker:
        # Mockando requisição com erro 500
        requests_mocker.get(
            url=MOCKED_REQUESTS_URL,
            status_code=500,
            reason="Internal Server Error"
        )

        with pytest.raises(requests.HTTPError):
            _ = requests_adapter.get()

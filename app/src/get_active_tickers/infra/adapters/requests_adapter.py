import requests
from requests.adapters import HTTPAdapter, Retry

from app.src._cross.utils.logger import get_logger
from app.src.get_active_tickers.domain.interfaces.adapters_interface import IRequestsAdapter


logger = get_logger()


class RequestsAdapter(IRequestsAdapter):
    def __init__(
        self,
        url: str,
        timeout: int,
        headers: dict[str, str],
        num_retries: int,
        backoff_factor: int,
        status_forcelist: list[int],
        session: requests.sessions.Session = requests.Session()
    ):
        self.__url = url
        self.__timeout = timeout
        self.__headers = headers
        self.__num_retries = num_retries
        self.__backoff_factor = backoff_factor
        self.__status_forcelist = status_forcelist
        self.__session = session

        # Configurando sessão da requisição
        self.__configure_request_session()


    def __configure_request_session(self) -> None:
        retry_config = Retry(
            total=self.__num_retries,
            backoff_factor=self.__backoff_factor,
            status_forcelist=self.__status_forcelist
        )

        http_adapter = HTTPAdapter(max_retries=retry_config)
        self.__session.mount("https://", http_adapter)
        self.__session.mount("http://", http_adapter)


    def get(self) -> requests.models.Response:
        try:
            response = self.__session.get(
                url=self.__url,
                headers=self.__headers,
                timeout=self.__timeout
            )

            return response

        except requests.Timeout as to_error:
            logger.error(f"Erro de timeout ao acessar a url {self.__url}")
            raise to_error

        except requests.ConnectionError as conn_error:
            logger.error(f"Erro de conexão ao acessar a url {self.__url}")
            raise conn_error

        except requests.HTTPError as http_error:
            logger.error(f"Erro de HTTP ao acessar a url {self.__url} "
                         f"com status code {http_error.response.status_code}")
            raise http_error

        except requests.RequestException as req_error:
            logger.error(f"Erro inesperado ao acessar a url {self.__url}")
            raise req_error


    def get_url(self) -> str:
        return self.__url

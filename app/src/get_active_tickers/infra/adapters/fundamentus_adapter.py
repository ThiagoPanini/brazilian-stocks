from typing import Any

import requests
from requests.adapters import HTTPAdapter, Retry

from bs4 import BeautifulSoup

from app.src.get_active_tickers.domain.entities.ticker import Ticker
from app.src.get_active_tickers.domain.interfaces.adapters_interface import ITickersInfoAdapter
from app.src._cross.utils.logger import get_logger


logger = get_logger()

# Parâmetros de configuração do requests para extração de dados do portal Fundamentus
REQUEST_CONFIG_PARAMS = {
    "url": "https://www.fundamentus.com.br/resultado.php",
    "timeout": 10,
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    "num_retries": 3,
    "backoff_factor": 1,
    "status_forcelist": [500, 502, 503, 504]
}


class FundamentusGetTickersAdapter(ITickersInfoAdapter):
    def __init__(
        self,
        session: requests.sessions.Session = requests.Session(),
        request_config_params: dict[str, Any] = REQUEST_CONFIG_PARAMS,
        html_parser: str = "lxml"
    ) -> None:
        self.session = session
        self.request_config_params = request_config_params
        self.html_parser = html_parser


    def __configure_request_session(self) -> None:
        retry_config = Retry(
            total=self.request_config_params["num_retries"],
            backoff_factor=self.request_config_params["backoff_factor"],
            status_forcelist=self.request_config_params["status_forcelist"]
        )

        http_adapter = HTTPAdapter(max_retries=retry_config)
        self.session.mount("https://", http_adapter)
        self.session.mount("http://", http_adapter)


    def __get_request_content(self) -> str:
        try:
            response = self.session.get(
                url=self.request_config_params["url"],
                headers=self.request_config_params["headers"],
                timeout=self.request_config_params["timeout"]
            )
            response.raise_for_status()
            return response.text

        except requests.Timeout as to_error:
            logger.error(f"Erro de timeout ao acessar a url {self.request_config_params["url"]}")
            raise to_error

        except requests.ConnectionError as conn_error:
            logger.error(f"Erro de conexão ao acessar a url {self.request_config_params["url"]}")
            raise conn_error

        except requests.HTTPError as http_error:
            logger.error(f"Erro de HTTP ao acessar a url {self.request_config_params["url"]} "
                         f"com status code {http_error.response.status_code}")
            raise http_error

        except requests.RequestException as req_error:
            logger.error(f"Erro inesperado ao acessar a url {self.request_config_params["url"]}")
            raise req_error


    def __parse_html_content(self, html_text: str) -> BeautifulSoup:
        if not isinstance(html_text, str):
            raise TypeError("O conteúdo HTML (html_text) deve ser uma string válida")

        return BeautifulSoup(html_text, self.html_parser)


    def __find_tickers_info(self, html_parsed: BeautifulSoup) -> list[dict[str, str]]:
        # Retornando tabela do HTML contendo células que possuem informações de ativos
        tickers_cells = list({
            row.find("td") for row in html_parsed.find_all("tr") if row.find("td") is not None
        })

        # Extraindo e consolidando informações em um dicionário
        tickers_info = sorted([
            {
                "codigo_papel": cell.find("a").text.upper().strip(),
                "nome_companhia": cell.find("span").get("title").upper().strip()
            }
            for cell in tickers_cells
        ], key=lambda x: x["codigo_papel"])

        return tickers_info


    def get_tickers(self) -> list[Ticker]:
        self.__configure_request_session()
        html_text = self.__get_request_content()
        html_parsed = self.__parse_html_content(html_text=html_text)
        tickers_info = self.__find_tickers_info(html_parsed=html_parsed)

        # Adaptando resultado como instâncias da entidade esperada
        tickers_objects = [
            Ticker(
                code=info["codigo_papel"],
                company_name=info["nome_companhia"],
                source_info="fundamentus"
            )
            for info in tickers_info
        ]

        return tickers_objects

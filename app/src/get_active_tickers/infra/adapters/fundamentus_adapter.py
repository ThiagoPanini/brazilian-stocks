from bs4 import BeautifulSoup

from app.src.get_active_tickers.domain.entities.ticker import Ticker
from app.src.get_active_tickers.domain.interfaces.adapters_interface import ITickersInfoAdapter
from app.src.get_active_tickers.infra.adapters.requests_adapter import RequestsAdapter


# Definindo URL como uma variável apartada para facilitar reuso em mocks
FUNDAMENTUS_URL = "https://www.fundamentus.com.br/resultado.php"

# Definindo adapter para requisições HTTP/HTTPs via requests
REQUESTS_ADAPTER = RequestsAdapter(
    url=FUNDAMENTUS_URL,
    timeout=10,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    num_retries=3,
    backoff_factor=3,
    status_forcelist=[500, 502, 503, 504]
)


class FundamentusGetTickersAdapter(ITickersInfoAdapter):
    def __init__(
        self,
        requests_adapter: RequestsAdapter = REQUESTS_ADAPTER,
        html_parser: str = "lxml"
    ) -> None:
        self.__requests_adapter = requests_adapter
        self.__html_parser = html_parser


    def __get_request_content(self) -> str:
        return self.__requests_adapter.get().text


    def __parse_html_content(self, html_text: str) -> BeautifulSoup:
        if not isinstance(html_text, str):
            raise TypeError("O conteúdo HTML (html_text) deve ser uma string válida")

        return BeautifulSoup(html_text, self.__html_parser)


    def __find_tickers_info(self, html_parsed: BeautifulSoup) -> list[dict[str, str]]:
        # Retornando tabela do HTML contendo células que possuem informações de ativos
        tickers_cells = list({
            row.find("td") for row in html_parsed.find_all("tr") if row.find("td") is not None
        })

        # Extraindo e consolidando informações em uma lista ordenada de dicionários
        tickers_info = sorted([
            {
                "codigo_papel": cell.find("a").text.upper().strip(),
                "nome_companhia": cell.find("span").get("title").upper().strip()
            }
            for cell in tickers_cells
        ], key=lambda x: x["codigo_papel"])

        return tickers_info


    def get_tickers(self) -> list[Ticker]:
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

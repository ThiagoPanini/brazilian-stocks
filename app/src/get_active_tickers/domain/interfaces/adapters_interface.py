from abc import ABC, abstractmethod
import requests
from app.src.get_active_tickers.domain.entities.ticker import Ticker


class IRequestsAdapter(ABC):
    """
    Interface de contrato para requisições HTTP/HTTPs via requests
    """
    @abstractmethod
    def get(self) -> requests.models.Response:
        raise NotImplementedError


class ITickersInfoAdapter(ABC):
    """
    Interface de contrato para coleta de informações de tickers da B3
    """
    @abstractmethod
    def get_tickers(self) -> list[Ticker]:
        raise NotImplementedError

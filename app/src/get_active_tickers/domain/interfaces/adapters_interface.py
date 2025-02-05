from abc import ABC, abstractmethod
from app.src.get_active_tickers.domain.entities.ticker import Ticker


class IHttpAdapter(ABC):
    """
    Interface de contrato para requisições HTTP/HTTPs via requests
    """
    @abstractmethod
    def get(self):
        pass


class ITickersInfoAdapter(ABC):
    """
    Interface de contrato para coleta de informações de tickers da B3
    """
    @abstractmethod
    def get_tickers(self) -> list[Ticker]:
        pass

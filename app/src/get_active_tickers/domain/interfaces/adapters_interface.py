from abc import ABCMeta, abstractmethod
from app.src.get_active_tickers.domain.entities.ticker import Ticker

class ITickersInfoAdapter(metaclass=ABCMeta):
    """
    Interface de contrato para coleta de informações de tickers da B3
    """

    @abstractmethod
    def get_tickers(self) -> list[Ticker]:
        raise NotImplementedError

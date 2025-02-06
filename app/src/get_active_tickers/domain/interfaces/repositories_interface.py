from abc import ABC, abstractmethod

from app.src.get_active_tickers.domain.entities.ticker import Ticker


class ITickersInfoRepository(ABC):
    """Interface de contrato para armazenamento de informações de tickers da B3"""

    @abstractmethod
    def persist(self, ticker: Ticker) -> None:
        pass

from app.src.get_active_tickers.domain.interfaces.repositories_interface import (
    ITickersInfoRepository
)

from app.src.get_active_tickers.infra.adapters.fundamentus_adapter import (
    ITickersInfoAdapter
)


class SaveTickersInfoUseCase:
    def __init__(self, adapter = ITickersInfoAdapter, repository = ITickersInfoRepository):
        self.__adapter = adapter
        self.__repository = repository

    def execute(self):
        tickers = self.__adapter.get_tickers()
        for ticker in tickers:
            self.__repository.persist(ticker=ticker)

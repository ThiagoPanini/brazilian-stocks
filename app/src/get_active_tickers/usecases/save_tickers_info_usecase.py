from typing import Literal
from app.src._cross.utils.logger import get_logger

from app.src.get_active_tickers.domain.interfaces.repositories_interface import (
    ITickersInfoRepository
)

from app.src.get_active_tickers.infra.adapters.fundamentus_adapter import (
    ITickersInfoAdapter
)


# Instanciando objeto de logger
logger = get_logger()


class SaveTickersInfoUseCase:
    def __init__(
        self,
        adapter = ITickersInfoAdapter,
        repository = ITickersInfoRepository,
        log_pace: Literal[50, 100] = 50
    ):
        self.__adapter = adapter
        self.__repository = repository
        self.log_pace = log_pace

    def __log_execution_status(self, loop_idx: int, num_elements: int) -> None:
        if loop_idx > 0 and loop_idx % self.log_pace == 0:
            num_elements_left = num_elements - loop_idx
            pct_elements_left = round(100 * num_elements_left / num_elements, 2)
            logger.info(f"Foram inseridos {loop_idx} tickers no repositório. "
                        f"Restam {num_elements_left} tickers ({pct_elements_left}% concluído)")

    def execute(self):
        tickers = self.__adapter.get_tickers()
        logger.info(f"Foram obtidos {len(tickers)} tickers de ações da B3")

        for ticker in tickers:
            self.__repository.persist(ticker=ticker)
            self.__log_execution_status(loop_idx=tickers.index(ticker), num_elements=len(tickers))

        logger.info(f"Processo de extração e escrita de informações finalizado com sucesso "
                    f"para todos os {len(tickers)} tickers da B3")

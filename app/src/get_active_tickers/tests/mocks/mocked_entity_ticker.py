from app.src.get_active_tickers.domain.entities.ticker import Ticker


# Definindo objeto Ticker mockado para ser utilizado em fixtures e testes unitários
MOCKED_TICKER = Ticker(
    code="MOCKED_CODE",
    company_name="MOCKED_COMPANY_NAME",
    source_info="MOCKED_SOURCE_INFO"
)

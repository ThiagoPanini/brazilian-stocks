import pytest

from app.src.get_active_tickers.domain.entities.ticker import Ticker

from app.src.get_active_tickers.tests.mocks.mocked_fundamentus_adapter import (
    MOCKED_FUNDAMENTUS_GET_TICKERS_EXPECTED_RETURN
)


@pytest.mark.adapter
@pytest.mark.fundamentus
def test_get_tickers_fundamentus_retorna_objeto_esperado(
    fundamentus_get_tickers_response: list[Ticker],
    expected_output: list[Ticker] = MOCKED_FUNDAMENTUS_GET_TICKERS_EXPECTED_RETURN
):
    """
    G: Dado que o usuário precisa extrair informações de tickers listados na B3
    W: Quando o método get_tickers do adapter fundamentus for executado com um input mockado
    T: Então o retorno precisa ser uma lista de Tickers conforme esperado dado o input mockado
    """

    assert fundamentus_get_tickers_response[0].code == expected_output[0].code
    assert fundamentus_get_tickers_response[0].company_name == expected_output[0].company_name
    assert fundamentus_get_tickers_response[0].source_info == expected_output[0].source_info
    assert fundamentus_get_tickers_response[0].dt_extracted == expected_output[0].dt_extracted


@pytest.mark.adapter
@pytest.mark.fundamentus
@pytest.mark.skip(reason="Testes redundantes para fins didáticos")
def test_get_tickers_fundamentus_retorna_lista(
    fundamentus_get_tickers_response
):
    """
    G: Dado que o usuário precisa extrair informações de tickers listados na B3
    W: Quando o método get_tickers do adapter fundamentus for executado
    T: Então o objeto de retorno deve ser uma lista
    """

    assert isinstance(fundamentus_get_tickers_response, list)


@pytest.mark.adapter
@pytest.mark.fundamentus
@pytest.mark.skip(reason="Testes redundantes para fins didáticos")
def test_get_tickers_fundamentus_retorna_lista_com_elementos(
    fundamentus_get_tickers_response
):
    """
    G: Dado que o usuário precisa extrair informações de tickers listados na B3
    W: Quando o método get_tickers do adapter fundamentus for executado
    T: Então a lista resultante não pode estar vazia
    """

    assert len(fundamentus_get_tickers_response) > 0


@pytest.mark.adapter
@pytest.mark.fundamentus
@pytest.mark.skip(reason="Testes redundantes para fins didáticos")
def test_get_tickers_fundamentus_retorna_lista_com_elementos_da_entidade_esperada(
    fundamentus_get_tickers_response
):
    """
    G: Dado que o usuário precisa extrair informações de tickers listados na B3
    W: Quando o método get_tickers do adapter fundamentus for executado
    T: Então os elementos da lista precisam representar a entidade mapeada para o retorno
    """

    assert isinstance(fundamentus_get_tickers_response[0], Ticker)

import pytest
from moto import mock_aws

from app.src.get_active_tickers.tests.mocks.mocked_dynamodb_repository import (
    MOCKED_DYNAMODB_TABLE_NAME,
)

from app.src.get_active_tickers.tests.mocks.mocked_entity_ticker import (
    MOCKED_TICKER
)


@pytest.mark.repository
@pytest.mark.dynamodb
@mock_aws
def test_dynamodb_repository_envia_itens_para_tabela(
    mocked_dynamodb_client,
    mocked_dynamodb_repository_setup
):
    """
    G: Dado que a aplicação utilizará o repositório DynamoDB para salvar dados de tickers
    W: Quando o método persist() do repositório for executado com um ticker mockado
    T: Então a tabela alvo da persistência precisa possuir um item condizente com o ticker mockado
    """

    # Criando tabela e persistindo item em instância mockada do DynamoDB
    mocked_dynamodb_repository_setup()

    # Validando se a tabela condiz com o esperado
    r = mocked_dynamodb_client.get_item(
        TableName=MOCKED_DYNAMODB_TABLE_NAME,
        Key={
            "code": {"S": MOCKED_TICKER.code},
            "dt_extracted": {"S": MOCKED_TICKER.dt_extracted}
        }
    )

    assert r["Item"]["code"]["S"] == MOCKED_TICKER.code
    assert r["Item"]["dt_extracted"]["S"] == MOCKED_TICKER.dt_extracted

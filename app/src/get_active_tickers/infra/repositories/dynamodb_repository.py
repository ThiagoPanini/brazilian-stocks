import boto3

from app.src.get_active_tickers.domain.entities.ticker import Ticker
from app.src.get_active_tickers.domain.interfaces.repositories_inteface import (
    ITickersInfoRepository
)


class DynamodbTickersInfoRepository(ITickersInfoRepository):

    def __init__(self, table_name: str, region_name: str = "sa-east-1"):
        self.__table_name: str = table_name
        self.__region_name: str = region_name
        self.__boto3_resource = boto3.resource("dynamodb", region_name=self.__region_name)
        self.__dynamodb_table = self.__boto3_resource.Table(self.__table_name)


    def persist(self, ticker: Ticker) -> None:
        self.__dynamodb_table.put_item(ticker.model_dump())

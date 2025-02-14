/* --------------------------------------------------------
ARQUIVO: dynamodb.tf @ get-active-tickers module

Criação de um DynamoDB previamente configurado como um
recurso de armazenamento de itens obtidos através de
interface para coleta de informações de ativos financeiros
listados na B3.
-------------------------------------------------------- */

resource "aws_dynamodb_table" "tickers_info" {
  name         = var.dynamodb_tickers_info_table_name
  billing_mode = var.dynamodb_tickers_info_table_billing_mode
  hash_key     = var.dynamodb_tickers_info_table_hash_key
  range_key    = var.dynamodb_tickers_info_table_range_key

  attribute {
    name = var.dynamodb_tickers_info_table_hash_key
    type = "S"
  }

  attribute {
    name = var.dynamodb_tickers_info_table_range_key
    type = "S"
  }
}

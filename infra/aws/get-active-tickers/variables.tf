/* --------------------------------------------------------
ARQUIVO: variables.tf @ get-active-tickers module

Arquivo de variáveis aceitas pelo módulo get-active-tickers
do projeto Terraform.
-------------------------------------------------------- */

variable "dynamodb_tickers_info_table_name" {
  description = "Nome da tabela a ser criada no DynamoDB para armazenar informações básicas de tickers listados na B3"
  type        = string
  default     = "tbl_b3_tickers_info"
}

variable "dynamodb_tickers_info_table_billing_mode" {
  description = "Tipo de cobrança associada ao consumo dos itens da tabela criada"
  type        = string
  default     = "PAY_PER_REQUEST"

  validation {
    condition     = var.dynamodb_tickers_info_table_billing_mode == "PROVISIONED" || var.dynamodb_tickers_info_table_billing_mode == "PAY_PER_REQUEST"
    error_message = "O valor da variável deve ser 'PROVISIONED' ou 'PAY_PER_REQUEST'."
  }
}

variable "dynamodb_tickers_info_table_hash_key" {
  description = "Nome da variável associada como Hash Key da tabela"
  type        = string
  default     = "code"
}

variable "dynamodb_tickers_info_table_range_key" {
  description = "Nome da variável associada como Range Key da tabela"
  type        = string
  default     = "dt_extracted"
}

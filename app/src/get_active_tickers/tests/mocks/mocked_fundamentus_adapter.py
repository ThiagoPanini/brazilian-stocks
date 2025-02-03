"""
Script responsável por disponibilizar objetos mockados de funcionalidades do projeto.

Na grande maioria dos casos, métodos de classes adapters ou repositories são utilizados para obter
objetos do mundo externo (no caso de adapter) ou de sistemas (no caso de repositories).
Eventualmente, tais objetos precisam ser validados através de testes unitários ou de integração
que, de alguma forma, verificam se os métodos citados se comportam como o esperado.

Dito isso, o objetivo deste script é facilitar a consolidação de objetos de retorno dos métodos
dentro da hierarquia de pastas deste projeto. Os objetos são representados por mocks armazenados
em variáveis que podem ser importadas e utilizadas nos scripts de testes do projeto, seja em
fixtures ou em testes unitários ou de integração.
"""

from app.src.get_active_tickers.domain.entities.ticker import Ticker


# Conteúdo HTML a ser mockado no requests como retorno do método
# __FundamentusGetTickersAdapter.__get_request_content()
MOCKED_FUNDAMENTUS_GET_TICKERS_REQUESTS_RESPONSE = """
    <tr>
    <th class="fd-column-0 sortable-text reverseSort" style="-moz-user-select: none;"><a href="#">Papel</a></th>
    <th class="sortable-numeric fd-column-1" style="-moz-user-select: none;"><a href="#">Cotação</a></th>
    </tr>
    </thead>
    <tbody>
    <tr class="">
    <td ckass="res_papel"><span class="tips" title="ITAÚSA"><a href="detalhes.php?papel=ITSA4">ITSA4</a></span></td>
    <td>8,73</td>
    <td>6,38</td>
    </tr>
    <tr class="par">
    <td ckass="res_papel"><span class="tips" title="ITAUUNIBANCO"><a href="detalhes.php?papel=ITUB4">ITUB4</a></span></td>
    <td>27,30</td>
    <td>8,47</td>
    </tr>
"""

# Retorno esperado do método FundamentusGetTickersAdapter.get_tickers()
MOCKED_FUNDAMENTUS_GET_TICKERS_EXPECTED_RETURN = [
    Ticker(
        code="ITSA4",
        company_name="ITAÚSA",
        source_info="fundamentus"
    ),
    Ticker(
        code="ITUB4",
        company_name="ITAUUNIBANCO",
        source_info="fundamentus"
    )
]

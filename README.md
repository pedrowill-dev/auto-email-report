# Automação de geração de relatorio e envio de email

## Requisitos

* Python 3.9+
* Bibliotecas:
	+ `openpyxl` para ler o arquivo de pedidos em formato Excel
	+ `pandas` para manipular os dados
	+ `loguru` para logging
	+ `python-dotenv` para ler variáveis de ambiente

* Um arquivo de pedidos em formato Excel com as colunas:
	+ `ID da Coluna`
	+ `Data do Pedido`
	+ `Cliente`
	+ `Valor Total`
	+ `ID do Pedido`


## Instalação

1. Clone o repositório:
    ```bash
   git clone https://github.dev/pedrowill-dev/teste-redspark-rpa
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd auto-email-report
   ```

3. Crie um ambiente virtual:

   ```bash
   uv init
   ```

4. Ative o ambiente virtual:

   - No Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - No macOS ou Linux:

     ```bash
     source venv/bin/activate
     ```

5. Instale as dependências listadas no arquivo `requirements.txt`:

   ```bash
    uv pip install -r pyproject.toml
   ```

6. Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente necessárias, como exemplo fornecido no arquivo `config.env`.

## Uso

1. Execute o script principal para gerar o relatório de pedidos:

   ```bash
   uv run run.py
   ```

2. O relatório de pedidos será gerado e enviado para os e-mails especificados no arquivo Excel.

## Estrutura do Projeto

- `src/`: contém o código-fonte do projeto.
- `data/`: contém templates de e-mail e arquivos de pedidos.
- `logs/`: armazena logs de execução.


## Licença

Este projeto está licenciado sob a Licença MIT.



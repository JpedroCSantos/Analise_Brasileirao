# 📊 Brasileirão Análise

## 📌 Visão Geral

O **Brasileirão Análise** é um projeto focado na análise estatística dos resultados do Campeonato Brasileiro. Com a crescente discussão sobre o impacto dos placares **0x0** no futebol, como mencionado recentemente por **Gerard Piqué**, este projeto busca fornecer insights baseados em dados para entender melhor os padrões das partidas, desempenho dos times e a influência dos diferentes formatos de pontuação.

Nos últimos anos, a quantidade de empates sem gols gerou questionamentos sobre a atratividade do jogo e possíveis mudanças no regulamento para incentivar partidas mais ofensivas. Utilizando **dados históricos do Brasileirão**, este projeto analisa estatísticas como:
- **Quantidade de empates por temporada**
- **Impacto das regras de pontuação na competitividade**

O sistema permite a **consulta de estatísticas via API**, a **importação de dados de temporadas anteriores** e a **visualização gráfica** das tendências no campeonato. Através da análise dos dados, é possível identificar padrões e sugerir alternativas para tornar o futebol mais dinâmico e emocionante.

O projeto foi desenvolvido utilizando **Python**, **Pandas**, **FastParquet**, **Matplotlib**, e outras bibliotecas para manipulação e visualização dos dados.


---

## 🚀 Funcionalidades Principais
- **Consulta de dados via API:** Coleta dados históricos do Campeonato Brasileiro utilizando a **API Sports Football**.
- **Leitura de arquivos locais:** Suporte à importação de dados de temporadas salvos localmente.
- **Processamento e agregação de dados:** Consolidação de estatísticas de times ao longo das temporadas.
- **Geração de visualizações:** Criação de gráficos e análises a partir dos dados processados.
- **Salvamento de resultados:** Exportação dos dados processados em formatos como Parquet e CSV.

---

## 📂 Estrutura do Projeto
```plaintext
├── app/                           # Aplicação principal
│   ├── api/                        # Módulo de interação com API externa
│   │   ├── classes/                # Classes auxiliares para consultas
│   │   ├── schema/                 # Schemas de requisição e resposta da API
│   │   ├── __init__.py
│   │   ├── consult.py               # Consulta e integração com API de futebol
│   ├── pipeline/                    # Processamento de dados
│   │   ├── classes/                 # Classes de processamento
│   │   ├── schemas/                 # Schemas de transformação
│   │   ├── __init__.py
│   │   ├── extract.py               # Extração de dados
│   │   ├── load.py                  # Salvamento de dados processados
│   │   ├── table.py                 # Estruturação de tabelas de estatísticas
│   │   ├── transform.py             # Transformação e agregação de dados
│   ├── visualization/                # Módulo de visualização de dados
│   │   ├── __init__.py
│   │   ├── graphs.py                # Funções de geração de gráficos
│   ├── main.py                       # Script principal do projeto
├── data/                             # Diretório para armazenar os dados processados
│   ├── input/                        # Dados brutos coletados
│   ├── output/                       # Dados processados
├── env/                              # Configuração de ambiente e variáveis
├── images/                           # Diretório para armazenar imagens usadas no projeto
├── .gitignore                        # Arquivo de exclusão do Git
├── .python-version                   # Versão do Python utilizada no projeto
├── poetry.lock                        # Arquivo de gerenciamento de dependências do Poetry
├── pyproject.toml                     # Configuração do projeto Python e dependências
├── README.md                          # Documentação do projeto
├── response.json                      # Arquivo JSON com respostas da API
```

## 📦 Instalação e Configuração

### 🛠️ 1. Requisitos
Antes de executar o projeto, certifique-se de ter:

- **🐍 Python** `>=3.13`
- **📦 Poetry** para gerenciar dependências.

### 📥 2. Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/JpedroCSantos/Analise_Brasileirao.git
    ```

2. Instale as dependências com Poetry:
    ```bash
    poetry install
    ```

3. Configure as variáveis de ambiente:
    - Crie um arquivo .env na pasta env/ e adicione a chave da API:
    ```bash
    api_football_key=SEU_TOKEN_AQUI
    ```

### ▶️ 3. Executando o Projeto

Para rodar a análise do Brasileirão, execute:
```bash
    poetry run python app/main.py
```
Isso irá: 
- ✅ Consultar dados via API ou arquivos locais.
- ✅ Processar e consolidar estatísticas.
- ✅ Gerar arquivos .parquet com os dados analisados.
- ✅ Criar gráficos para visualização dos resultados.

## 📚 Dependências Principais

O projeto utiliza as seguintes bibliotecas:

| 📦 Biblioteca    | 🔧 Função                                       |
|-----------------|-----------------------------------------------|
| `pandas`        | Manipulação e análise de dados               |
| `requests`      | Requisições HTTP para APIs                   |
| `dotenv`        | Gerenciamento de variáveis de ambiente       |
| `fastparquet`   | Leitura e escrita de arquivos `.parquet`     |
| `matplotlib`    | Geração de gráficos                          |
| `pillow`        | Manipulação de imagens                      |

### 📌 Como instalar as dependências?
Todas as dependências são gerenciadas automaticamente pelo **Poetry**. Para instalá-las, basta rodar o comando:

```bash
poetry install
```
Caso precise adicionar novas dependências ao projeto, utilize:
```bash
poetry add nome-da-biblioteca
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você deseja ajudar a melhorar este projeto, siga estas etapas:

1. Faça um **fork** do repositório.
2. Crie uma **branch** para sua nova funcionalidade:
   ```bash
   git checkout -b feature/nova-funcionalidade
3. Faça suas alterações e commite:
    ```bash
    git commit -m "Adicionando nova funcionalidade"
    ```
4. Envie suas alterações para o seu repositório remoto:
    ```bash
    git push origin feature/nova-funcionalidade
    ```
5. Abra um Pull Request (PR) no repositório original 🚀.

## 🏆 Autor

Este projeto foi desenvolvido por:

**👤 João Pedro Santos**  
📩 **E-mail:** [jpedro.csantos@hotmail.com](mailto:jpedro.csantos@hotmail.com)  
🔗 **LinkedIn:** [linkedin.com/in/jpedro-santos](https://www.linkedin.com/in/jpedro-santos/)  

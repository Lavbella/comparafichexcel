# Advanced File Cross-Referencing & Audit Tools (Data Matching)

[Português](#português) | [English](#english)

---

##  Licença / License
This project is licensed under the **GNU GPLv3**. See the [LICENSE](LICENSE) file for details.

---

## Português

Esta é uma aplicação web interativa desenvolvida em Python com **Streamlit**, concebida como uma ferramenta avançada de auditoria e cruzamento de dados (*Data Matching*) para grandes volumes de informação. A plataforma permite carregar dois ficheiros Excel distintos, selecionar dinamicamente a coluna mestre de cada um através de menus suspensos interativos (ex: NIF, IDs Corporativos, E-mails) e realizar análises relacionais e de conciliação.

###  Funcionalidades e Engenharia Central

#### UI/UX & Layout de Estado Inicial
Para proporcionar uma interface limpa e intuitiva, o painel inclui um **Modo de Estado Inicial** que renderiza um *wireframe* estruturado com 3 colunas simétricas (Registos Carregados, Chaves de Correspondência e Estado da Auditoria) juntamente com uma mensagem informativa "Awaiting Execution...". A interface faz a transição para as tabelas analíticas no milissegundo em que os ficheiros são processados.

#### Motores de Cruzamento de Dados (Pandas Pipeline)
A aplicação utiliza o poder do **pandas** para segmentar e auditar os dados em quatro perspetivas claras:
*   **Registos Comuns (Nos 2 Excel):** Identifica e isola apenas as linhas que existem em ambos os ficheiros com base nas chaves selecionadas.
*   **Apenas no Ficheiro A:** Extrai e exibe os registos que são exclusivos do primeiro ficheiro carregado, revelando o que falta no Ficheiro B.
*   **Apenas no Ficheiro B:** Extrai e exibe os registos que são exclusivos do segundo ficheiro carregado, revelando o que falta no Ficheiro A.
*   **Vista Consolidada (Mostrar Tudo com Indicações):** Combina a totalidade dos dados de ambos os ficheiros, anexando uma coluna indicadora que assinala claramente a origem de cada registo (se existe apenas no Ficheiro A, apenas no Ficheiro B ou em ambos).

###  Pré-requisitos (Ubuntu)
Antes de começar, certifique-se de que tem as dependências essenciais do sistema instaladas:
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-tk git -y
```

###  1. Configurar o Ambiente Virtual (venv)
Execute estes comandos no terminal para clonar o repositório e preparar o ambiente:

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Atualizar o gerenciador de pacotes e instalar os requisitos (incluindo pandas, openpyxl e streamlit)
pip install --upgrade pip
pip install -r requirements.txt
```

###  2. Executar a Aplicação em Desenvolvimento
Com o ambiente virtual (`venv`) ativo, inicie a aplicação:

**Via Streamlit direto:**
```bash
streamlit run app.py
```

**Via Script Wrapper (utilizado pelo executável):**
```bash
python run_app.py
```
A interface abrirá automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

###  3. Como Gerar o Executável (Ubuntu)
Para compilar esta aplicação Streamlit num único ficheiro binário executável utilizando o PyInstaller, execute:

```bash
# Limpar caches de compilações anteriores
rm -rf build dist

# Compilar utilizando as configurações do ficheiro .spec
pyinstaller --clean app.spec
```
O binário final será gerado dentro da pasta **`dist/`**. Para o iniciar diretamente pelo terminal, utilize:
```bash
./dist/app
```

---

## English

This is an interactive web application built with **Streamlit** in Python, engineered as an advanced data-matching and audit platform for high-volume datasets. The tool allows users to upload two separate Excel files, dynamically define a master matching key for each via intuitive dropdown menus (e.g., NIF, Corporate IDs, Emails), and perform deep relational auditing.

###  Features & Core Components

#### UI/UX & Initial State Layout
To deliver a clean and structured user experience, the dashboard features an **Initial State Mode** rendering 3 symmetrical columns (Loaded Rows, Matching Keys, and Audit Status) alongside an info status card stating "Awaiting Execution...". It transitions seamlessly into interactive data frames the moment the matching pipeline finishes execution.

#### Data Matching Engines (Pandas Core)
The processing engine leverages **pandas** to split and cross-reference records into four comprehensive audit views:
*   **Common Records (In both Excel files):** Isolates rows that share matching master keys across both uploaded datasets.
*   **Only in File A:** Extracts and displays records that exist exclusively in the first file, revealing what is missing from File B.
*   **Only in File B:** Extracts and displays records that exist exclusively in the second file, revealing what is missing from File A.
*   **Consolidated View (Show All with Indicators):** Combines the complete datasets from both files, appending a dedicated tracking column that explicitly flags the origin of each record (whether it exists only in File A, only in File B, or across both).

###  Prerequisites (Ubuntu)
Before starting, ensure you have the essential system dependencies installed:
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-tk git -y
```

###  1. Setting Up the Virtual Environment (venv)
Run these commands in your terminal to set up the isolated project environment:

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install requirements (including pandas, openpyxl, and streamlit)
pip install --upgrade pip
pip install -r requirements.txt
```

###  2. Running the Application in Development
With the virtual environment (`venv`) active, launch the dashboard:

**Via direct Streamlit command:**
```bash
streamlit run app.py
```

**Via Wrapper Script (used by the executable):**
```bash
python run_app.py
```
The application will automatically open in your default browser (usually at `http://localhost:8501`).

###  3. How to Generate the Executable (Ubuntu)
To compile the Streamlit application into a single standalone Linux binary using PyInstaller, run:

```bash
# Clear previous build caches
rm -rf build dist

# Compile using the configuration from the .spec file
pyinstaller --clean app.spec
```
The final standalone binary will be generated inside the **`dist/`** folder. To run it, use:
```bash
./dist/app
```

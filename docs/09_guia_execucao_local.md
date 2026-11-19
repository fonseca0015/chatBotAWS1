# Guia Passo a Passo: Como Rodar o Projeto Localmente

Este manual fornece instruções completas e testadas para configurar e executar o **ERP Helpper** em seu ambiente local (Windows, Linux ou macOS).

---

## 1. Pré-Requisitos do Sistema

Antes de iniciar, certifique-se de ter instalado:
- **Python 3.10** ou superior ([python.org](https://www.python.org/downloads/)).
- **Git** instalado e configurado no terminal.
- Uma chave válida de API da **OpenAI** (com saldo/créditos ativos).

---

## 2. Passo a Passo de Instalação e Execução

### Passo 1: Clonar o Repositório
Abra o seu terminal (PowerShell, Prompt de Comando ou Bash) e clone o projeto:
```bash
git clone https://github.com/fonseca0015/chatBotAWS1.git
cd chatBotAWS1
```

---

### Passo 2: Criar e Ativar o Ambiente Virtual (`venv`)
É altamente recomendado utilizar um ambiente virtual isolado para evitar conflito de pacotes.

#### No Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
> *Nota: Caso o PowerShell apresente erro de execução de scripts, execute previamente:*
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### No Windows (CMD):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### No Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Passo 3: Instalar as Dependências
Com o ambiente virtual ativado, instale os pacotes necessários:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Passo 4: Configurar as Variáveis de Ambiente (`.env`)
Copie o arquivo de exemplo `.env.example` para criar seu `.env`:

#### No Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

#### No Linux / macOS:
```bash
cp .env.example .env
```

Abra o arquivo `.env` recém-criado em seu editor de preferência e adicione sua chave de API da OpenAI:
```dotenv
OPENAI_API_KEY=sk-proj-sua-chave-completa-aqui
PORT=5000
DB_PATH=base_de_conhecimento_db
COLLECTION_NAME=docs_uno_erp_cosine
```

---

### Passo 5: Inicializar o Servidor Flask e o ChromaDB
Execute o script principal:
```bash
python main.py
```

#### O que esperar na inicialização:
1. O sistema verifica a existência da pasta `base_de_conhecimento_db/`.
2. Se a coleção `docs_uno_erp_cosine` já existir populada, o banco é carregado em segundos.
3. Se a pasta não existir ou estiver vazia, o script lê automaticamente o arquivo `knowledge_base.json`, fatiará os textos em chunks com `tiktoken`, gerará os embeddings via OpenAI e persistirá o banco.
4. O servidor iniciará escutando em `http://0.0.0.0:5000`.

---

## 3. Testando a Search API Localmente

### Teste via cURL (Prompt de Comando ou Bash):
```bash
curl -X POST http://127.0.0.1:5000/search \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Como resolver rejeição 201 no UNO ERP?"}'
```

### Teste via PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/search" `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"pergunta": "Como resolver rejeição 201?"}' | ConvertTo-Json -Depth 4
```

A resposta esperada é um array JSON contendo os artigos recuperados com `categoria`, `titulo`, `texto_completo` e `url`.

---

## 4. Executando a Interface Web (`index.html`)

A interface conversacional web não exige compiladores. Você pode executá-la de duas formas:

### Opção A: Abertura Direta
Dê dois cliques no arquivo `index.html` ou abra-o em qualquer navegador moderno (Chrome, Edge, Firefox).

### Opção B: Servidor HTTP Local (Recomendado)
Para evitar restrições de CORS em alguns navegadores:
```bash
# Em um novo terminal, dentro da pasta do projeto:
python -m http.server 8080
```
Acesse no navegador: **`http://localhost:8080`**.

> **Nota:** O frontend envia as mensagens para o webhook do **n8n** configurado na linha 201 do `index.html`. Caso queira apontar para o seu próprio n8n local ou de homologação, altere a constante `n8nWebhookUrl` no script.

---

## 5. Resolução de Problemas Comuns (*Troubleshooting*)

- **Erro `openai.AuthenticationError`:**
  - Verifique se a variável `OPENAI_API_KEY` está preenchida corretamente no `.env` e se a conta possui créditos ativos na plataforma da OpenAI.
- **Porta 5000 já em uso:**
  - No Windows, encerre processos ocupando a porta com `netstat -ano | findstr :5000` ou altere a porta no final do arquivo `main.py` para `5001`.
- **Erro de importação de módulos:**
  - Confirme se o ambiente virtual (`venv`) está devidamente ativado antes de executar `python main.py`.

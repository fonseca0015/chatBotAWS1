# Guia de Deploy da Aplicação

Este documento descreve as alternativas e o passo a passo para realizar o deploy em produção do ecossistema do **ERP Helpper**, incluindo a Search API (Flask + ChromaDB), a orquestração no n8n e a interface Web.

---

## 1. Links de Deploy e Endpoints da Aplicação

| Componente | Ambiente | URL / Endpoint |
| :--- | :--- | :--- |
| 🌐 **Frontend Web (Chatbot)** | Produção (GitHub Pages) | [https://fonseca0015.github.io/chatBotAWS1/](https://fonseca0015.github.io/chatBotAWS1/) |
| ⚡ **Search API (Flask/ChromaDB)** | Produção (AWS EC2) | `http://44.203.191.31:5000/search` |
| 🔄 **Webhook do n8n (Orquestrador)** | Produção (n8n Cloud) | `https://unoerpai.app.n8n.cloud/webhook/c7683d30-5ffb-448b-a9cb-2dac0ac443bb` |
| 📦 **Workflow n8n Exportado** | Repositório | [`n8n/workflow_uno_erp_helpper.json`](../n8n/workflow_uno_erp_helpper.json) |

---

## 2. Estratégias de Deploy da Search API

Como a Search API utiliza persistência em disco para o banco vetorial (**ChromaDB**), o deploy exige armazenamento persistente com leitura e escrita rápida.

### Opção 1: Deploy com Docker e Docker Compose (Recomendado)
A aplicação já conta com `Dockerfile` e `docker-compose.yml` prontos no repositório.

1. **Subir para a máquina servidora (ex.: AWS EC2 Ubuntu 22.04 LTS):**
   ```bash
   git clone https://github.com/fonseca0015/chatBotAWS1.git
   cd chatBotAWS1
   ```
2. **Criar o `.env` de produção:**
   ```bash
   cp .env.example .env
   nano .env # Insira a sua OPENAI_API_KEY
   ```
3. **Subir os containers em segundo plano:**
   ```bash
   docker compose up -d --build
   ```
4. **Verificar os logs de inicialização:**
   ```bash
   docker compose logs -f erp-helpper-search-api
   ```

---

### Opção 2: Deploy na AWS (EC2 + Nginx + Gunicorn + Certbot SSL)

Para garantir alta disponibilidade e latência mínima sem oscilações de túnel:

1. **Provisionar Instância:**
   - Tipo de Instância: `t3.medium` ou `t3.small` (mínimo de 2 GB de RAM para embeddings e ChromaDB).
   - Sistema Operacional: Ubuntu Server 24.04 / 22.04 LTS.
   - Security Group: Liberar portas 22 (SSH), 80 (HTTP), 443 (HTTPS) e 5000 (Custom TCP caso queira acesso direto da API).

2. **Instalar Dependências no Servidor:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3-pip python3-venv nginx
   ```

3. **Configurar a Aplicação:**
   ```bash
   git clone https://github.com/fonseca0015/chatBotAWS1.git /var/www/erphelpper
   cd /var/www/erphelpper
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt gunicorn
   cp .env.example .env
   # Preencher OPENAI_API_KEY no .env
   ```

4. **Criar o Serviço Systemd (`/etc/systemd/system/erphelpper.service`):**
   ```ini
   [Unit]
   Description=ERP Helpper Search API Flask Service
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/var/www/erphelpper
   EnvironmentFile=/var/www/erphelpper/.env
   ExecStart=/var/www/erphelpper/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 main:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
   Ativar o serviço:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start erphelpper
   sudo systemctl enable erphelpper
   ```

---

### Opção 3: Deploy em PaaS (Render / Railway)
Para ambientes gerenciados com baixo esforço operacional:
1. Conecte o repositório GitHub ao painel do Render ou Railway.
2. Defina o tipo de serviço como **Web Service**.
3. Adicione um **Persistent Disk** montado em `/app/base_de_conhecimento_db` para que a base vetorial não seja perdida entre deploys.
4. Configure a variável de ambiente secreta `OPENAI_API_KEY`.
5. Start Command: `python main.py` ou `gunicorn -w 2 -b 0.0.0.0:$PORT main:app`.

---

## 3. Deploy do Frontend Web (`index.html`)

A interface conversacional é uma SPA estática leve (*Single Page Application*). Ela pode ser hospedada com custo zero e CDN global:

1. **GitHub Pages (Gratuito e Imediato):**
   - Acesse as **Settings** do repositório no GitHub.
   - Navegue até a aba **Pages**.
   - Em *Source*, selecione a branch `main` e a pasta `/ (root)`.
   - Clique em **Save**. Em minutos o site estará ativo na URL: `https://fonseca0015.github.io/chatBotAWS1/`.
2. **Vercel / Netlify / AWS S3 + CloudFront:**
   - Faça upload do arquivo `index.html` ou conecte o repositório para deploy automático com HTTPS padrão.

---

## 4. Túnel de Desenvolvimento (ngrok)

Durante o desenvolvimento ou testes rápidos para expor a máquina local ao n8n Cloud:
```bash
ngrok http 5000
```
Copie a URL `https://xxxx.ngrok-free.app` gerada e configure-a como destino HTTP no nó de consulta do fluxo do n8n.

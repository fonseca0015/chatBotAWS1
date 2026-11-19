# Relatório de Problema, Solução Aplicada e Riscos Previstos

> **Documento de Referência:** Projeto UNO ERP — Interesse da Empresa Parceira  
> **Data de Emissão:** 18 de setembro de 2026 | **Solicitante:** Cesar (Liderança do Projeto)

---

## 1. Objetivo e Contexto
Este relatório formaliza:
1. O diagnóstico da instabilidade ocorrida na busca de resultados do **ERP Helpper** e a respectiva correção técnica aplicada.
2. A análise preventiva dos riscos e custos operacionais atrelados aos serviços externos da solução, com destaque para **ElevenLabs** (canal de voz) e **n8n** (orquestração), além do consumo de tokens da **OpenAI** e a infraestrutura de rede da Search API.

---

## 2. Diagnóstico do Problema e Solução Aplicada

### 2.1. O Problema Identificado
Durante os testes de integração, ao realizar consultas pelo chat ou telefone, o sistema frequentemente não encontrava resultados pertinentes na documentação do UNO ERP e retornava mensagens genéricas de falha.
Essa etapa (RF03 e RF04 - "Consultar Dúvida") é o alicerce da arquitetura RAG: sem a recuperação precisa dos trechos corretos, o modelo gerador passa a responder por alucinação ou recusa o atendimento, degradando a confiabilidade do suporte.

### 2.2. Causas Raízes Identificadas
1. **Esgotamento de Saldo/Tokens da OpenAI:** A ausência de créditos na conta da API impedia o modelo `text-embedding-3-small` de converter a pergunta em vetor e o `gpt-4o-mini` de estruturar a resposta.
2. **Instabilidade no Banco Vetorial (ChromaDB):** O banco vetorial local não estava persistindo ou inicializando as coleções de forma adequada após reinicializações.

### 2.3. Solução Aplicada
- Reestruturação do ciclo de vida da conexão do ChromaDB no arquivo `main.py`, com persistência em disco robusta (`chromadb.PersistentClient`), criação/validação automática da coleção e população transparente a partir de `knowledge_base.json`.
- Adição de rotinas de contingência com fallback automático e recarga de créditos nas chaves da OpenAI. A busca voltou a operar em regime nominal.

---

## 3. Análise de Custos e Riscos: ElevenLabs (Canal de Voz)

### 3.1. Modelo de Cobrança
A API do ElevenLabs opera por consumo de **créditos**:
- No modelo **Multilingual v2**: $1\text{ crédito} = 1\text{ caractere}$ sintetizado.
- Nos modelos **Flash / Turbo**: $0,5\text{ a }1\text{ crédito} = 1\text{ caractere}$.
- Quando o pacote contratado se esgota, a síntese de áudio é bloqueada ou entra em regime de cobrança por excedente (*overage*).

### 3.2. Tabela de Planos de Referência (Base Agosto/2026)

| Plano | Preço Mensal | Créditos Inclusos | Estimativa de Uso | Observação Comercial |
| :--- | :--- | :--- | :--- | :--- |
| **Free** | US$ 0 | 10.000 | ~10 min de áudio | **Não permite uso comercial**. Inviável para produção. |
| **Starter** | US$ 5 – 6 | ~30.000 | ~30 min de fala | Menor plano com direito comercial. |
| **Creator** | US$ 22 | ~121.000 | ~2 horas de fala | Adequado para pilotos e testes com usuários reais. |
| **Pro** | US$ 99 | ~600.000 | ~10 horas (600 min) | Custo de excedente mais barato; ideal para operação inicial. |
| **Scale / Business** | US$ 299 / 990 | 1,8 mi / 6 mi | Alto volume | Sob demanda para produção em grande escala. |

### 3.3. Riscos e Mitigações para Voz
- **Esgotamento Súbito:** O canal telefônico fica mudo ou cai. *Mitigação:* Configurar alertas automáticos por webhook quando o saldo atingir $20\%$ da cota mensal.
- **Custo Flutuante com Respostas Longas:** *Mitigação:* Instruir o prompt da LLM no canal de voz a gerar respostas ultra-objetivas ($\le 300$ caracteres), configurar limite de turnos por ligação e implementar cache de áudio para perguntas frequentes.
- **Perda de Créditos Sobressalentes:** Créditos não consumidos acumulam por até 2 meses nos planos pagos, expirando caso haja downgrade de plano.

---

## 4. Análise de Custos e Riscos: n8n (Orquestrador de Fluxos)

### 4.1. Modelo de Cobrança
No n8n, a cobrança é calculada por **execução** (cada ciclo completo do workflow, do webhook de entrada à resposta ao usuário).
- No ERP Helpper, cada pergunta submetida no chat ou interação de voz consome 1 execução.
- Na nuvem oficial (n8n Cloud), não há plano gratuito permanente (apenas trial de 14 dias).

### 4.2. Comparativo de Planos e Auto-Hospedagem

| Opção | Custo Aproximado | Limite Execuções/mês | Observação Operacional |
| :--- | :--- | :--- | :--- |
| **n8n Cloud — Starter** | US$ 20 – 24 / mês | 2.500 | Insuficiente: 100 perguntas/dia já atingem 3.000 execuções/mês. |
| **n8n Cloud — Pro** | US$ 50 – 60 / mês | 10.000 | Faixa recomendada para volume operacional médio sem sobrecarga de infra. |
| **n8n Cloud — Business** | US$ 667 – 800 / mês | 40.000 | Voltado a empresas com conformidade estrita e governança avançada. |
| **Community Edition (Self-Hosted)** | **Licença Gratuita** + Servidor (~US$ 5 – 10 / mês) | **Sem limite** | **Excelente custo-benefício**: a equipe assume provisionamento, backup e atualizações. |

### 4.3. Riscos e Mitigações para n8n
- **Estouro da Cota Cloud:** Ao atingir o teto de 2.500 execuções no Starter, os fluxos deixam de rodar até a virada do ciclo de faturamento.
- **Recomendação Estratégica:** Adotar o **n8n Community Edition auto-hospedado** em instância Docker compartilhada na nuvem (ex: AWS EC2 com a Search API) para zerar os custos por execução.

---

## 5. Outros Custos e Infraestrutura do Ecossistema

1. **Tokens OpenAI (`text-embedding-3-small` e `gpt-4o-mini`):**
   - Custo por milhão de tokens extremamente acessível no `gpt-4o-mini` e no modelo de embedding.
   - É obrigatório manter recarga com cobrança automática ou saldo mínimo de US$ 10 – 20 para evitar paradas do RAG.
2. **Substituição do Túnel ngrok por Hospedagem Estável:**
   - Durante a fase inicial de desenvolvimento, utilizou-se o **ngrok** para expor a Search API local ao n8n Cloud.
   - O túnel ngrok não possui SLA de produção e reinicia a URL em caso de queda.
   - **Ação recomendada:** Realizar o deploy definitivo da Search API em servidor em nuvem (ex: AWS EC2 com IP elástico ou Render/Railway) e configurar domínio com certificado SSL.

---

## 6. Matriz de Síntese para a Empresa Parceira

| Ponto de Avaliação | Situação Atual | Ação Recomendada para Produção |
| :--- | :--- | :--- |
| **Busca de Resultados (RAG)** | ✅ **Corrigida e Estável** | Manter monitoramento contínuo de saldo na OpenAI e executar testes automatizados com perguntas-padrão de referência. |
| **ElevenLabs (Voz)** | ⚠️ **Risco de Custo Recorrente** | Contratar plano compatível (Creator ou Pro), estipular limites de duração por chamada e ativar alertas de consumo. |
| **n8n (Orquestração)** | ⚠️ **Risco de Limite de Execuções** | Migrar para **n8n Community Edition auto-hospedado** em Docker ou contratar o plano Pro Cloud conforme o volume. |
| **Infraestrutura e Servidor** | ⚠️ **Dependência de Túnel Dev (ngrok)** | Migrar a API Flask para hospedagem permanente na AWS com Docker e SSL, garantindo disponibilidade 24/7. |

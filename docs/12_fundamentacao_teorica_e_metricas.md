# Fundamentação Teórica, Métricas e Referências Bibliográficas

Este documento sintetiza os embasamentos teóricos, acadêmicos e metodológicos que sustentam a arquitetura e as decisões de engenharia do **ERP Helpper**, em consonância com a monografia do Projeto Integrador apresentada à **FATEC Sorocaba**.

---

## 1. Inteligência Artificial, PLN e o Suporte Técnico N1

O suporte técnico em empresas fornecedoras de ERP é classicamente particionado em níveis de maturidade (N1, N2 e N3). O primeiro nível (N1) absorve uma carga desproporcional de chamados operacionais repetitivos (como parâmetros fiscais, configurações cadastrais e rejeições da SEFAZ), cujas soluções já estão descritas nos manuais corporativos.

- **Impacto da IA Generativa no Suporte:** Conforme demonstrado por Brynjolfsson, Li e Raymond (2023) em pesquisa publicada no *Quarterly Journal of Economics*, o uso de assistentes inteligentes em operações de helpdesk eleva em média **14% a resolução de problemas por hora**, alcançando ganhos de **34% entre atendentes iniciantes**.
- **Superação de Chatbots Rígidos:** Enquanto os primeiros sistemas conversacionais baseavam-se em árvores estáticas de decisão e regras programadas (como o histórico ELIZA de Weizenbaum, 1966), a arquitetura Transformer (Vaswani et al., 2017) e os grandes modelos de linguagem (Brown et al., 2020) viabilizaram uma compreensão contextual flexível da linguagem humana (Jurafsky & Martin, 2025).

---

## 2. Mitigação de Alucinações via Arquitetura RAG

Os Modelos de Linguagem de Grande Escala (LLMs) são naturalmente suscetíveis ao fenômeno de **alucinação**, isto é, geração de afirmações semanticamente convincentes, porém factualmente incorretas ou infundadas (Ji et al., 2023; Kalai et al., 2025). Em um ERP corporativo, uma instrução fiscal inventada por uma IA pode causar sérios prejuízos tributários e operacionais.

Para anular esse risco, o ERP Helpper adota o padrão **RAG (*Retrieval-Augmented Generation*)**, introduzido por Patrick Lewis et al. (2020) e corroborado por Shuster et al. (2021):

```mermaid
flowchart LR
    A["Pergunta do Usuário"] --> B["Geração de Embeddings\n(text-embedding-3-small)"]
    B --> C["Busca por Cosseno\n(ChromaDB HNSW)"]
    C --> D["Contexto Oficial Recuperado\n(Manuais UNO ERP)"]
    D --> E["Síntese Fundamentada\n(OpenAI GPT-4o-mini)"]
    E --> F["Resposta sem Alucinação"]
```

### Por que RAG e não Fine-Tuning?
1. **Atualização Dinâmica (RF06):** Manuais fiscais e versões do UNO ERP mudam com frequência. No RAG, basta reinserir o chunk no ChromaDB sem custos de treinamento de máquina (Lewis et al., 2020).
2. **Auditabilidade das Respostas:** As respostas citam diretamente os links oficiais da Wiki do ERP (`unoerpwiki.herokuapp.com`).
3. **Eficiência de Custos:** Ajuste fino (*Fine-tuning*) exige curadoria intensiva de datasets e custos altos de computação, ao passo que a busca vetorial via ChromaDB opera localmente com latência de milissegundos.

---

## 3. Harness Engineering e Orquestração com n8n

O conceito de **Harness Engineering** foi formalizado por equipes de engenharia de ponta (OpenAI, 2026g) para descrever a estrutura que organiza, parametriza e controla o ciclo de vida dos agentes de IA (instruções de sistema, ferramentas, testes e validação de saídas).

No **ERP Helpper**, a plataforma **n8n** atua exatamente como esse *Harness*:
- Recebe a intenção do usuário via Webhook;
- Consulta a Search API em Flask;
- Agrega metadados e monta o prompt técnico;
- Aplica diretrizes rígidas no *System Message* do agente;
- Higieniza e formata a resposta antes da entrega final ao usuário.

---

## 4. Comunicação por Voz em Meio Digital (Telefonia e ElevenLabs)

A viabilização do canal telefônico (RF02 e RF10) apoia-se em padrões abertos de telecomunicações:
- **Telefonia IP / VoIP:** Uso do protocolo SIP (RFC 3261 - Rosenberg et al., 2002) para digitalização de voz em pacotes IP.
- **Pipeline Encadeada (*Chained Pipeline*):** Em contraste com abordagens puras de *speech-to-speech*, a OpenAI (2026c) recomenda a pipeline encadeada para suporte corporativo com conformidade:
  $$\text{Áudio (Voz)} \xrightarrow{\text{STT / Whisper}} \text{Texto} \xrightarrow{\text{RAG + LLM}} \text{Resposta} \xrightarrow{\text{TTS / ElevenLabs}} \text{Áudio Sintetizado}$$
- **Twilio ConversationRelay:** Padrão via WebSocket que conecta a chamada à infraestrutura de IA, delegando a geração de voz de ultra-realismo ao motor neural do **ElevenLabs**.
- **Ajustes de Usabilidade em Voz:** Respostas estritamente orais ($\le 250$ caracteres), sem sintaxe Markdown, sem listas complexas e sem leitura de links longos, priorizando clareza auditiva imediata.

---

## 5. Métricas de Sucesso e KPIs (ISO 9241-11)

A avaliação contínua do assistente toma como base os três pilares de usabilidade da norma **ISO 9241-11**:

| Pilar ISO | Métrica no ERP Helpper | Indicador e Meta |
| :--- | :--- | :--- |
| **Eficácia** | Taxa de Resolução no N1 | $\ge 70\%$ de dúvidas resolvidas sem necessidade de suporte humano. |
| **Eficiência** | Tempo Médio de Resposta (TMR) | $\le 3,0\text{ s}$ no chat web e $\le 2,5\text{ s}$ na síntese por voz (RNF06). |
| **Satisfação** | CSAT de Atendimento | Avaliação média do usuário $\ge 4,5$ em escala de 1 a 5. |
| **Cobertura** | Taxa de Escalonamento N1 | Percentual de consultas que exigem transferência para equipe humana ($\le 25\%$). |

### Comparativo de Mercado (Benchmarking):
- **Intercom Fin:** Taxa média de resolução autônoma reportada de 76% (Intercom, 2026).
- **TOTVS (Protheus e Corten):** Retenção inicial de 20% das demandas de primeiro atendimento via assistente especializado (TOTVS S.A., 2026).

---

## 6. Referências Bibliográficas (Formato ABNT)

- AYRES, Julia. **Métricas para chatbots: quais os melhores KPIs para você analisar?** Infobip, 1 maio 2023. Disponível em: <https://www.infobip.com/pt/blog/metricas-para-chatbots>. Acesso em: 15 nov. 2026.
- BROWN, Tom B. et al. **Language models are few-shot learners.** In: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS, 33., 2020. Anais [...]. Curran Associates, 2020. p. 1877-1901. Disponível em: <https://arxiv.org/abs/2005.14165>. Acesso em: 15 nov. 2026.
- BRYNJOLFSSON, Erik; LI, Danielle; RAYMOND, Lindsey R. **Generative AI at work.** National Bureau of Economic Research, 2023. Publicado em: *Quarterly Journal of Economics*, v. 140, n. 2, p. 889-942, 2025. DOI: <https://doi.org/10.3386/w31161>.
- INTERNATIONAL ORGANIZATION FOR STANDARDIZATION (ISO). **ISO 9241-11:2018: Ergonomics of human-system interaction — Part 11: Usability: Definitions and concepts.** Genebra: ISO, 2018. Disponível em: <https://www.iso.org/standard/63500.html>.
- JI, Ziwei et al. **Survey of hallucination in natural language generation.** *ACM Computing Surveys*, New York, v. 55, n. 12, art. 248, 2023. DOI: <https://doi.org/10.1145/3571730>.
- JURAFSKY, Daniel; MARTIN, James H. **Speech and language processing.** 3. ed. (draft). Stanford: Stanford University, 2025. Disponível em: <https://web.stanford.edu/~jurafsky/slp3/>.
- KALAI, Adam Tauman et al. **Why language models hallucinate.** *arXiv preprint arXiv:2509.04664*, 2025.
- LEWIS, Patrick et al. **Retrieval-augmented generation for knowledge-intensive NLP tasks.** In: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS (NeurIPS), 33., 2020. p. 9459-9474.
- MANNING, Christopher D.; RAGHAVAN, Prabhakar; SCHÜTZE, Hinrich. **Introduction to information retrieval.** Cambridge: Cambridge University Press, 2008.
- OPENAI. **Harness engineering: leveraging Codex in an agent-first world.** 11 fev. 2026g. Disponível em: <https://openai.com/index/harness-engineering/>.
- OPENAI DEVELOPERS. **Voice agents.** OpenAI API Docs, 2026c. Disponível em: <https://developers.openai.com/api/docs/guides/voice-agents>.
- RADFORD, Alec et al. **Robust speech recognition via large-scale weak supervision.** 2023. Disponível em: <https://arxiv.org/abs/2212.04356>.
- REIMERS, Nils; GUREVYCH, Iryna. **Sentence-BERT: sentence embeddings using Siamese BERT-networks.** In: EMNLP, 2019. Disponível em: <https://arxiv.org/abs/1908.10084>.
- ROSENBERG, Jonathan et al. **SIP: Session Initiation Protocol.** RFC 3261. IETF, 2002. Disponível em: <https://www.rfc-editor.org/rfc/rfc3261>.
- RUSSELL, Stuart; NORVIG, Peter. **Artificial intelligence: a modern approach.** 4. ed. Pearson, 2021.
- SHUSTER, Kurt et al. **Retrieval augmentation reduces hallucination in conversation.** In: EMNLP 2021. ACL, 2021. Disponível em: <https://arxiv.org/abs/2104.07567>.
- TOTVS S.A. **Informações trimestrais: 30 de setembro de 2026.** 2026.
- TWILIO. **ConversationRelay best practices.** Twilio Docs, 2026a. Disponível em: <https://www.twilio.com/docs/voice/conversationrelay/best-practices>.
- VASWANI, Ashish et al. **Attention is all you need.** In: NeurIPS, 30., 2017. p. 5998-6008.
- WEIZENBAUM, Joseph. **ELIZA: a computer program for the study of natural language communication between man and machine.** *Communications of the ACM*, v. 9, n. 1, p. 36-45, 1966.

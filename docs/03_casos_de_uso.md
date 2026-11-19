# Especificação de Casos de Uso

## 1. Diagrama Geral de Casos de Uso
O diagrama a seguir detalha as interações dos atores (Usuário, Gateway Telefônico e Suporte N1) com os casos de uso do sistema **ERP Helpper**.

```mermaid
flowchart LR
    subgraph Atores
        U["fa:fa-user Usuário"]
        GT["fa:fa-phone Gateway Telefônico"]
        SN1["fa:fa-headset Suporte N1"]
    end

    subgraph Sistema ["Sistema ERP Helpper"]
        UC1(["Consultar Dúvida via Chat"])
        UC2(["Atender Chamada Telefônica"])
        UC3(["Processar Banco Vetorial"])
        UC4(["Escalonar para Suporte N1"])
        UC5(["Registrar Erro / Fallback"])
    end

    U --> UC1
    U --> GT
    GT --> UC2

    UC1 -.->|«include»| UC3
    UC2 -.->|«include»| UC3

    UC3 -.->|«extend» (Sem resposta satisfatória)| UC4
    UC3 -.->|«extend» (Falha de conexão / transcrição)| UC5

    UC4 --> SN1
```

---

## 2. Atores do Sistema

| Ator | Tipo | Papel no Sistema |
| :--- | :--- | :--- |
| **Usuário** | Primário (Humano) | Colaborador/operador do UNO ERP que submete perguntas de texto ou liga para o canal de voz em busca de auxílio sobre rotinas do sistema. |
| **Gateway Telefônico** | Secundário (Sistema) | Serviço de telefonia e VoIP (ex: Twilio) que estabelece e gerencia o canal de comunicação por voz entre o usuário e o fluxo do assistente. |
| **Suporte N1** | Secundário (Humano) | Equipe de atendimento humano da parceira que recebe os casos de dúvida escalonados em situações atípicas ou não documentadas. |

---

## 3. Especificação Detalhada de Casos de Uso

### Caso de Uso: RF04 - Consultar Dúvida

| Campo | Descrição |
| :--- | :--- |
| **Identificador** | **UC01 / RF04** |
| **Nome** | Consultar Dúvida (via Chat Web ou Voz) |
| **Ator Principal** | Usuário |
| **Atores Secundários** | Gateway Telefônico (no canal voz), Suporte N1 (em caso de escalonamento) |
| **Pré-Condições** | 1. O usuário tem acesso à interface web ou ao número do canal de voz.<br>2. O servidor da Search API e o banco vetorial ChromaDB estão ativos.<br>3. Credenciais da API OpenAI e fluxos do n8n estão operacionais. |
| **Pós-Condições** | O usuário recebe uma resposta fundamentada na documentação do UNO ERP com formatação clara e links de fontes oficiais, ou mensagem amigável de contingência/escalonamento. |

#### Fluxo Principal de Ações (Quadro 1 da Análise)

| Passo | Ação do Ator | Ação do Sistema |
| :---: | :--- | :--- |
| **1** | O usuário acessa a funcionalidade "Consultar Dúvida" (chat web ou chamada telefônica). | |
| **2** | | O sistema apresenta o campo para inserção da pergunta (ou inicia a escuta telefônica com saudação). |
| **3** | O usuário digita ou fala a sua dúvida e submete a mensagem. | |
| **4** | | O sistema recebe a pergunta, valida sintaticamente e normaliza os caracteres. |
| **5** | | O sistema executa a **vetorização da pergunta**, gerando embeddings via modelo OpenAI (`text-embedding-3-small`). |
| **6** | | O sistema compara os vetores gerados com o banco vetorial ChromaDB, executando busca semântica por similaridade de cosseno somada à busca lexical por palavras-chave. |
| **7** | | O sistema identifica os documentos mais relevantes através de reclassificação (*reranking* com `gpt-4o-mini`) e compõe a resposta contextualizada via n8n. |
| **8** | | O sistema devolve a resposta final ao usuário (em HTML no chat ou sintetizada em áudio de voz com ElevenLabs). |

#### Fluxos Alternativos e de Exceção

- **Fluxo Alternativo A1 - Match Exato de Código de Rejeição (ex: Rejeição 201):**
  - No passo 6, se a dúvida contiver padrões como `rejeição 201`, o algoritmo de busca identifica o documento específico (ID 314) com prioridade máxima e ignora o custo do LLM Reranker, acelerando a resposta.
- **Fluxo de Exceção E1 - Documentação Insuficiente (Escalonamento para Suporte N1):**
  - Se a busca no banco vetorial não retornar trechos com score de similaridade aceitável, o sistema emite resposta informando a ausência de dados na base e encaminha o ticket/protocolo para a fila do Suporte N1.
- **Fluxo de Exceção E2 - Falha de Conectividade ou Ausência de Tokens de API:**
  - Caso haja indisponibilidade de rede ou falha na chamada da OpenAI/ElevenLabs, o sistema captura a exceção, registra log de auditoria no servidor e aciona mensagem de contingência ao usuário ("*Serviço momentaneamente indisponível. Por favor contate o suporte*").

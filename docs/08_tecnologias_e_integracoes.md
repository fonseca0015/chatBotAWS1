# Tecnologias Utilizadas e Ecossistema de Integrações

## 1. Stack Tecnológico Principal

### 1.1. Linguagem e Back-end
- **Python 3.10+**: Linguagem central que executa todo o processamento de ingestão, normalização documental, cálculo de embeddings, busca híbrida e orquestração da API.
- **Flask**: Microframework web em Python utilizado para expor o microsserviço de busca (`POST /search`). Escolhido por sua simplicidade, performance enxuta e facilidade de integração em containers.
- **tiktoken**: Biblioteca da OpenAI para contagem e segmentação exata de tokens. Permite particionar os manuais do UNO ERP em chunks de tamanho ideal (`max_tokens=2000`, `overlap=500`), evitando truncamento nos modelos de embedding.

### 1.2. Banco de Dados e Armazenamento Vetorial
- **ChromaDB**: Banco vetorial open-source leve e de alta eficiência. Opera em modo persistente local (`base_de_conhecimento_db/`), utilizando o algoritmo HNSW com métrica de similaridade por cosseno (`hnsw:space: cosine`).
- **JSON**: O arquivo `knowledge_base.json` atua como fonte de verdade dos manuais, contendo categorias, títulos, links e textos integrais.

### 1.3. Inteligência Artificial e Modelos
- **OpenAI `text-embedding-3-small`**: Modelo de representação vetorial denso (1536 dimensões) com excelente equilíbrio entre precisão semântica e custo reduzido.
- **OpenAI `gpt-4o-mini`**: Modelo de linguagem de última geração utilizado para:
  1. *Query Expansion*: Expansão de termos técnicos da pergunta do usuário.
  2. *LLM Reranking*: Reclassificação de relevância dos candidatos documentais.
  3. *Generative Synthesis*: Redação da resposta final estruturada e contextualizada no n8n.

### 1.4. Orquestração e Integração de Fluxos
- **n8n**: Plataforma de automação de workflows baseada em nós. Recebe os webhooks da interface web ou do gateway de voz, invoca a Search API, consulta a OpenAI e prepara o payload final.
- **JavaScript (no n8n)**: Scripts internos para limpeza de saídas, remoção de markdown incompatível e conversão de fontes em tags HTML estruturadas.

### 1.5. Interface e Canais de Comunicação
- **Frontend Web (HTML5 / CSS3 / Vanilla JS)**: Interface responsiva em modo escuro com indicadores visuais de digitação (*typing indicator*), histórico de mensagens e área dedicada a fontes com links clicáveis.
- **ElevenLabs API**: Motor de síntese de voz neural (*Text-to-Speech*) de altíssima fidelidade utilizado para converter respostas de texto em chamadas de voz com cadência humana.

---

## 2. Tecnologias Complementares e Ecossistema do Projeto

O ecossistema do ERP Helpper foi estruturado considerando tecnologias complementares para viabilizar as próximas etapas de expansão e sustentação:

| Tecnologia / Ferramenta | Papel no Ecossistema | Descrição e Aplicação |
| :--- | :--- | :--- |
| **ElevenLabs** | Síntese de Voz (TTS) | Permite gerar vozes ultra-realistas com inteligência artificial, conferindo tom humanizado e profissional ao atendimento telefônico. |
| **Lovable** | Prototipação Ágil | Plataforma com IA para acelerar a criação e evolução de interfaces de usuário sem complexidade de infraestrutura. |
| **Bubble** | Plataforma No-Code | Plataforma voltada para a criação de painéis administrativos e portais internos de suporte sem necessidade de programação manual. |
| **OpenClaw** | Automação Digital | Ferramenta voltada para automação de tarefas e processos digitais com IA para aumentar a produtividade operacional. |
| **ViverdeIA** | Hub de Soluções de IA | Plataforma voltada a estratégias e ecossistemas inteligentes para aplicações de negócio. |
| **VoIP (Voice over IP)** | Telecomunicações | Protocolo de transmissão de voz pela internet, substituindo a telefonia convencional e permitindo integração nativa com o gateway de IA. |
| **MCP (Model Context Protocol)** | Protocolo de Integração | Padrão aberto criado para conectar com segurança modelos de IA a fontes de dados locais, ferramentas e sistemas corporativos. |
| **WhatsApp** | Canal Mensageria | Canal estratégico para futura disponibilização do assistente via mensagens de texto e áudio para os operadores do ERP. |

---

## 3. Referências Bibliográficas e Links Oficiais

1. **ElevenLabs**: Síntese de Voz e IA de Áudio. Disponível em: <https://elevenlabs.io/>. Acesso em: 06 abr. 2026.
2. **Lovable**: Desenvolvimento Ágil com IA. Disponível em: <https://lovable.dev/>. Acesso em: 06 abr. 2026.
3. **Bubble**: Plataforma No-Code para Aplicações Web. Disponível em: <https://bubble.io/>. Acesso em: 06 abr. 2026.
4. **OpenClaw**: Automação e IA para Tarefas Digitais. Disponível em: <https://www.hostinger.com/br/tutoriais/o-que-e-openclaw>. Acesso em: 06 abr. 2026.
5. **ViverdeIA**: Plataforma de Automações Inteligentes. Disponível em: <https://viverdeia.ai/>. Acesso em: 06 abr. 2026.
6. **Leads2b**: O que é VoIP e como funciona. Disponível em: <https://leads2b.com/blog/o-que-e-voip-e-como-funciona/>. Acesso em: 06 abr. 2026.
7. **Google Cloud**: Model Context Protocol (MCP). Disponível em: <https://cloud.google.com/discover/what-is-model-context-protocol?hl=pt-BR>. Acesso em: 06 abr. 2026.
8. **WhatsApp Business**: FAQ e Documentação de Mensageria. Disponível em: <https://faq.whatsapp.com/?locale=pt_BR>. Acesso em: 06 abr. 2026.

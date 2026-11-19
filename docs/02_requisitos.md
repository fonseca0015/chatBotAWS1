# Análise e Especificação de Requisitos

## 1. Técnica Utilizada para Levantamento dos Requisitos
O levantamento e refinamento dos requisitos do sistema **ERP Helpper** foram conduzidos através de reuniões e entrevistas estruturadas com o representante da empresa parceira, **Tiago Garcia Amato**. Durante essas sessões foram mapeadas as reais dores do suporte N1, os erros operacionais mais frequentes dos clientes do UNO ERP e os critérios técnicos de viabilidade para canais Web e Telefonia.

---

## 2. Requisitos Funcionais (RF)

| Identificador | Nome do Requisito | Descrição Detalhada | Prioridade |
| :--- | :--- | :--- | :--- |
| **RF01** | Atender via Chatbot | O sistema deverá manter o atendimento via Chatbot funcional, processando e respondendo prontamente às solicitações e dúvidas de texto do usuário. | Essencial |
| **RF02** | Estabelecer Interação por Voz | O sistema deverá estabelecer a comunicação com o usuário exclusivamente por meio de voz durante a chamada telefônica, sem a necessidade de interface visual. | Importante |
| **RF03** | Consultar Base de Conhecimento Integrada | O sistema deverá consultar a base vetorial integrada para recuperar os trechos documentais pertinentes à dúvida do usuário antes da geração de resposta. | Essencial |
| **RF04** | Responder a Dúvidas Frequentes | O sistema deverá responder com alta precisão e rapidez às dúvidas mais recorrentes através do Chatbot, otimizando o tempo de resolução. | Essencial |
| **RF05** | Escalonar Atendimento | O sistema deverá encaminhar automaticamente os casos com dúvidas complexas ou não resolvidas para o suporte humano de nível N1 da empresa. | Importante |
| **RF06** | Atualizar Continuamente o Agente de IA | O sistema deverá permitir a reindexação e vetorização periódica da base de conhecimento conforme novos manuais e tutoriais do ERP forem publicados. | Importante |
| **RF07** | Converter Fala em Texto em Tempo Real (STT) | O sistema deverá converter a fala do usuário em texto com alta fidelidade semântica para que a busca vetorial não seja prejudicada por variações de dicção ou ruído. | Essencial (Voz) |
| **RF08** | Sintetizar Voz (TTS) | O sistema deverá processar a resposta textual formulada e sintetizá-la em áudio de alta naturalidade através da API do ElevenLabs com tom profissional. | Essencial (Voz) |
| **RF09** | Gerenciar Turnos de Conversa (Duplex) | O sistema deverá detectar pausas naturais na fala do usuário para cessar a escuta e iniciar o processamento da resposta, evitando sobreposição de falas. | Importante (Voz) |
| **RF10** | Integrar com Gateway de Telefonia | O sistema deverá integrar-se a gateways telefônicos (ex: Twilio / provedores SIP/VoIP) para receber e originar chamadas telefônicas do canal de voz. | Essencial (Voz) |

---

## 3. Requisitos Não Funcionais (RNF)

| Identificador | Categoria | Descrição | Métrica / Critério de Aceitação |
| :--- | :--- | :--- | :--- |
| **RNF01** | Eficiência de Resposta | O tempo de processamento e retorno da resposta textual deve ser otimizado para não impactar a usabilidade do usuário. | Tempo médio de busca RAG $\le 3$ segundos. |
| **RNF02** | Usabilidade | Interface de chat web limpa, intuitiva, responsiva, amigável em dispositivos móveis e desktops, com tema escuro e digitação assistida. | Padrão ergonômico moderno com preview visual. |
| **RNF03** | Confiabilidade | Alta disponibilidade operacional para atender a dúvidas dos clientes em qualquer horário comercial e em regime estendido. | Disponibilidade $\ge 99\%$. |
| **RNF04** | Segurança e Privacidade | Preservação rigorosa da integridade dos manuais, confidencialidade de tokens e credenciais (`.env`), sem exposição indevida de dados corporativos. | Conformidade com LGPD e boas práticas de segredos. |
| **RNF05** | Escalabilidade | Arquitetura modular que suporta o crescimento simultâneo de requisições de chat e chamadas de voz concorrentes. | Suporte a chamadas simultâneas sem degradação do banco. |
| **RNF06** | Latência Fim-a-Fim (Ponta a Ponta) | No canal de voz, o tempo entre o término da fala do usuário e a primeira emissão de áudio da IA não deve quebrar a fluidez humana da conversa. | Latência total $\le 2,5$ segundos. |
| **RNF07** | Tolerância a Ruído de Fundo | O subsistema de captura e transcrição de áudio deve filtrar ruídos urbanos e de escritórios barulhentos para não desviar a transcrição. | Transcrição precisa com cancelamento de ruído. |
| **RNF08** | Gestão de Custos e Tokenização | O sistema deve possuir monitoramento de créditos de API (ElevenLabs TTS, STT e tokens OpenAI) e limite protetivo de duração por chamada/sessão. | Travas de limite e alertas de saldo no n8n/painéis. |
| **RNF09** | Identificação de Falha de Conexão | Em caso de perda de conexão com o banco vetorial ou APIs de terceiros, deve ser acionado um fallback com aviso ao usuário e registro de logs detalhados. | Resposta de contingência e log no servidor em caso de erro. |

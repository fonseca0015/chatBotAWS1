# Contexto e Visão Geral do Projeto

## 1. Visão Geral do Produto
O **ERP Helpper** é um assistente virtual inteligente baseado em Inteligência Artificial generativa e arquitetura **RAG** (*Retrieval-Augmented Generation*), projetado para atender usuários do **UNO ERP** e responder a dúvidas simples, recorrentes e problemas operacionais do dia a dia (como parametrizações fiscais, erros de tela e códigos de rejeição).

O sistema foi concebido para atuar em duas fases de evolução:
- **Fase 1 (Web Chat):** Interface web conversacional ágil e moderna disponibilizada para autoatendimento imediato.
- **Fase 2 (Canal de Voz / Telefonia Inteligente):** Atendimento por voz via chamada telefônica com IA, permitindo interação natural em tempo real (Full Duplex) por meio de síntese de voz e reconhecimento de fala.

## 2. Objetivo de Negócio
O principal objetivo do projeto é **reduzir drasticamente a demanda sobre o suporte N1 da empresa parceira**, oferecendo um primeiro nível de suporte automatizado, confiável e embasado diretamente na documentação oficial e base de conhecimento homologada do UNO ERP.

### Benefícios Principais:
- **Resolução Imediata de Dúvidas Cotidianas:** Redução do tempo de espera do cliente final.
- **Alívio da Fila N1:** A equipe humana de suporte passa a focar apenas em problemas de alta complexidade ou que exigem intervenções operacionais diretas no banco de dados do ERP.
- **Respostas Baseadas em Fatos:** A aplicação de RAG mitiga alucinações de modelos de linguagem, restringindo o conteúdo gerado aos manuais do sistema.
- **Multicanalidade Integrada:** O usuário pode escolher tirar dúvidas via chat ou chamada telefônica, mantendo a mesma base de conhecimento como referência.

## 3. Delimitação de Escopo
- **Sistema de Consulta:** O ERP Helpper atua estritamente como um assistente consultivo e de orientação. Ele **não altera** dados, cadastros ou registros diretamente dentro do UNO ERP.
- **Público-Alvo:** Usuários operacionais e administrativos que utilizam o ERP diariamente em empresas parceiras.
- **Escalonamento:** Situações não contempladas pela base documental ou com respostas insatisfatórias são formalmente escalonadas para a equipe humana de Suporte N1.

## 4. Histórico de Alinhamento com a Empresa Parceira
O escopo, regras de negócio e requisitos do projeto foram mapeados e validados em reuniões técnicas e executivas com o representante da parceira, **Tiago Garcia Amato**, e com a liderança de projeto (**Cesar**), definindo:
1. As prioridades para tratamento de dúvidas críticas (ex.: rejeições fiscais de NFe como a Rejeição 201).
2. O levantamento de custos e restrições com provedores de nuvem (n8n, ElevenLabs e OpenAI).
3. A definição de métricas de confiabilidade e desempenho para o assistente.

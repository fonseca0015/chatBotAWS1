# Contexto e Visão Geral do Projeto

## 1. Visão Geral do Produto
O **ERP Helpper** é um assistente virtual inteligente baseado em Inteligência Artificial generativa e arquitetura **RAG** (*Retrieval-Augmented Generation*), projetado para atender usuários do **UNO ERP** e responder a dúvidas simples, recorrentes e problemas operacionais do dia a dia (como parametrizações fiscais, erros de tela e códigos de rejeição).

O sistema foi concebido para atuar em duas fases de evolução:
- **Fase 1 (Web Chat):** Interface web conversacional ágil e moderna disponibilizada para autoatendimento imediato.
- **Fase 2 (Canal de Voz / Telefonia Inteligente):** Atendimento por voz via chamada telefônica com IA, permitindo interação natural em tempo real (Full Duplex) por meio de síntese de voz e reconhecimento de fala.

## 2. Estrutura de Suporte Técnico (N1, N2 e N3) e o Cenário da Uno Soluções

Em empresas fornecedoras de sistemas ERP (*Enterprise Resource Planning*), a estrutura de atendimento é tradicionalmente escalonada em três níveis:
- **Suporte de Nível 1 (N1):** Porta de entrada do usuário. Recebe, registra, tria e resolve dúvidas operacionais simples, como permissões de acesso, dúvidas de cadastro de clientes/produtos, configurações de telas e emissão de notas fiscais com rejeições da SEFAZ. O atendimento baseia-se em manuais e FAQs.
- **Suporte de Nível 2 (N2):** Profissionais dedicados a análises técnicas intermediárias, inconsistências de dados no banco relacional ou configurações avançadas de infraestrutura.
- **Suporte de Nível 3 (N3):** Equipe de engenharia de software e desenvolvimento do ERP, responsável por correções de bugs no código-fonte e atualizações estruturais do sistema.

### O Desafio Identificado
Devido ao elevado volume de chamados recebidos pelo suporte N1 da **Uno Soluções**, identificou-se que a maior parte das dúvidas dos clientes eram repetitivas e já contavam com resolução documentada na base de conhecimento corporativa. A equipe humana ficava sobrecarregada com atendimentos de baixo valor agregado, gerando filas de espera e custos operacionais elevados.

### A Proposta do ERP Helpper
Criar um **agente de inteligência artificial de autoatendimento multicanal (Web Chat e Voz)** que consulte os dados homologados da Uno Soluções via arquitetura RAG e forneça respostas imediatas, precisas e contextualizadas, encaminhando à equipe humana apenas os casos de alta complexidade.

---

## 3. Delimitação de Escopo
- **Sistema de Consulta:** O ERP Helpper atua estritamente como um assistente consultivo e de orientação. Ele **não altera** dados, cadastros ou registros diretamente dentro do UNO ERP.
- **Público-Alvo:** Usuários operacionais e administrativos que utilizam o ERP diariamente em empresas clientes da Uno Soluções.
- **Escalonamento:** Situações não contempladas pela base documental ou com respostas insatisfatórias são formalmente escalonadas para a equipe humana de Suporte N1.

---

## 4. Histórico de Alinhamento e Governança
O escopo, regras de negócio e requisitos do projeto foram mapeados e validados em reuniões técnicas com o representante da parceira, **Tiago Garcia Amato**, e sob orientação e mediação do professor coordenador **Prof. Antônio Cesar de Barros Munari**, definindo:
1. As prioridades para tratamento de dúvidas críticas (ex.: rejeições fiscais de NFe como a Rejeição 201).
2. O levantamento de custos e restrições com provedores de nuvem (n8n, ElevenLabs e OpenAI).
3. A definição de métricas de confiabilidade e desempenho para o assistente.

---

## 5. Contexto Acadêmico: Projeto Integrador (FATEC Sorocaba)

Este projeto foi concebido e implementado no âmbito da disciplina de **Projeto Integrador (PI)** do **Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas — AMS**, da **Faculdade de Tecnologia de Sorocaba — José Crespo Gonzales (FATEC Sorocaba)**, vinculada ao **Centro Paula Souza (CPS)** e ao Governo do Estado de São Paulo.

### Identificação Institucional
- **Instituição:** Faculdade de Tecnologia de Sorocaba (FATEC Sorocaba — José Crespo Gonzales)
- **Órgão Mantenedor:** Centro Paula Souza (CPS) — Governo do Estado de São Paulo
- **Curso:** Superior de Tecnologia em Análise e Desenvolvimento de Sistemas (AMS)
- **Título do Trabalho:** Documentação de Desenvolvimento de Software — ERP Helpper
- **Orientador:** Prof. Antônio Cesar de Barros Munari
- **Empresa Parceira:** Uno Soluções (Representante Técnico: Tiago Garcia Amato)
- **Local e Data:** Sorocaba/SP — Novembro de 2026

### 👥 Equipe de Desenvolvimento (Autores)
| Nome Completo | Papel no Projeto Integrador |
| :--- | :--- |
| **Andreus Vinicius Araújo de Andrade** | Engenharia de Requisitos e Modelagem Conceitual |
| **Arthur do Amaral Barreto** | Qualidade de Software, Testes e Avaliação de Usabilidade |
| **Cauã de Andrade Nogueira** | Engenharia de Dados, Chunking e Curadoria Documental |
| **Gabriel Fonseca de Lemos** | Orquestração de Fluxos n8n, Infraestrutura e Redes |
| **Pedro Henrique Cardozo Dias** | Arquitetura RAG, Desenvolvimento Full Stack e Busca Híbrida |

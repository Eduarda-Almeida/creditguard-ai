# 🛡️ CreditGuard AI

### Assistente inteligente de análise preliminar de crédito imobiliário

O **CreditGuard AI** é uma aplicação web educacional que combina regras de negócio, programação em Python e inteligência artificial generativa para simular análises preliminares de elegibilidade de crédito imobiliário.

O projeto surgiu da experiência profissional de sua desenvolvedora no setor de crédito imobiliário, com o objetivo de explorar como a IA pode apoiar a interpretação de dados financeiros, identificar inconsistências e automatizar a elaboração de pareceres explicativos.

**🔗 Demonstração online:** [https://creditguard-ai-dt5qwutnfguky8w7nygem8.streamlit.app/]

## ✨ Funcionalidades

- Cadastro de cliente fictício com nome, CPF e data de nascimento.
- Registro de renda declarada, renda comprovada, parcelas e despesas.
- Informações sobre avaliação do imóvel e financiamento pretendido.
- Entrada manual de score fictício.
- Cálculo de comprometimento de renda, endividamento total e percentual financiado.
- Identificação de inconsistências com base em critérios educacionais.
- Classificação de elegibilidade simulada, acompanhada dos motivos.
- Sugestão demonstrativa de data para acompanhamento das pendências.
- Geração de parecer explicativo utilizando o Gemini.
- Exportação de relatório em arquivo de texto.

## 🤖 Como a inteligência artificial é utilizada?

A aplicação utiliza uma arquitetura com duas etapas:

**1. Análise estruturada com Python**

O sistema calcula indicadores financeiros e verifica critérios previamente definidos. Essa etapa determina o resultado da simulação.

**2. Interpretação com Gemini**

A inteligência artificial recebe os indicadores calculados e as pendências identificadas para gerar um parecer explicativo, com recomendações educativas.

A IA não modifica os critérios nem toma decisões reais de concessão de crédito.

## 🛠️ Tecnologias utilizadas

- Python
- Streamlit
- Google Gen AI SDK
- Gemini
- Git e GitHub
- Streamlit Community Cloud

## 📊 Critérios demonstrativos

Para fins exclusivamente educacionais, o protótipo considera:

- Divergência entre rendas de até 5%.
- Comprometimento da parcela de até 30%.
- Endividamento mensal total de até 40%.
- Financiamento de até 80% do valor de avaliação.
- Saldo de renda residual positivo.
- Score fictício igual ou superior a 600 pontos.
- Maioridade na data da análise.

Esses parâmetros foram definidos para demonstrar o funcionamento da aplicação e **não representam políticas oficiais de instituições financeiras**.

## 🔐 Privacidade e limitações

O CreditGuard AI deve ser utilizado somente com dados fictícios.

- Não consulta Serasa, SPC, BACEN ou bases bancárias.
- Não realiza aprovação ou reprovação real de crédito.
- Não prevê alterações futuras do score.
- Não utiliza nome, CPF ou data de nascimento nas solicitações enviadas ao Gemini.
- Não possui banco de dados para armazenamento de informações dos clientes.

## ▶️ Execução local

1. Clone o repositório.
2. Instale as dependências do arquivo `requirements.txt`.
3. Configure sua chave do Gemini em `.streamlit/secrets.toml`, utilizando o nome `GEMINI_API_KEY`.
4. Execute `python -m streamlit run app.py`.

A chave de API deve permanecer privada e não deve ser publicada no repositório.

## 👩🏽‍💻 Desenvolvedora

**Maria Eduarda Almeida**

Graduanda em Sistemas de Informação pelo Instituto Federal da Bahia (IFBA) e profissional da área de análise de crédito imobiliário.

Este projeto representa a aplicação prática de conhecimentos em programação, integração de APIs, inteligência artificial generativa e análise de processos de negócio.

---

**CreditGuard AI — Tecnologia aplicada à análise financeira, com responsabilidade e transparência.**
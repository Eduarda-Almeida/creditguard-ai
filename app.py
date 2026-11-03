import streamlit as st
from google import genai

st.set_page_config(
    page_title="CreditGuard AI",
    page_icon="🛡️"
)

st.title("🛡️ CreditGuard AI")
st.write("Assistente inteligente de análise preliminar de crédito")
st.caption("Protótipo educacional com dados fictícios.")

st.divider()

st.subheader("Informações financeiras")

renda = st.number_input(
    "Renda mensal fictícia (R$)",
    min_value=0.0,
    value=5000.0,
    step=100.0
)

parcela = st.number_input(
    "Parcela mensal fictícia (R$)",
    min_value=0.0,
    value=1500.0,
    step=100.0
)

if st.button("Analisar com IA"):

    if renda <= 0:
        st.error("Informe uma renda maior que zero.")

    else:
        comprometimento = (parcela / renda) * 100

        st.metric(
            "Comprometimento de renda",
            f"{comprometimento:.1f}%"
        )

        st.info(
            "Cálculo demonstrativo. "
            "Não representa aprovação de crédito."
        )

        prompt = f"""
        Você é um assistente educacional de análise financeira.

        Analise exclusivamente os dados fictícios abaixo:

        Renda mensal: R$ {renda:.2f}
        Parcela mensal: R$ {parcela:.2f}
        Comprometimento da renda: {comprometimento:.1f}%

        Apresente uma análise objetiva em português com:

        1. Interpretação do comprometimento da renda.
        2. Informações adicionais que deveriam ser verificadas.
        3. Limitações desta análise.

        Regras:
        - Não aprove nem reprove crédito.
        - Não invente informações ou regras bancárias.
        - Não afirme que existe risco comprovado sem evidências.
        - Informe que é necessária revisão humana.
        - Utilize no máximo 150 palavras.
        """

        st.subheader("🤖 Análise gerada por IA")

        try:
            cliente = genai.Client(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            with st.spinner("Gemini está analisando os dados..."):
                resposta = cliente.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

            if resposta.text:
                st.markdown(resposta.text)
            else:
                st.warning("A IA não retornou uma análise.")

        except Exception as erro:
            st.error(
                "Não foi possível gerar a análise. "
                "Verifique a conexão e a configuração da API."
            )
            st.caption(
                f"Tipo de erro: {type(erro).__name__}"
            )
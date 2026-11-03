import streamlit as st
from google import genai
from datetime import date, timedelta


# =====================================
# CONFIGURAÇÕES
# =====================================

st.set_page_config(
    page_title="CreditGuard AI",
    page_icon="🛡️",
    layout="wide"
)

VERSAO = "2.0"

# Critérios exclusivamente educacionais.
LIMITE_DIVERGENCIA_RENDA = 5
LIMITE_COMPROMETIMENTO = 30
LIMITE_ENDIVIDAMENTO = 40
LIMITE_FINANCIAMENTO = 80
SCORE_MINIMO_FICTICIO = 600
PRAZO_REAVALIACAO_FICTICIO = 30


# =====================================
# FUNÇÕES AUXILIARES
# =====================================

def formatar_reais(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X")
    texto = texto.replace(".", ",")
    texto = texto.replace("X", ".")
    return f"R$ {texto}"


def formatar_percentual(valor):
    return f"{valor:.1f}".replace(".", ",") + "%"


def calcular_idade(nascimento, referencia):
    idade = referencia.year - nascimento.year

    if (referencia.month, referencia.day) < (
        nascimento.month,
        nascimento.day
    ):
        idade -= 1

    return idade


def mascarar_cpf(cpf):
    numeros = "".join(c for c in cpf if c.isdigit())

    if len(numeros) == 11:
        return f"***.***.***-{numeros[-2:]}"

    return "***.***.***-**"


CAMPOS_FORMULARIO = [
    "nome_cliente",
    "cpf_cliente",
    "data_nascimento",
    "data_analise",
    "renda_declarada",
    "renda_comprovada",
    "parcela",
    "outras_dividas",
    "despesas",
    "valor_avaliacao",
    "valor_financiado",
    "score",
    "data_score",
    "data_regularizacao",
    "confirmacao"
]


def limpar_formulario():
    for campo in CAMPOS_FORMULARIO:
        st.session_state.pop(campo, None)

    st.session_state.pop("resultado", None)


# =====================================
# CABEÇALHO
# =====================================

st.title("🛡️ CreditGuard AI")

st.subheader(
    "Assistente inteligente de análise preliminar de crédito imobiliário"
)

st.caption(
    "Projeto de portfólio desenvolvido com Python, "
    "Streamlit e Inteligência Artificial Generativa."
)

st.warning(
    "⚠️ AMBIENTE EDUCACIONAL: utilize somente dados fictícios. "
    "As regras são demonstrativas e não correspondem aos critérios "
    "de aprovação de qualquer instituição financeira. "
    "O sistema não consulta bureaus de crédito nem aprova empréstimos."
)

st.button(
    "🧹 Limpar formulário",
    on_click=limpar_formulario
)

st.divider()


# =====================================
# FORMULÁRIO
# =====================================

with st.form("formulario_creditguard"):

    st.header("👤 Identificação do Cliente")

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        nome_cliente = st.text_input(
            "Nome do cliente",
            value="",
            placeholder="Digite um nome fictício",
            key="nome_cliente"
        )

        data_nascimento = st.date_input(
            "Data de nascimento",
            value=None,
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            format="DD/MM/YYYY",
            key="data_nascimento"
        )

    with coluna2:
        cpf_cliente = st.text_input(
            "CPF fictício",
            value="",
            placeholder="000.000.000-00",
            key="cpf_cliente"
        )

        data_analise = st.date_input(
            "Data da análise",
            value=None,
            format="DD/MM/YYYY",
            key="data_analise"
        )

    st.divider()

    st.header("💰 Informações Financeiras")

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        renda_declarada = st.number_input(
            "Renda mensal declarada (R$)",
            min_value=0.0,
            value=None,
            step=100.0,
            placeholder="Informe a renda",
            key="renda_declarada"
        )

        parcela = st.number_input(
            "Parcela mensal pretendida (R$)",
            min_value=0.0,
            value=None,
            step=100.0,
            placeholder="Informe a parcela",
            key="parcela"
        )

        despesas = st.number_input(
            "Despesas essenciais mensais (R$)",
            min_value=0.0,
            value=None,
            step=100.0,
            placeholder="Informe as despesas",
            key="despesas"
        )

    with coluna2:
        renda_comprovada = st.number_input(
            "Renda mensal comprovada (R$)",
            min_value=0.0,
            value=None,
            step=100.0,
            placeholder="Informe a renda",
            key="renda_comprovada"
        )

        outras_dividas = st.number_input(
            "Outras parcelas de dívidas mensais (R$)",
            min_value=0.0,
            value=None,
            step=100.0,
            placeholder="Informe o valor ou zero",
            key="outras_dividas"
        )

    st.divider()

    st.header("🏠 Informações do Imóvel")

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        valor_avaliacao = st.number_input(
            "Valor de avaliação do imóvel (R$)",
            min_value=0.0,
            value=None,
            step=1000.0,
            placeholder="Informe o valor",
            key="valor_avaliacao"
        )

    with coluna2:
        valor_financiado = st.number_input(
            "Valor pretendido de financiamento (R$)",
            min_value=0.0,
            value=None,
            step=1000.0,
            placeholder="Informe o valor",
            key="valor_financiado"
        )

    st.divider()

    st.header("📊 Score de Crédito Fictício")

    st.info(
        "O score deve ser informado manualmente e será utilizado "
        "apenas nesta simulação. Não existe consulta à Serasa, "
        "ao SPC ou a qualquer outra base de crédito."
    )

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        score = st.number_input(
            "Score fictício (0 a 1000)",
            min_value=0,
            max_value=1000,
            value=None,
            step=1,
            placeholder="Informe o score fictício",
            key="score"
        )

    with coluna2:
        data_score = st.date_input(
            "Data de referência do score (opcional)",
            value=None,
            format="DD/MM/YYYY",
            key="data_score"
        )

    st.divider()

    st.header("📅 Planejamento de Reavaliação")

    data_regularizacao = st.date_input(
        "Previsão fictícia de regularização das pendências (opcional)",
        value=None,
        format="DD/MM/YYYY",
        key="data_regularizacao",
        help=(
            "Se houver pendências, o sistema poderá sugerir "
            "uma data de acompanhamento 30 dias depois."
        )
    )

    st.caption(
        "O prazo de 30 dias é uma hipótese criada para o projeto. "
        "Não representa previsão de alteração do score "
        "nem prazo de reanálise bancária."
    )

    st.divider()

    confirmacao = st.checkbox(
        "Confirmo que todos os dados informados são fictícios.",
        key="confirmacao"
    )

    enviar = st.form_submit_button(
        "🤖 Analisar com IA",
        type="primary",
        use_container_width=True
    )


# =====================================
# PROCESSAMENTO DA SIMULAÇÃO
# =====================================

if enviar:

    # Limpa o resultado anterior para não exibir dados desatualizados.
    st.session_state.resultado = None

    campos_obrigatorios = {
        "Nome do cliente": nome_cliente,
        "CPF fictício": cpf_cliente,
        "Data de nascimento": data_nascimento,
        "Data da análise": data_analise,
        "Renda declarada": renda_declarada,
        "Renda comprovada": renda_comprovada,
        "Parcela mensal": parcela,
        "Outras dívidas": outras_dividas,
        "Despesas essenciais": despesas,
        "Valor de avaliação": valor_avaliacao,
        "Valor financiado": valor_financiado,
        "Score fictício": score
    }

    faltantes = []

    for nome_campo, valor in campos_obrigatorios.items():

        if valor is None:
            faltantes.append(nome_campo)

        elif isinstance(valor, str) and not valor.strip():
            faltantes.append(nome_campo)

    if faltantes:

        st.error(
            "Preencha os campos obrigatórios antes de analisar: "
            + ", ".join(faltantes)
        )

    elif not confirmacao:

        st.error(
            "Confirme que está utilizando somente dados fictícios."
        )

    else:

        numeros_cpf = "".join(
            caracter for caracter in cpf_cliente
            if caracter.isdigit()
        )

        erro_validacao = None

        if len(numeros_cpf) != 11:
            erro_validacao = (
                "O CPF fictício deve conter 11 dígitos."
            )

        elif renda_declarada <= 0 or renda_comprovada <= 0:
            erro_validacao = (
                "As rendas declarada e comprovada "
                "devem ser maiores que zero."
            )

        elif parcela <= 0:
            erro_validacao = (
                "A parcela pretendida deve ser maior que zero."
            )

        elif valor_avaliacao <= 0 or valor_financiado <= 0:
            erro_validacao = (
                "A avaliação do imóvel e o financiamento "
                "devem ser maiores que zero."
            )

        elif data_nascimento > data_analise:
            erro_validacao = (
                "A data de nascimento não pode ser posterior "
                "à data da análise."
            )

        if erro_validacao:

            st.error(erro_validacao)

        else:

            # =================================
            # CÁLCULOS
            # =================================

            idade = calcular_idade(
                data_nascimento,
                data_analise
            )

            divergencia_renda = (
                abs(renda_declarada - renda_comprovada)
                / renda_comprovada
                * 100
            )

            comprometimento = (
                parcela / renda_comprovada * 100
            )

            endividamento_total = (
                (parcela + outras_dividas)
                / renda_comprovada
                * 100
            )

            percentual_financiado = (
                valor_financiado
                / valor_avaliacao
                * 100
            )

            saldo_residual = (
                renda_comprovada
                - parcela
                - outras_dividas
                - despesas
            )

            # =================================
            # REGRAS FICTÍCIAS
            # =================================

            criterios = [
                (
                    "Maioridade",
                    idade >= 18,
                    "Idade inferior a 18 anos na data da análise."
                ),
                (
                    "Compatibilidade das rendas",
                    divergencia_renda <= LIMITE_DIVERGENCIA_RENDA,
                    (
                        "Divergência entre renda declarada "
                        "e comprovada superior a 5%."
                    )
                ),
                (
                    "Comprometimento da parcela",
                    comprometimento <= LIMITE_COMPROMETIMENTO,
                    (
                        "Parcela superior a 30% "
                        "da renda comprovada."
                    )
                ),
                (
                    "Endividamento total",
                    endividamento_total <= LIMITE_ENDIVIDAMENTO,
                    (
                        "Comprometimento total superior "
                        "a 40% da renda comprovada."
                    )
                ),
                (
                    "Percentual de financiamento",
                    percentual_financiado <= LIMITE_FINANCIAMENTO,
                    (
                        "Financiamento pretendido superior "
                        "a 80% do valor de avaliação."
                    )
                ),
                (
                    "Saldo residual",
                    saldo_residual > 0,
                    (
                        "A renda residual após parcelas "
                        "e despesas não é positiva."
                    )
                ),
                (
                    "Score fictício",
                    score >= SCORE_MINIMO_FICTICIO,
                    (
                        "Score fictício abaixo de "
                        "600 pontos."
                    )
                )
            ]

            pendencias = [
                motivo
                for _, aprovado, motivo in criterios
                if not aprovado
            ]

            elegivel = len(pendencias) == 0

            if elegivel:

                status = (
                    "ELEGÍVEL NOS CRITÉRIOS SIMULADOS"
                )

            else:

                status = (
                    "NÃO ELEGÍVEL NOS CRITÉRIOS SIMULADOS"
                )

            # =================================
            # REAVALIAÇÃO FICTÍCIA
            # =================================

            data_reavaliacao = None

            if not elegivel and data_regularizacao is not None:

                data_base = max(
                    data_regularizacao,
                    data_analise
                )

                data_reavaliacao = (
                    data_base
                    + timedelta(
                        days=PRAZO_REAVALIACAO_FICTICIO
                    )
                )

            # =================================
            # PARECER COM GEMINI
            # =================================

            lista_pendencias = (
                "\n".join(f"- {p}" for p in pendencias)
                if pendencias
                else "Nenhuma pendência simulada."
            )

            prompt = f"""
Você é um assistente de um protótipo EDUCACIONAL
de análise preliminar de crédito imobiliário.

Os valores são inteiramente fictícios.

IMPORTANTE:
- Não aprove nem reprove crédito real.
- Não invente consultas à Serasa, SPC, BACEN ou bancos.
- Não afirme que houve consulta de score.
- Não altere o resultado das regras calculadas.
- Não invente informações adicionais do cliente.
- Não prometa aumento de score.
- Não apresente critérios fictícios como regras oficiais.
- Explique de forma profissional e objetiva.

DADOS NUMÉRICOS DA SIMULAÇÃO:

Idade: {idade} anos
Renda declarada: {renda_declarada}
Renda comprovada: {renda_comprovada}
Parcela: {parcela}
Outras dívidas mensais: {outras_dividas}
Despesas essenciais mensais: {despesas}
Valor de avaliação: {valor_avaliacao}
Valor financiado: {valor_financiado}
Score fictício informado manualmente: {score}

Comprometimento da parcela:
{comprometimento:.2f}%

Endividamento total:
{endividamento_total:.2f}%

Percentual financiado:
{percentual_financiado:.2f}%

Divergência de renda:
{divergencia_renda:.2f}%

Saldo residual:
{saldo_residual}

RESULTADO DEFINIDO PELO SISTEMA:
{status}

PENDÊNCIAS:
{lista_pendencias}

Escreva um parecer com:

1. Resumo da simulação.
2. Interpretação dos indicadores.
3. Explicação das pendências, se houver.
4. Recomendações educativas para nova análise.
5. Limitações dos dados e da simulação.

Não inclua conclusão de crédito real.
"""

            parecer_ia = (
                "Parecer de IA indisponível. "
                "Os cálculos e critérios simulados "
                "permanecem disponíveis."
            )

            with st.spinner(
                "Gerando parecer explicativo com Gemini..."
            ):

                try:

                    chave = st.secrets.get(
                        "GEMINI_API_KEY"
                    )

                    if not chave:
                        raise ValueError(
                            "Chave de IA não configurada."
                        )

                    cliente_ia = genai.Client(
                        api_key=chave
                    )

                    resposta = (
                        cliente_ia.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt
                        )
                    )

                    if resposta.text:
                        parecer_ia = resposta.text

                except Exception:

                    st.warning(
                        "Não foi possível gerar o parecer "
                        "com IA agora. Verifique a "
                        "configuração da chave e a cota "
                        "da API. A simulação continua disponível."
                    )

            # =================================
            # RELATÓRIO
            # =================================

            linhas_relatorio = [
                "CREDITGUARD AI",
                "RELATÓRIO EDUCACIONAL DE SIMULAÇÃO",
                "=" * 45,
                "",
                f"Cliente fictício: {nome_cliente}",
                f"CPF mascarado: {mascarar_cpf(cpf_cliente)}",
                (
                    "Data de nascimento: "
                    f"{data_nascimento:%d/%m/%Y}"
                ),
                f"Idade na análise: {idade} anos",
                f"Data da análise: {data_analise:%d/%m/%Y}",
                "",
                "INFORMAÇÕES FINANCEIRAS",
                f"Renda declarada: {formatar_reais(renda_declarada)}",
                f"Renda comprovada: {formatar_reais(renda_comprovada)}",
                f"Parcela: {formatar_reais(parcela)}",
                f"Outras dívidas: {formatar_reais(outras_dividas)}",
                f"Despesas: {formatar_reais(despesas)}",
                "",
                "INFORMAÇÕES DO IMÓVEL",
                f"Avaliação: {formatar_reais(valor_avaliacao)}",
                f"Financiamento: {formatar_reais(valor_financiado)}",
                "",
                "INDICADORES",
                (
                    "Comprometimento: "
                    f"{formatar_percentual(comprometimento)}"
                ),
                (
                    "Endividamento total: "
                    f"{formatar_percentual(endividamento_total)}"
                ),
                (
                    "Percentual financiado: "
                    f"{formatar_percentual(percentual_financiado)}"
                ),
                (
                    "Divergência de renda: "
                    f"{formatar_percentual(divergencia_renda)}"
                ),
                f"Saldo residual: {formatar_reais(saldo_residual)}",
                f"Score fictício: {score}",
                (
                    "Data de referência do score: "
                    + (
                        data_score.strftime("%d/%m/%Y")
                        if data_score
                        else "Não informada"
                    )
                ),
                "",
                f"RESULTADO: {status}",
                "",
                "PENDÊNCIAS"
            ]

            if pendencias:

                for pendencia in pendencias:
                    linhas_relatorio.append(
                        f"- {pendencia}"
                    )

            else:

                linhas_relatorio.append(
                    "Nenhuma pendência simulada."
                )

            linhas_relatorio.extend([
                "",
                "REAVALIAÇÃO",
                (
                    data_reavaliacao.strftime("%d/%m/%Y")
                    if data_reavaliacao
                    else "Não estimada"
                ),
                "",
                "PARECER EXPLICATIVO DA IA",
                parecer_ia,
                "",
                "AVISO:",
                (
                    "Simulação educacional com dados "
                    "e critérios fictícios."
                ),
                (
                    "Não representa aprovação, "
                    "reprovação ou consulta real de crédito."
                )
            ])

            relatorio = "\n".join(
                linhas_relatorio
            )

            # Salva resultado para não desaparecer
            # quando o usuário baixar o relatório.

            st.session_state.resultado = {
                "versao": VERSAO,
                "nome": nome_cliente,
                "cpf": mascarar_cpf(cpf_cliente),
                "data_nascimento": data_nascimento,
                "idade": idade,
                "data_analise": data_analise,
                "comprometimento": comprometimento,
                "endividamento_total": endividamento_total,
                "percentual_financiado": percentual_financiado,
                "saldo_residual": saldo_residual,
                "criterios": criterios,
                "status": status,
                "elegivel": elegivel,
                "data_reavaliacao": data_reavaliacao,
                "parecer_ia": parecer_ia,
                "relatorio": relatorio
            }


# =====================================
# EXIBIÇÃO DOS RESULTADOS
# =====================================

resultado = st.session_state.get("resultado")

if (
    isinstance(resultado, dict)
    and resultado.get("versao") == VERSAO
):

    st.divider()

    st.header("📋 Resultado da Simulação")

    st.write(
        f"**Cliente:** {resultado['nome']}"
    )

    st.write(
        f"**CPF:** {resultado['cpf']}"
    )

    st.write(
        "**Data de nascimento:** "
        f"{resultado['data_nascimento']:%d/%m/%Y}"
    )

    st.write(
        f"**Idade:** {resultado['idade']} anos"
    )

    st.write(
        "**Data da análise:** "
        f"{resultado['data_analise']:%d/%m/%Y}"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Comprometimento da parcela",
            formatar_percentual(
                resultado["comprometimento"]
            )
        )

    with col2:
        st.metric(
            "Endividamento total",
            formatar_percentual(
                resultado["endividamento_total"]
            )
        )

    with col3:
        st.metric(
            "Percentual financiado",
            formatar_percentual(
                resultado["percentual_financiado"]
            )
        )

    st.metric(
        "Saldo residual",
        formatar_reais(
            resultado["saldo_residual"]
        )
    )

    st.divider()

    if resultado["elegivel"]:

        st.success(
            "✅ " + resultado["status"]
        )

    else:

        st.error(
            "⚠️ " + resultado["status"]
        )

    st.subheader(
        "🔎 Verificação dos Critérios Simulados"
    )

    for nome_criterio, aprovado, motivo in resultado["criterios"]:

        if aprovado:

            st.write(
                f"✅ {nome_criterio}: "
                "critério demonstrativo atendido."
            )

        else:

            st.write(
                f"❌ {nome_criterio}: {motivo}"
            )

    if resultado["data_reavaliacao"]:

        st.info(
            "📅 Data sugerida para acompanhamento: "
            f"{resultado['data_reavaliacao']:%d/%m/%Y}. "
            "Estimativa educacional baseada em prazo "
            "fictício de 30 dias após a regularização "
            "ou a análise, o que for posterior. "
            "Não é previsão de melhora do score."
        )

    st.divider()

    st.header("🤖 Parecer Explicativo com IA")

    st.markdown(
        resultado["parecer_ia"]
    )

    st.divider()

    st.download_button(
        label="📥 Baixar Relatório da Simulação",
        data=resultado["relatorio"],
        file_name="creditguard_ai_relatorio.txt",
        mime="text/plain; charset=utf-8",
        use_container_width=True
    )

    st.caption(
        "Resultado demonstrativo. "
        "Não constitui decisão real de crédito."
    )


# =====================================
# RODAPÉ
# =====================================

st.divider()

st.caption(
    "CreditGuard AI | Projeto educacional de "
    "Maria Eduarda Almeida | Python + Streamlit + Gemini"
)
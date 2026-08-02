import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(
    page_title="FUTILA COMPRAS - Carrinho em Tempo Real",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicialização do Estado Global
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []


# 3. Funções de Manipulação dos Dados
# noinspection PyShadowingNames
def adicionar_produto(nome, mercado, preco, qtd):
    if not nome.strip():
        st.sidebar.error("Por favor, insira o nome do produto.")
        return

    subtotal = preco * qtd
    item_id = len(st.session_state.carrinho) + 1

    produto_dados = {
        "ID": item_id,
        "Supermercado": mercado,
        "Produto": nome,
        "Preço Unit. (€)": preco,
        "Qtd": qtd,
        "Subtotal (€)": subtotal
    }

    st.session_state.carrinho.append(produto_dados)
    st.toast(f"🛒 {nome} adicionado com sucesso!")


def remover_produto(idx_remover):
    st.session_state.carrinho.pop(idx_remover)
    st.toast("❌ Produto removido!")


def limpar_carrinho():
    st.session_state.carrinho = []
    st.toast("🧹 Carrinho totalmente limpo.")


# 4. PAINEL ESQUERDO (Sidebar para Inputs)
st.sidebar.header("➕ Adicionar Produto")

with st.sidebar.form(key="form_produto", clear_on_submit=True):
    mercado = st.selectbox(
        "Supermercado:",
        ["Continente", "Pingo Doce", "Lidl", "Mercadona", "Auchan", "Recheio", "Outro"]
    )

    nome = st.text_input("Nome do Produto:", placeholder="Ex: Leite Meio Gordo, Arroz...")
    preco = st.number_input("Preço Unitário (€):", min_value=0.0, step=0.01, format="%.2f", value=0.0)
    qtd = st.number_input("Quantidade:", min_value=1, step=1, value=1)

    # LINHA CORRIGIDA AQUI:
    btn_adicionar = st.form_submit_button("Colocar no Carrinho")

    if btn_adicionar:
        adicionar_produto(nome, mercado, preco, qtd)

# 5. PAINEL DIREITO (Visualização e Métricas)
st.title("🛒 FUTILA COMPRAS")
st.subheader("Carrinho de Compras em Tempo Real")

total_global = sum(item["Subtotal (€)"] for item in st.session_state.carrinho)
st.metric(label="Total no Carrinho", value=f"{total_global:.2f} €")

st.write("---")

if st.session_state.carrinho:
    df_carrinho = pd.DataFrame(st.session_state.carrinho)
    col_tabela, col_acoes = st.columns([3, 1])  # Ajuste de proporção para a tabela ficar maior

    with col_tabela:
        st.markdown("### Produtos no Meu Carrinho")
        st.dataframe(
            df_carrinho.drop(columns=["ID"]),
            use_container_width=True,
            hide_index=True
        )

    with col_acoes:
        st.markdown("### Ações")

        for idx, item in enumerate(st.session_state.carrinho):
            if st.button(f"Remover Item {idx + 1}", key=f"btn_del_{idx}", type="secondary"):
                remover_produto(idx)
                st.rerun()

        st.write("")
        if st.button("Esvaziar Carrinho", type="primary", use_container_width=True):
            limpar_carrinho()
            st.rerun()
else:
    st.info("O seu carrinho está vazio. Use o painel lateral para adicionar produtos!")

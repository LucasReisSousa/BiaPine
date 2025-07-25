import streamlit as st
import os
from bia import gerar_dicionario_word
from pine import atualizar_planilha
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

    if __name__ == "__main__":
        app.run(debug=True)

st.set_page_config(page_title="Ferramentas CKAN – BIA & PINE", layout="wide")
st.title("🔗 Ferramentas CKAN – BIA & PINE")

opcao = st.sidebar.radio("Escolha a ferramenta:", ["📖 BIA – Dicionário de Dados", "📈 PINE – Monitoramento"])

# ============================
# Aba BIA
# ============================
if opcao.startswith("📖"):
    st.header("📖 BIA – Gerar Dicionário de Dados em Word")
    recurso_url = st.text_input("Cole o link completo do recurso CKAN:")
    template_path = "modelo_bia2_pronto_para_preencher.docx"

    if st.button("Gerar Dicionário de Dados"):
        if not recurso_url:
            st.error("⚠️ Por favor, informe o link do recurso CKAN.")
        elif not os.path.exists(template_path):
            st.error("⚠️ Template não encontrado na pasta do app.")
        else:
            with st.spinner("Gerando o documento Word..."):
                try:
                    caminho_docx = gerar_dicionario_word(recurso_url, template_path)
                    if caminho_docx and os.path.exists(caminho_docx):
                        with open(caminho_docx, "rb") as file:
                            st.success("✅ Dicionário gerado com sucesso!")
                            st.download_button(
                                label="📥 Baixar Word",
                                data=file,
                                file_name=os.path.basename(caminho_docx),
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                    else:
                        st.error("❌ Não foi possível gerar o documento.")
                except Exception as e:
                    st.error(f"⚠️ Erro ao gerar o dicionário: {e}")

# ============================
# Aba PINE
# ============================
else:
    st.header("📈 PINE – Atualizar Monitoramento")
    portal_url = st.text_input("Cole o link do portal CKAN:")
    verificar_urls = st.checkbox("Verificar URLs dos recursos?")
    if st.button("Atualizar Planilha"):
        if not portal_url:
            st.error("⚠️ Por favor, informe o link do portal CKAN.")
        else:
            with st.spinner("Atualizando planilha..."):
                try:
                    sucesso, mensagem = atualizar_planilha(portal_url, verificar_urls)
                    if sucesso:
                        st.success(f"✅ {mensagem}")
                    else:
                        st.error(f"❌ {mensagem}")
                except Exception as e:
                    st.error(f"⚠️ Erro ao atualizar a planilha: {e}")

import streamlit as st
import cohere

def get_cohere_response(prompt, api_key):
    try:
        co = cohere.Client(api_key)
        response = co.chat(
            message=prompt,
            model="command",
            temperature=0.3,
            preamble="Você é um especialista em análise de documentos brasileiros"
        )
        return response.text
    except Exception as e:
        return f"Erro na API: {str(e)}"

def main():
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Menu", ["⚙️ Configuração", "📊 Análise"])
    
    if page == "⚙️ Configuração":
        st.header("Configuração do Cohere")
        st.markdown("""
        **Guia de Configuração:**
        1. Crie uma conta no [Cohere](https://cohere.com)
        2. Obtenha sua API Key [aqui](https://dashboard.cohere.com/api-keys)
        3. Cole a chave abaixo:
        """)
        
        api_key = st.text_input("Chave API Cohere:", type="password")
        if api_key:
            st.session_state.cohere_api_key = api_key
            st.success("Chave configurada com sucesso!")
            
        st.markdown("""
        **Limites do Plano Gratuito:**
        - 100 requisições/dia
        - Até 4.096 tokens por requisição
        """)
        
    elif page == "📊 Análise":
        st.header("Análise de Documentos")
        if 'cohere_api_key' not in st.session_state:
            st.error("Configure sua chave API na página de Configuração!")
            return
            
        user_input = st.text_area("Cole seu texto:", height=300)
        if st.button("Analisar"):
            with st.spinner("Processando..."):
                response = get_cohere_response(
                    f"Analise este documento em português e destaque:\n"
                    f"- Dados importantes\n- Possíveis erros\n- Valores relevantes\n\n{user_input}",
                    st.session_state.cohere_api_key
                )
                st.subheader("Resultado:")
                st.write(response)

if __name__ == "__main__":
    main()

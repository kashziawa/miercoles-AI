import streamlit as st
from groq import Groq
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

st.title("Prototipo de LLM y Análisis de Texto")

api_key = st.sidebar.text_input("Ingrese su API Key de Groq", type="password")

if api_key:
    client = Groq(api_key=api_key)
else:
    st.warning("Por favor, ingrese su API Key de Groq en la barra lateral.")

tab1, tab2, tab3 = st.tabs(["1. Visualización de Tokenización", "2. Similitud de Coseno (Embeddings)", "3. Generación de Texto"])

with tab1:
    st.header("Visualización de Tokenización")
    text_input = st.text_area("Ingrese el texto a analizar:", "Aprenderemos los fundamentos de la inteligencia artificial y el procesamiento del lenguaje natural.")
    
    if st.button("Ejecutar tokenización"):
        words = text_input.split()
        colors = ["#FFD1DC", "#AEC6CF", "#77DD77", "#FDFD96", "#B39EB5", "#FFB347"]
        
        st.subheader("Resultado de la partición")
        html_content = ""
        tokens_info = []
        
        for idx, word in enumerate(words):
            color = colors[idx % len(colors)]
            token_id = hash(word) % 10000
            html_content += f'<span style="background-color: {color}; padding: 3px 6px; margin: 2px; border-radius: 3px; font-weight: bold;">{word}</span> '
            tokens_info.append({"Token": word, "Token ID": token_id})
        
        st.markdown(html_content, unsafe_allow_html=True)
        st.write("---")
        st.dataframe(tokens_info)

with tab2:
    st.header("Cálculo de Similitud de Coseno entre Frases")
    text_a = st.text_input("Frase 1:", "El perro está corriendo alegremente en el parque.")
    text_b = st.text_input("Frase 2:", "El perro de mascota está corriendo al aire libre.")
    
    if st.button("Calcular similitud"):
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        vec_a = embedder.encode([text_a])
        vec_b = embedder.encode([text_b])
        
        sim = cosine_similarity(vec_a, vec_b)[0][0]
        
        st.metric(label="Similitud de Coseno", value=f"{sim:.4f}")
        if sim > 0.7:
            st.success("¡Las dos frases son muy similares semánticamente!")
        else:
            st.info("Las dos frases tienen diferencias en su significado.")

with tab3:
    st.header("Generación de Texto con Modelos de Groq")
    
    model_choice = st.selectbox("Seleccione el modelo:", ["llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"])
    temperature = st.slider("Temperatura (Creatividad):", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Máximo de tokens:", 50, 1000, 300)
    
    prompt = st.text_area("Ingrese el prompt (poesía, consejo, resumen, etc.):", "Escribe un poema corto sobre el futuro de la inteligencia artificial.")
    
    if st.button("Generar texto"):
        if not api_key:
            st.error("Por favor, ingrese su API Key de Groq.")
        else:
            try:
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                generated_text = response.choices[0].message.content
                st.subheader("Resultado generado:")
                st.write(generated_text)
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

import streamlit as st
from PIL import Image
st.set_page_config(page_title="OllamaLangDemo", page_icon="./assets/img/me.webp")

def intro():
    

    st.write("# Bienvenido a OllamaLang")
    
    st.sidebar.success("Selecciona una opción en el menú lateral para comenzar")
    st.markdown(
        """
        ## ¿Por qué creé este proyecto?

        Este proyecto demuestra cómo utilizar **Ollama** y **Langchain** para crear aplicaciones de procesamiento de lenguaje natural. Observé que la mayoría de los tutoriales disponibles en línea utilizan APIs de pago, y no encontré muchos recursos que mostraran cómo implementar estas tecnologías de forma local para ahorrar costos mientras se aprende.

        **👈 Si quieres aprender o probar, ve a la barra de navegación** para continuar con el contenido.

        ### ¿Dónde puedo aprender más?

        - Documentación de [Ollama](https://github.com/ollama/ollama/blob/main/docs/tutorials.md)
        - Documentación de [Langchain](https://python.langchain.com/v0.2/docs/introduction/)
        - Documentación de [ChatOllama](https://python.langchain.com/v0.2/docs/integrations/chat/ollama/)

        ### Si quieres ver más de mis proyectos

        - Mi [GitHub](https://github.com/fernandosilvot)
        - Mi [LinkedIn](https://www.linkedin.com/in/fernando-silvo-t/)
        - Mi [Sitio Web](https://fernandosilvot.github.io/)

        Si te sirvió mi proyecto, dame una estrella en GitHub 🌟 y compártelo por LinkedIn etiquetando me 🧑‍💻. ¡Me ayudaría mucho!
    """
    )
    st.image("./assets/img/me.webp", width=200, caption="Fernando Silva T")


def instalacionesPrevias():
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    
    st.markdown(
        """
            ## ¿Qué necesito previamente?

            Para ejecutar los demos, necesitas tener instalado **Python 3.9** o superior. Si no lo tienes instalado, puedes descargarlo desde [aquí](https://www.python.org/downloads/).

            Además, debes instalar las siguientes librerías:

            ```bash
            pip install streamlit
            pip install langchain
            pip install langchain_community
            ```

            También necesitas tener instalado **Ollama**, que puedes descargar desde [aquí](https://ollama.com/).

            Después de instalar Ollama, debes instalar los modelos de lenguaje. Para los demos, utilicé los modelos **Gemma** y **LLama3**. Descárgalos con el siguiente comando:

            ```bash
            ollama run {modelo a elección (gemma o LLama3)}
            ```

            Una vez que hayas instalado el modelo de lenguaje, debes hacerle un pull con el siguiente comando:

            ```bash
            ollama pull {modelo a elección (gemma o LLama3)}
            ```

            Después de completar estos pasos, ya estarás listo para ejecutar los demos.
        
    """
    )
    
    

def chatMemory():
    from langchain_community.llms import Ollama
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage, AIMessage
    
    st.markdown(f'# {list(page_names_to_funcs.keys())[2]}')
    
    
    modelo = st.selectbox("Modelo", ["gemma", "llama3"])
    
    llm = Ollama(model=modelo)
    
    Nombre_bot = st.text_input("Nombre del Bot", value="Bot")
    
    prompt = f"""."""
    
    prompt_bot = st.text_area("Descripción del Bot", value=prompt)
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    prompt_template = ChatPromptTemplate(
        messages=[
            ("system", prompt_bot),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ]
    )
    
    chain = prompt_template | llm
    
    user_input = st.text_input("Escribe tu pregunta", key="user_input")
    
    if st.button("Enviar"):
        if user_input.lower() == "/adios":
            st.stop()
        else:
            response = chain.invoke(
                {"input": user_input, "chat_history": st.session_state["chat_history"]})
            st.session_state["chat_history"].append(HumanMessage(content=user_input))
            st.session_state["chat_history"].append(AIMessage(content=response))
    
    chat_display = ""
    
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            chat_display += f"🧑‍💻Tu: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            chat_display += f"🤖{Nombre_bot}: {msg.content}\n"
            
    st.text_area("Chat", value=chat_display, height=400, key="chat_area",disabled=True)
        
    


def blogGenerator():
    from langchain_community.chat_models import ChatOllama
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import PromptTemplate

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    
    def obtenerRespuesta(modelo, temperatura, template_idioma, input_tema, numero_palabras, estilo_blog):
        
        llm = ChatOllama(
            model=modelo,
            temperature=temperatura,
            max_new_tokens=2048) # 2048 tokens = 1024 palabras
        
        if template_idioma == "es":
            template = """ Eres un experto en redacción de blogs, necesito que crees un blog, con el siguiente estilo {estilo_blog}, sobre el tema {input_tema} en un máximo de {numero_palabras} palabras, en español."""
        elif template_idioma == "en":
            template = """You are an expert in blog writing, I need you to create a blog, with the following style {estilo_blog}, on the topic {input_tema} in a maximum of {numero_palabras} words, in English."""
        
        prompt = PromptTemplate(
            input_variables=['estilo_blog', 
                             'input_tema', 
                             'numero_palabras'],
            template=template)            
        
        prompt_formateado = prompt.format(estilo_blog=estilo_blog, input_tema=input_tema, numero_palabras=numero_palabras)
        
        chain = llm | StrOutputParser()
        
        response = chain.invoke(prompt_formateado)
        
        return response
    
    st.title("Generador de Blog")
    texto_entrada = st.text_area("Escribe el tema del blog que deseas crear")
    
    col1, col2 = st.columns([1, 2])
    
    with  col1:
        modelo = st.selectbox("Modelo", ["gemma", "llama3"])
    with col2:
        temperatura = st.slider("Temperatura", min_value=0.1, max_value=1.0, value=0.7)
    
    col3, col4, col5 = st.columns([6, 4, 4])
    
    with col3:
        num_palabras = st.number_input("Número de palabras", min_value=50, max_value=1000, value=500)
    
    with col4:
        estilo_blog = st.selectbox("Estilo del blog", ["Formal", "Informal", "Técnico"], index=0)
    
    with col5:
        idioma = st.selectbox("Idioma", ["Español", "Inglés"], index=0)
    
    submit = st.button("Generar Blog")
    
    if submit:
        if not texto_entrada:
            st.error("Por favor, ingresa un tema para el blog")
        elif not num_palabras > 0:
            st.error("Por favor, ingresa un número de palabras válido")
        else:
            if idioma == "Español":
                idioma = "es"
            elif idioma == "Inglés":
                idioma = "en"
                
            with st.spinner("Generando publicación..."):
                st.write(obtenerRespuesta(modelo, temperatura, idioma, texto_entrada, num_palabras, estilo_blog))
    

page_names_to_funcs = {
    "Introducción": intro,
    "Requisitos": instalacionesPrevias,
    "Demo Chat con Memoria": chatMemory,
    "Demo Generador de Blogs": blogGenerator
}

demo_name = st.sidebar.selectbox("Escoge una opción", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
# ChatBot Flask + RAG

Versión del chatbot estilo WhatsApp de clase incorporando arquitectura RAG.

## Flujo
Usuario → Flask → Retriever → contexto recuperado → Generator → respuesta.

## Retriever
`rag/retriever.py` divide la base de conocimiento en fragmentos y usa TF-IDF + similitud coseno para recuperar los fragmentos más relacionados con la pregunta.

## Generator
`rag/generator.py` recibe el contexto recuperado y construye la respuesta usando ese contexto.

## Base de conocimiento
Edita `rag/documents/conocimiento.txt` y reemplaza el contenido de ejemplo por la documentación de TU proyecto. Puedes incluir objetivo, funcionalidades, usuarios, procesos, reglas de negocio, módulos y preguntas frecuentes.

## Instalación
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Abre http://127.0.0.1:5000

## Para explicar al profesor
Cuando el usuario pregunta, Flask recibe la consulta. El Retriever busca los fragmentos más relevantes en la base de conocimiento mediante TF-IDF y similitud coseno. Esos fragmentos forman el contexto. Luego el Generator construye la respuesta a partir de ese contexto.

Nota: esta versión no requiere una API externa. Si el profesor exige que Generation use un LLM, el Generator puede conectarse posteriormente a OpenAI, Gemini u Ollama.

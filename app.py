from flask import Flask, render_template, request, jsonify
from rag.retriever import RAGRetriever
from rag.generator import generate_answer
from datetime import datetime

app = Flask(__name__)
retriever = RAGRetriever('rag/documents/conocimiento.txt')

# Mensaje de bienvenida actualizado con la especialidad del bot
messages = [{
    'sender': 'bot',
    'text': '¡Hola! 👋 Soy un asistente especializado en Inteligencia Artificial, Sistemas y Tecnología. ¿En qué tema tecnológico puedo ayudarte hoy?',
    'time': datetime.now().strftime('%H:%M')
}]

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/api/messages', methods=['GET'])
def get_messages(): 
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def send_message():
    data = request.get_json(silent=True) or {}
    text = str(data.get('text','')).strip()
    
    if not text: 
        return jsonify({'error': 'El mensaje no puede estar vacío.'}), 400
    
    # 1. Registrar mensaje del usuario
    user = {
        'sender': 'user',
        'text': text,
        'time': datetime.now().strftime('%H:%M')
    }
    messages.append(user)
    
    # 2. Recuperar contexto relevante
    context = retriever.retrieve(text, top_k=3)
    
    # 3. Generar la respuesta evaluando si está dentro del dominio permitido
    reply = generate_answer(text, context)
    
    # 4. Registrar respuesta del bot
    bot = {
        'sender': 'bot',
        'text': reply,
        'time': datetime.now().strftime('%H:%M')
    }
    messages.append(bot)
    
    return jsonify({'user': user, 'bot': bot, 'rag': {'sources_used': len(context)}})

@app.route('/api/messages', methods=['DELETE'])
def clear_messages():
    messages.clear()
    messages.append({
        'sender': 'bot',
        'text': 'Chat limpiado. ¡Pregúntame cualquier duda sobre IA, Sistemas o Tecnología! 💻✨',
        'time': datetime.now().strftime('%H:%M')
    })
    return jsonify({'ok': True})

if __name__ == '__main__': 
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify, send_from_directory
import speech_recognition as sr
import time

r = sr.Recognizer()
escutando = True

comando = "" 
nome = ""     
sobrenome = ""
idade = "" 

# Função para ouvir e processar o áudio
def ouvir_comando():
    global escutando
    with sr.Microphone() as source:
        print("Ouvindo...")
        while escutando:
            try:
                audio = r.listen(source)
                # Converte o áudio em texto
                comando = r.recognize_google(audio, language='pt-BR')
                print(f"Comando recebido: {comando}")
                return comando.lower()
            except sr.UnknownValueError:
                print("Não foi possível entender o áudio.")
                return ""
            except sr.RequestError as e:
                print(f"Erro na requisição de reconhecimento de fala: {e}")
                return ""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ComandoDeVoz.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/reconhecer', methods=['POST'])
def reconhecer():
    global escutando, comando, nome, sobrenome, idade
    comando = ouvir_comando()

    if comando == "parar":
        escutando = False

    if comando == "preencher campo nome":
        mostrar_mensagem("Aguardando valor para o campo Nome...")
        time.sleep(0.5)
        nome = ouvir_comando()
    elif comando == "preencher campo sobrenome":
        mostrar_mensagem("Aguardando valor para o campo Sobrenome...")
        time.sleep(0.5)
        sobrenome = ouvir_comando()
    elif comando == "preencher campo idade":
        mostrar_mensagem("Aguardando valor para o campo Idade...")
        time.sleep(0.5)
        idade = ouvir_comando()

    return jsonify({'comando': comando, 'nome': nome, 'sobrenome': sobrenome, 'idade': idade})

#
def mostrar_mensagem(mensagem):
    print(mensagem)

if __name__ == '__main__':
    app.run(debug=True)

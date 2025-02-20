import os
import json
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)
CORS(app)

# Rutas de los archivos JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTADOS_FILE = os.path.join(BASE_DIR, 'resultados.json')
ESTUDIANTES_FILE = os.path.join(BASE_DIR, 'estudiantes.json')
BINGO_ESTUDIANTES_FILE = os.path.join(BASE_DIR, 'bingo_estudiantes.json')

# Variables de la ruleta
VARIABLES_RULETA = [
    "Mindfullness", "Pensamiento Productivo", "Visualización", "Cambio de creencias",
    "Cambio de postura", "Respiración consciente", "Técnica de relajación", "Hábitos emocionalmente saludables",
    "Cambio de actividad", "Emoción", "Sentimiento", "Estado de ánimo", "Phineas Gage", "Sonrisa Social",
    "Sonrisa auténtica", "Marc Brackett", "Dicha", "Consuelo", "Optimismo", "Bienestar", "Amargura",
    "Decepción", "Nostalgia", "Resentimiento", "Frustración", "Furia", "Desprecio", "Aversión",
    "Discriminación", "Igualdad", "Equidad", "Curiosidad", "Admiración", "Pasmo", "Temor", "Malestar",
    "Satisfacción", "Estrés", "Arrepentimiento", "Culpa"
]

# Respuestas correctas
RESPUESTAS_TABLA = [
    "Atención plena al presente", "Cambiar diálogo negativo por uno productivo",
    "Técnica para mejorar el ánimo, imaginando escenarios agradables",
    "Técnicas para transformar creencias limitantes en positivas y constructivas",
    "Tomar consciencia de nuestra posición y adoptarlas para potenciar emociones",
    "Controlar reacciones con relajación y respiración consciente",
    "Formas de relajar el cuerpo y liberar endorfinas",
    "Hábitos que fomentan un estado de ánimo positivo, como leer, escribir o dibujar",
    "Identificar si lo que estamos haciendo nos perjudica y dejar de realizarlo",
    "Respuesta automática e intensa a un estímulo externo o interno.",
    "Interpretación consciente y duradera de una emoción",
    "Disposición emocional difusa y prolongada en el tiempo",
    "Caso que demostró la importancia de la corteza prefrontal",
    "Tensión en los párpados inferiores, pero no consiguen elevar la piel",
    "Expresión relajada, se muestran los dientes superiores y la expresión facial es de felicidad",
    "Hay que dar permiso al mundo a sentir",
    "Felicidad, suerte, estado del ánimo que se complace en la posesión de un bien",
    "Alivio que siente una persona de una pena, dolor o disgusto",
    "Tendencia de ver y juzgar las cosas considerando su aspecto más favorable",
    "Estado o situación de satisfacción o felicidad",
    "Sentimiento de pena, aflicción o disgusto",
    "Frustración que se da al desengañarse de lo que no satisface nuestras expectativas",
    "Tristeza melancólica por el recuerdo de un bien perdido",
    "Enojo o enfado por algo, especialmente con los causantes",
    "Fracaso en un deseo",
    "Ira exaltada contra algo o alguien, persona muy irritada",
    "Falta de estima por algo o alguien, desestimación o desaire",
    "Asco frente a algo o a alguien",
    "Ideología que considera inferiores a personas por su raza, clase social, etc.",
    "Principio que establece que todas las personas tienen los mismos derechos",
    "Igualdad de ánimo (se cree que es sinónimo de igualdad)",
    "Deseo e interés por conocer lo que no se sabe",
    "Consideración especial hacia algo o alguien por sus cualidades",
    "Paralización que surge del asombro extremo",
    "Sentimiento de inquietud y miedo que provoca la necesidad de huir",
    "Sensación de incomodidad",
    "Cumplimiento de una necesidad, un deseo, una pasión",
    "Alteración física y mental por exigirse un rendimiento superior al normal",
    "Pesar que se siente por haber hecho alguna cosa",
    "Mezcla de ira y de tristeza que aparece cuando omitimos responsabilidades"
]


# Funciones de reinicio
def reiniciar_archivo(file_path, default_value=[]):
    """Crea o vacía un archivo JSON con valores por defecto."""
    with open(file_path, 'w') as f:
        json.dump(default_value, f, indent=4)

@app.route('/ruleta')
def ruleta():
    """Carga la ruleta y reinicia los datos del juego"""
    reiniciar_archivo(RESULTADOS_FILE)
    reiniciar_archivo(ESTUDIANTES_FILE)
    reiniciar_archivo(BINGO_ESTUDIANTES_FILE, {})
    return render_template('ruleta.html', variables_ruleta=VARIABLES_RULETA)

@app.route('/estudiante')
def estudiante():
    """Carga la vista del bingo del estudiante"""
    return render_template('estudiante.html', respuestas_tabla=RESPUESTAS_TABLA)

@app.route('/girar', methods=['POST'])
def girar_ruleta():
    """Selecciona una variable aleatoria y la guarda en resultados.json"""
    variable = random.choice(VARIABLES_RULETA)
    with open(RESULTADOS_FILE, 'r') as f:
        data = json.load(f)
    data.append(variable)
    reiniciar_archivo(RESULTADOS_FILE, data)
    return jsonify({'variable': variable})

@app.route('/registrar-estudiante', methods=['POST'])
def registrar_estudiante():
    """Registra un nuevo estudiante en la lista de espera"""
    data = request.get_json()
    nombre = data.get('estudiante')

    if not nombre:
        return jsonify({'message': 'Nombre de estudiante requerido'}), 400

    estudiantes = []
    if os.path.exists(ESTUDIANTES_FILE):
        with open(ESTUDIANTES_FILE, 'r') as f:
            estudiantes = json.load(f)

    if any(est['nombre'] == nombre for est in estudiantes):
        return jsonify({'message': 'Estudiante ya registrado'}), 400

    estudiantes.append({'nombre': nombre, 'aceptado': False, 'puntaje': 0})
    reiniciar_archivo(ESTUDIANTES_FILE, estudiantes)

    return jsonify({'message': 'Estudiante registrado exitosamente'})

@app.route('/obtener-estudiantes', methods=['GET'])
def obtener_estudiantes():
    """Devuelve la lista de estudiantes en espera"""
    if not os.path.exists(ESTUDIANTES_FILE):
        return jsonify({'estudiantes': []})

    with open(ESTUDIANTES_FILE, 'r') as f:
        estudiantes = json.load(f)

    return jsonify({'estudiantes': estudiantes})

@app.route('/aceptar-estudiante', methods=['POST'])
def aceptar_estudiante():
    """Acepta a un estudiante para que pueda jugar"""
    data = request.get_json()
    nombre = data.get('estudiante')

    if not nombre:
        return jsonify({'message': 'Nombre de estudiante requerido'}), 400

    with open(ESTUDIANTES_FILE, 'r') as f:
        estudiantes = json.load(f)

    for est in estudiantes:
        if est['nombre'] == nombre:
            est['aceptado'] = True
            break

    reiniciar_archivo(ESTUDIANTES_FILE, estudiantes)
    return jsonify({'message': f'Estudiante {nombre} aceptado'})

@app.route('/obtener-marcador', methods=['GET'])
def obtener_marcador():
    """Devuelve la lista de estudiantes con su estado y puntaje"""
    if not os.path.exists(ESTUDIANTES_FILE):
        return jsonify({'jugadores': []})

    with open(ESTUDIANTES_FILE, 'r') as f:
        estudiantes = json.load(f)

    jugadores = [{'nombre': est['nombre'], 'puntaje': est.get('puntaje', 0)} for est in estudiantes if est['aceptado']]
    return jsonify({'jugadores': jugadores})

@app.route('/validar-respuesta', methods=['POST'])
def validar_respuesta():
    """Verifica si la respuesta seleccionada es correcta"""
    data = request.get_json()
    respuesta = data.get('respuesta')

    if not respuesta:
        return jsonify({'message': 'Respuesta requerida'}), 400

    es_correcta = respuesta in RESPUESTAS_TABLA
    return jsonify({'correcta': es_correcta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

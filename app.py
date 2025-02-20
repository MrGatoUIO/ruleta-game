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

@app.route('/resultados', methods=['GET'])
def json_resultados():
    """Devuelve el contenido de resultados.json"""
    if not os.path.exists(RESULTADOS_FILE):
        return jsonify({'message': 'El archivo no existe'}), 404

    with open(RESULTADOS_FILE, 'r') as f:
        data = json.load(f)

    return jsonify(data)

@app.route('/estudiantes', methods=['GET'])
def json_estudiantes():
    """Devuelve el contenido de estudiantes.json"""
    if not os.path.exists(ESTUDIANTES_FILE):
        return jsonify({'message': 'El archivo no existe'}), 404

    with open(ESTUDIANTES_FILE, 'r') as f:
        data = json.load(f)

    return jsonify(data)

@app.route('/bingo_estudiantes', methods=['GET'])
def json_bingo_estudiantes():
    """Devuelve el contenido de bingo_estudiantes.json"""
    if not os.path.exists(BINGO_ESTUDIANTES_FILE):
        return jsonify({'message': 'El archivo no existe'}), 404

    with open(BINGO_ESTUDIANTES_FILE, 'r') as f:
        data = json.load(f)

    return jsonify(data)

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

def guardar_tarjeta_estudiante(nombre, opciones):
    """Guarda la tarjeta generada para un estudiante específico."""
    estudiantes_tarjetas = {}

    if os.path.exists(BINGO_ESTUDIANTES_FILE):
        with open(BINGO_ESTUDIANTES_FILE, 'r') as f:
            estudiantes_tarjetas = json.load(f)

    estudiantes_tarjetas[nombre] = opciones

    with open(BINGO_ESTUDIANTES_FILE, 'w') as f:
        json.dump(estudiantes_tarjetas, f, indent=4)

@app.route('/obtener-tarjeta', methods=['POST'])
def obtener_tarjeta():
    """Devuelve la tarjeta asignada a un estudiante o la genera si no existe."""
    data = request.get_json()
    nombre = data.get('estudiante')

    if not nombre:
        return jsonify({'message': 'Nombre de estudiante requerido'}), 400

    estudiantes_tarjetas = {}
    if os.path.exists(BINGO_ESTUDIANTES_FILE):
        with open(BINGO_ESTUDIANTES_FILE, 'r') as f:
            estudiantes_tarjetas = json.load(f)

    if nombre in estudiantes_tarjetas:
        return jsonify({'tarjeta': estudiantes_tarjetas[nombre]})

    # Generar nueva tarjeta si no existe
    tarjeta = random.sample(RESPUESTAS_TABLA, 15)
    guardar_tarjeta_estudiante(nombre, tarjeta)

    return jsonify({'tarjeta': tarjeta})

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
    """Verifica si la respuesta seleccionada es correcta con base en la ruleta"""
    data = request.get_json()
    respuesta = data.get('respuesta')

    if not respuesta:
        return jsonify({'message': 'Respuesta requerida'}), 400

    # Cargar las variables que ya salieron en la ruleta
    if not os.path.exists(RESULTADOS_FILE):
        return jsonify({'message': 'No hay resultados en la ruleta'}), 400

    with open(RESULTADOS_FILE, 'r') as f:
        variables_salidas = json.load(f)  # Lista de las variables que ya salieron en la ruleta

    # Verificar si la respuesta corresponde con alguna variable ya salida
    for variable in variables_salidas:
        if variable in VARIABLES_RULETA:
            index = VARIABLES_RULETA.index(variable)  # Encontramos el índice de la variable en la lista
            respuesta_correcta = RESPUESTAS_TABLA[index]  # Obtenemos la respuesta correcta
            if respuesta == respuesta_correcta:
                return jsonify({'correcta': True}), 200

    return jsonify({'correcta': False}), 200

@app.route('/validar-ganador', methods=['POST'])
def validar_ganador():
    """Cuenta cuántas respuestas correctas tiene el estudiante y actualiza su puntaje"""
    data = request.get_json()
    nombre = data.get('estudiante')
    respuestas_seleccionadas = set(data.get('respuestas', []))

    if not nombre or not respuestas_seleccionadas:
        return jsonify({'message': 'Nombre del estudiante y respuestas requeridas'}), 400

    # Cargar las variables que ya salieron en la ruleta
    if not os.path.exists(RESULTADOS_FILE):
        return jsonify({'message': 'No hay resultados en la ruleta'}), 400

    with open(RESULTADOS_FILE, 'r') as f:
        variables_salidas = set(json.load(f))  # Set de variables que han salido en la ruleta

    # Obtener respuestas correctas basadas en las variables ya salidas
    respuestas_correctas = {RESPUESTAS_TABLA[VARIABLES_RULETA.index(var)] for var in variables_salidas if var in VARIABLES_RULETA}

    # Contar cuántas respuestas seleccionadas son correctas
    correctas = len(respuestas_seleccionadas & respuestas_correctas)

    # Actualizar puntaje en el archivo de estudiantes
    if os.path.exists(ESTUDIANTES_FILE):
        with open(ESTUDIANTES_FILE, 'r') as f:
            estudiantes = json.load(f)

        for est in estudiantes:
            if est['nombre'] == nombre:
                est['puntaje'] = correctas  # Guardamos el puntaje actualizado
                break

        with open(ESTUDIANTES_FILE, 'w') as f:
            json.dump(estudiantes, f, indent=4)
        ganador = correctas == 15  # Esto devuelve True si correctas == 15, de lo contrario False

    return jsonify({
        'message': f'{nombre} tiene {correctas} respuestas correctas',
        'correctas': correctas,
        'ganador': ganador  # Devolvemos si ganó o no
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

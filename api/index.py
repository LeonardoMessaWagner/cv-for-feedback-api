from flask import Flask, jsonify, render_template
from coleta_e_grafico import coletar_e_gerar_grafico

app = Flask(__name__)

@app.route('/coletar_e_grafico', methods=['GET'])
def coletar_e_grafico_route():
    gráfico_base64 = coletar_e_gerar_grafico()
    return jsonify({'gráfico_base64': gráfico_base64})


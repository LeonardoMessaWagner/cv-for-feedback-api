# coleta_e_grafico.py
import cv2
import mediapipe as mp
from fer import FER
import matplotlib.pyplot as plt
import io
import base64
import time

def coletar_e_gerar_grafico():
    detector = FER()
    mp_face_mesh = mp.solutions.face_mesh
    facemesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    captura = cv2.VideoCapture(0)

    emocoes_por_segundo = []
    tempo_inicio = time.time()
    duracao = 6 #sempre 1 segundo para mais
    ultimo_segundo = 0
    
    while True:
        tempo_atual = time.time()
        segundos_passados = int(tempo_atual - tempo_inicio)
        
        if segundos_passados >= duracao:
            break
        
        sucesso, frame = captura.read()
        if not sucesso:
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        saida_facemesh = facemesh.process(frame_rgb)
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        resultados_emocao = detector.detect_emotions(frame_bgr)
        
        if segundos_passados > ultimo_segundo:
            if resultados_emocao:
                resultado = resultados_emocao[0]
                emocao, pontuacao = max(resultado['emotions'].items(), key=lambda item: item[1])
                emocoes_por_segundo.append({'segundo': segundos_passados, 'emocao': emocao})
            ultimo_segundo = segundos_passados
    
    captura.release()
    
    gráfico_base64 = gerar_grafico(emocoes_por_segundo)
    
    return gráfico_base64

def gerar_grafico(emocoes):
    segundos = [emo['segundo'] for emo in emocoes]
    emoções = [emo['emocao'] for emo in emocoes]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(segundos, emoções, marker='D')
    plt.xlabel('Segundos')
    plt.ylabel('Emoções')
    plt.title('Emoções Coletadas ao Longo do Tempo')
    plt.grid(True)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    gráfico_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return gráfico_base64

import speech_recognition as sr
import os
import wave
import contextlib
import pydub
from pydub import AudioSegment
import math

def dividir_audio(caminho_arquivo, duracao_parte=300):
    try:
        # Carrega o arquivo de áudio
        audio = AudioSegment.from_wav(caminho_arquivo)
        
        # Converte para mono e 16kHz
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        # Calcula o número de partes
        duracao_total = len(audio) / 1000  # em segundos
        num_partes = math.ceil(duracao_total / duracao_parte)
        
        partes = []
        for i in range(num_partes):
            inicio = i * duracao_parte * 1000
            fim = min((i + 1) * duracao_parte * 1000, len(audio))
            
            parte = audio[inicio:fim]
            caminho_parte = f"{os.path.splitext(caminho_arquivo)[0]}_parte_{i+1}.wav"
            parte.export(caminho_parte, format="wav")
            partes.append(caminho_parte)
        
        return partes
    except Exception as e:
        print(f"Erro ao dividir o áudio: {str(e)}")
        return None

def transcrever_audio(caminho_arquivo):
    # Inicializa o reconhecedor
    reconhecedor = sr.Recognizer()
    
    try:
        # Carrega o arquivo de áudio
        with sr.AudioFile(caminho_arquivo) as fonte:
            # Ajusta para o ruído ambiente
            reconhecedor.adjust_for_ambient_noise(fonte)
            # Obtém o áudio do arquivo
            audio = reconhecedor.record(fonte)
            
            # Tenta transcrever o áudio usando diferentes serviços
            try:
                texto = reconhecedor.recognize_google(audio, language='pt-BR')
            except:
                try:
                    texto = reconhecedor.recognize_whisper(audio, language='portuguese')
                except:
                    texto = reconhecedor.recognize_sphinx(audio, language='pt-BR')
            
            return texto
            
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio"
    except sr.RequestError as e:
        return f"Erro ao acessar o serviço de reconhecimento: {str(e)}\nVerifique sua conexão com a internet."
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"

def main():
    print("=== Transcrição de Áudio ===")
    print("Digite o caminho completo do arquivo de áudio (formato WAV):")
    caminho_arquivo = input().strip()
    
    if not os.path.exists(caminho_arquivo):
        print("Arquivo não encontrado!")
        return
    
    # Verifica o formato do arquivo
    try:
        with contextlib.closing(wave.open(caminho_arquivo, 'rb')) as f:
            frames = f.getnframes()
            taxa = f.getframerate()
            duracao = frames / float(taxa)
            canais = f.getnchannels()
            bits = f.getsampwidth() * 8
            
            print(f"\nInformações do arquivo:")
            print(f"Taxa de amostragem: {taxa} Hz")
            print(f"Canais: {canais}")
            print(f"Bits por amostra: {bits}")
            print(f"Duração: {duracao:.2f} segundos")
            
            if duracao > 300:  # Se o arquivo for maior que 5 minutos
                print("\nO arquivo é muito grande. Dividindo em partes menores...")
                partes = dividir_audio(caminho_arquivo)
                if partes:
                    texto_completo = ""
                    for i, parte in enumerate(partes):
                        print(f"\nTranscrevendo parte {i+1} de {len(partes)}...")
                        texto = transcrever_audio(parte)
                        texto_completo += texto + "\n"
                        # Remove o arquivo temporário
                        os.remove(parte)
                    
                    print("\nTranscrição completa:")
                    print(texto_completo)
                    
                    # Salva a transcrição em um arquivo
                    nome_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]
                    with open(f"{nome_arquivo}_transcricao.txt", "w", encoding="utf-8") as arquivo:
                        arquivo.write(texto_completo)
                    
                    print(f"\nTranscrição salva em: {nome_arquivo}_transcricao.txt")
                    return
    except Exception as e:
        print(f"\nErro ao verificar o arquivo: {str(e)}")
        return
    
    # Se o arquivo for pequeno, transcreve normalmente
    print("\nTranscrevendo...")
    texto = transcrever_audio(caminho_arquivo)
    
    print("\nTranscrição:")
    print(texto)
    
    # Salva a transcrição em um arquivo
    nome_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]
    with open(f"{nome_arquivo}_transcricao.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)
    
    print(f"\nTranscrição salva em: {nome_arquivo}_transcricao.txt")

if __name__ == "__main__":
    main() 
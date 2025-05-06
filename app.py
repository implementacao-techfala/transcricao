import streamlit as st
import os
from transcriber import transcrever_audio, dividir_audio
import tempfile
import wave
import contextlib

st.set_page_config(
    page_title="Transcrição de Áudio",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Transcrição de Áudio")

st.write("""
Esta aplicação permite fazer upload de arquivos de áudio WAV e gerar uma transcrição do conteúdo.
""")

# Upload do arquivo de áudio
uploaded_file = st.file_uploader("Escolha um arquivo de áudio WAV", type=['wav'])

if uploaded_file is not None:
    # Criar um arquivo temporário para salvar o áudio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Verificar a duração do arquivo
    try:
        with contextlib.closing(wave.open(tmp_file_path, 'rb')) as f:
            frames = f.getnframes()
            taxa = f.getframerate()
            duracao = frames / float(taxa)
            
            st.info(f"""
            Informações do arquivo:
            - Taxa de amostragem: {taxa} Hz
            - Duração: {duracao:.2f} segundos
            """)
            
            # Se o arquivo for maior que 5 minutos (300 segundos), dividir em partes
            if duracao > 300:
                st.warning("O arquivo é muito grande. Será dividido em partes menores para transcrição.")
    except Exception as e:
        st.error(f"Erro ao verificar o arquivo: {str(e)}")

    # Botão para iniciar a transcrição
    if st.button("Iniciar Transcrição"):
        with st.spinner("Transcrevendo o áudio... Isso pode levar alguns minutos."):
            try:
                # Verificar se precisa dividir o áudio
                with contextlib.closing(wave.open(tmp_file_path, 'rb')) as f:
                    frames = f.getnframes()
                    taxa = f.getframerate()
                    duracao = frames / float(taxa)
                
                if duracao > 300:
                    # Dividir o áudio em partes
                    partes = dividir_audio(tmp_file_path)
                    if not partes:
                        st.error("Erro ao dividir o áudio em partes.")
                    else:
                        texto_completo = ""
                        progress_bar = st.progress(0)
                        for i, parte in enumerate(partes):
                            st.text(f"Transcrevendo parte {i+1} de {len(partes)}...")
                            texto = transcrever_audio(parte)
                            texto_completo += texto + "\n"
                            # Atualizar a barra de progresso
                            progress_bar.progress((i + 1) / len(partes))
                            # Remover o arquivo temporário da parte
                            os.remove(parte)
                        
                        transcription = texto_completo
                else:
                    # Transcrever normalmente se o arquivo for pequeno
                    transcription = transcrever_audio(tmp_file_path)
                
                # Exibir a transcrição
                st.text_area("Transcrição:", transcription, height=300)
                
                # Botão para download da transcrição
                st.download_button(
                    label="Baixar Transcrição",
                    data=transcription,
                    file_name="transcricao.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Ocorreu um erro durante a transcrição: {str(e)}")
            finally:
                # Limpar o arquivo temporário
                os.unlink(tmp_file_path)

st.markdown("---")
st.markdown("Desenvolvido com ❤️ usando Streamlit") 
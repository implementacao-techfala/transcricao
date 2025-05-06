# Transcrição de Áudio

Este é um programa simples para transcrever arquivos de áudio para texto.

## Requisitos

- Python 3.6 ou superior
- Conexão com a internet (para usar o serviço de reconhecimento do Google)

## Instalação

1. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

2. Para instalar o PyAudio no Windows, você pode precisar baixar o instalador apropriado do site oficial ou usar:
```bash
pip install pipwin
pipwin install pyaudio
```

## Como usar

1. Execute o programa:
```bash
python transcriber.py
```

2. Digite o caminho completo do arquivo de áudio que deseja transcrever (formato WAV)
3. O programa irá transcrever o áudio e salvar o resultado em um arquivo de texto com o mesmo nome do arquivo de áudio, adicionando "_transcricao.txt" ao final

## Observações

- O programa suporta apenas arquivos no formato WAV
- A transcrição é feita usando o serviço de reconhecimento de fala do Google
- O programa está configurado para reconhecer português do Brasil 
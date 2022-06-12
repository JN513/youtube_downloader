# Youtube_downloader
  
![Imagem da jánela](https://github.com/JN513/youtube_downloader/blob/create_pages/window.png) 

Software para download de videos e musicas do Youtube feito com Python, PyQt5 e Pytube.

## Requisitos

Para utilizar o programa sera necessesario ter instado:

* Versão 3.0 ou superior do **[Python](https://www.python.org/)** (testei na 3.8 e 3.10);
* **[Python-pip](https://pt.stackoverflow.com/questions/239047/como-instalar-o-pip-no-windows-10)**.
* FFMPEG (**[FFmpeg](https://www.ffmpeg.org/)**) para converter os videos para mp3.

## Instalação

Para instalar todas as Bibliotecas, basta instalar usando o arquivo requirements.txt, com o seguinte comando:
``` pip install -r requirements.txt ```

Para instalar o ffmpeg no linux utilize:
- para distros baseadas em debian ou ubuntu ``` sudo apt-get install ffmpeg ```
- para distros baseadas em arch ``` sudo pacman -Syu ffmpeg ```
- para distros baseadas em fedora ou centos ``` sudo dnf install ffmpeg ```

Para instalar o ffmpeg no MACOSX utilize:
``` brew install ffmpeg ```

Para instalar o ffmpeg no windows utilize:
``` https://www.ffmpeg.org/download.html ```

## Utilização

Após a instalação das dependencias utilize:
``` python3 main.py ```
Para rodar o programa.

## Duvidas e Bugs

Em caso de alguma duvida, bug na aplicação ou sujestão, utilize o menu issues do github.

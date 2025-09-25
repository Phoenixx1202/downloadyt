Passo 1: Instalar o Python

O Python é a linguagem de programação que usamos para escrever nosso aplicativo. Se você ainda não o tem, a instalação é muito simples.

Acesse o Site Oficial: Abra seu navegador e vá para python.org. O site geralmente já detecta que você está no Windows e sugere a versão mais recente.

Baixe o Instalador: Clique no botão para baixar a versão mais recente do Python.

Execute a Instalação

Abra o arquivo que você baixou.

Na primeira tela da instalação, marque a caixinha que diz "Add python.exe to PATH". Isso é MUITO importante para que possamos usar os comandos python e pip diretamente no terminal.

Depois de marcar a caixa, pode clicar em "Install Now".

Verificação: Para confirmar que tudo deu certo, abra o menu Iniciar, digite cmd ou PowerShell e, no terminal que abrir, digite o comando abaixo e aperte Enter:

```bash
python --version
```

Se aparecer a versão do Python que você instalou (ex: Python 3.12.4), parabéns, o primeiro passo está concluído!

Passo 2: Instalar a Biblioteca yt-dlp

Nosso código importa a biblioteca yt-dlp, que é a ferramenta que faz todo o trabalho pesado de buscar e baixar os vídeos do YouTube. Vamos instalá-la usando o pip, o gerenciador de pacotes do Python.

Abra o Terminal: Se você fechou, abra o cmd ou PowerShell novamente.

Execute o Comando de Instalação: Digite o comando a seguir e pressione Enter.


```bash
pip install yt-dlp
```

O pip vai se conectar à internet, baixar a biblioteca yt-dlp e todas as suas dependências e instalá-las para você.

Verificação: Para ter certeza de que a biblioteca foi instalada, você pode usar o comando:


```bash
pip show yt-dlp
```

Ele deve mostrar os detalhes da biblioteca, como a versão instalada.

Passo 3: Instalar o FFmpeg

Você já tentou baixar um vídeo em 1080p do YouTube e percebeu que o vídeo e o áudio vêm em arquivos separados? E como nosso app converte vídeos para MP3? É aqui que o FFmpeg entra!

Ele é uma ferramenta poderosa que o yt-dlp usa para:

Juntar (merge): Unir os arquivos de vídeo e áudio em um único MP4 ou MKV.

Converter: Extrair o áudio de um vídeo e salvá-lo como MP3.

Sem o FFmpeg, o download de vídeos em alta qualidade e a conversão para MP3 não funcionarão!

Baixe o FFmpeg:

Vá para o site: https://www.gyan.dev/ffmpeg/builds/

Role a página até a seção "release builds".

Clique no arquivo ffmpeg-release-full.7z para baixar. (Você precisará de um programa como o 7-Zip ou WinRAR para descompactar).

Descompacte e Organize:

Descompacte o arquivo que você baixou.

Dentro, você verá uma pasta com um nome como ffmpeg-7.0-full_build. 

Renomeie essa pasta para algo simples, como FFmpeg.

Mova essa pasta FFmpeg para um local fácil de acessar, como a raiz do seu disco C:\. O caminho final da pasta deve ser C:\FFmpeg.

Adicione o FFmpeg ao PATH do Windows:

Assim como fizemos com o Python, precisamos dizer ao Windows onde encontrar o FFmpeg.

Pressione a tecla Windows, digite "variáveis de ambiente" e clique em "Editar as variáveis de ambiente do sistema".

Clique no botão "Variáveis de Ambiente...".

Na seção "Variáveis do Sistema", encontre e selecione a variável Path e clique em "Editar...".

Clique em "Novo" e cole o caminho para a pasta bin dentro da sua pasta FFmpeg. Se você seguiu meu exemplo, o caminho é:

C:\FFmpeg\bin
Clique "OK" em todas as janelas para salvar.

Verificação Final:

Abra um NOVO terminal (é importante abrir um novo para que ele carregue as novas configurações do PATH).

Digite o comando:

```bash
ffmpeg -version
```

Se aparecerem informações sobre a versão do FFmpeg, tudo está pronto!

Passo 4: Como Transformar seu App em um Programa (.EXE)

A. Instalando o PyInstaller

Abra seu terminal (cmd ou PowerShell).

Instale o PyInstaller com um simples comando pip:

```bash
pip install pyinstaller
```

B. Convertendo o Script

Pelo terminal, navegue até a pasta onde está o seu script Python (ex: downloader_app.py). Use o comando cd seu\caminho\para\a\pasta.

Agora, execute o comando principal do PyInstaller. Temos algumas opções úteis:

--onefile: Cria um único arquivo .exe, em vez de uma pasta cheia de arquivos. É o mais prático!

--windowed ou -w: Impede que aquela janela de console preta apareça por trás da sua interface gráfica. Essencial para apps com janela.

--icon="caminho/para/seu/icone.ico": Permite que você defina um ícone personalizado para o seu programa. Você precisa ter um arquivo de imagem no formato .ico.

Juntando tudo, o comando fica assim:

```bash
pyinstaller --onefile --windowed --icon="youtube.ico" downloader_app.py
```

(Lembre-se de substituir "youtube.ico" pelo nome do seu arquivo de ícone, ou remova a opção --icon se não tiver um).

C. Encontrando seu Programa

O PyInstaller vai trabalhar por um tempo e criar algumas pastas. Ao final, você encontrará seu programa pronto para uso dentro da pasta chamada dist.

É só entrar na pasta dist e seu arquivo downloader_app.exe estará lá!








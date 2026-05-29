# IMPORTE A BIBLIOTECA: pytz, tzlocal, PyYAML, requests, num2words

import time, os,random,re,requests,sys,yaml
from enum import Enum
from num2words import num2words
from colorama import Back, Fore, Style
from pathlib import Path

from tkinter import filedialog, Tk, messagebox;
from tzlocal import get_localzone
from datetime import datetime
from pytz import timezone
from dotenv import set_key, dotenv_values

class Style_Extra:
    ITALICO = "\033[3m"

atencaoAtual = 4
print(atencaoAtual * 0.8)

def DataAtual(formatar=False):
    try:
        fh = get_localzone()
        dataHora = datetime.now(fh)
        return dataHora.strftime('%d/%m/%Y') if formatar else dataHora
    except:
        return None

def FusoHorario(formatar=True):
    try:
        fh = get_localzone()
        dataHora = datetime.now(fh)
        horaFormatada = dataHora.strftime('%H:%M:%S')
        if(not formatar):
            return horaFormatada.split(':')
        return horaFormatada
    except:
        return None

def MensagemDeConsole(mensagem, tipo=0,titulo=""):
    corMensagem = ['\033[0m', '\033[0m']
    tipoMensagem = ''
    match tipo:
        case 0: 
            corMensagem[0] = Fore.GREEN
            corMensagem[1] = Back.GREEN
            tipoMensagem = 'SUCESSO'
        case 1:
            corMensagem[0] = Fore.YELLOW
            corMensagem[1] = Back.YELLOW
            tipoMensagem = 'AVISO'
        case 2:
            corMensagem[0] = Fore.RED
            corMensagem[1] = Back.RED
            tipoMensagem = 'FALHA'
        case 3:
            corMensagem[0] = Fore.WHITE
            corMensagem[1] = Back.BLACK
            tipoMensagem = 'INFO'

    titulo = f"{corMensagem[1]}{Style.BRIGHT}[{titulo}]{Style.RESET_ALL}: " if len(titulo) > 0 else ""
    rotulo = f"{corMensagem[0]}{Style.BRIGHT}{tipoMensagem} > {Style.RESET_ALL}" if len(tipoMensagem) > 0 else ""
    mensagem = f"{corMensagem[0]}'{Style_Extra.ITALICO}{mensagem}{corMensagem[0]}{Style_Extra.ITALICO}'{Style.RESET_ALL}"

    print(f"{titulo}{rotulo}{mensagem.strip()}{Style.RESET_ALL}\n")
    
class tipoDeMensagem(Enum):
    INFO = 1
    SUCESSO = 2
    AVISO = 3
    FALHA = 4

def MensagemDeConsolePro(mensagem, tipo=tipoDeMensagem.SUCESSO,titulo="CONSOLE",horario=False,prefixoRotulo="",prefixoMensagem=""):
    corMensagem = ['\033[0m', '\033[0m']
    tipoMensagem = ''
    match tipo:
        case _ if tipo == tipoDeMensagem.SUCESSO or tipo == 0:
            corMensagem[0] = Fore.GREEN
            corMensagem[1] = Back.GREEN
            tipoMensagem = 'SUCESSO'
        case _ if tipo == tipoDeMensagem.AVISO or tipo == 1:
            corMensagem[0] = Fore.YELLOW
            corMensagem[1] = Back.YELLOW
            tipoMensagem = 'AVISO'
        case _ if tipo == tipoDeMensagem.FALHA or tipo ==  2:
            corMensagem[0] = Fore.RED
            corMensagem[1] = Back.RED
            tipoMensagem = 'FALHA'
        case _ if tipo == tipoDeMensagem.INFO or tipo == 3:
            corMensagem[0] = Fore.WHITE
            corMensagem[1] = Back.BLACK
            tipoMensagem = 'INFO'

    horarioAtual = f"{Style.BRIGHT}{FusoHorario().split(':')[0]}:{FusoHorario().split(':')[1]}{Style.RESET_ALL} | " if horario else ""
    
    inicio = f"{Style.BRIGHT}✿ 「{corMensagem[1]} {titulo} {Style.RESET_ALL}{Style.BRIGHT}」✿  " if len(titulo) > 0 else ""
    rotulo = f"\n╰┈➤  {prefixoRotulo+Style.RESET_ALL}{Style.DIM+horarioAtual+Style.RESET_ALL}"
    f"{corMensagem[0]}{Style.BRIGHT}{tipoMensagem} ➤  {Style.RESET_ALL}" if len(tipoMensagem) > 0 else ""

    reticencias = [f"{corMensagem[0]}⌞{Fore.RESET}",f"{corMensagem[0]}⌝{Fore.RESET}"]

    mensagem = f"{Style.BRIGHT}{reticencias[0]} ❛{prefixoMensagem}{mensagem}❜{reticencias[1]}{Style.RESET_ALL}"

    print(f"{inicio}{rotulo}{mensagem.strip()}{Style.RESET_ALL}\n")
    
def DiretorioAtual(completo=False):
    if getattr(sys, 'frozen',False):
        return os.path.dirname(sys.executable) if not completo else sys.executable
    else:
        return os.path.dirname(os.path.abspath(sys.argv[0])) if not completo else os.path.abspath(sys.argv[0])

def ObterENV(arquivoEnv):
    if(not os.path.exists(arquivoEnv)):
        MensagemDeConsolePro("O Arquivo Informado NÃO Existe!",tipoDeMensagem.FALHA)
        return None
    return dotenv_values(arquivoEnv)

def LerVarENV(variaveisEnv,chaveBuscada,chavePadrao=None):
    if(not variaveisEnv or not chaveBuscada):
        return chavePadrao or None
    else:
        return variaveisEnv.get(chaveBuscada,chavePadrao)
    
def AlterarVarENV(novoValor,chaveBuscada,arquivoEnv,reticencias=False):
    set_key(arquivoEnv,chaveBuscada,novoValor,quote_mode="always" if reticencias else "never")
    
def ObterYML(arquivoYML):
    if(not os.path.exists(arquivoYML)):
        MensagemDeConsolePro("O Arquivo Informado NÃO Existe!",tipoDeMensagem.FALHA)
        return None
    try:
        with open(arquivoYML, "r", encoding="utf-8") as yml:
            blocos = yaml.safe_load(yml)
            if(blocos):
                return blocos
            MensagemDeConsolePro(f"O Arquivo YML '{os.path.basename(arquivoYML)}' Está VAZIO ou CORROMPIDO!",tipoDeMensagem.FALHA)
    except Exception as e:
        MensagemDeConsolePro(f"O Arquivo YML '{os.path.basename(arquivoYML)}' NÃO Pôde ser Lido!\nCausa: {e}",2)
        return None
    
def LerDataYML(blocos,nomeDado,trechoDado="",dadoPadrao=None, **kwargs):
    if(not blocos or not isinstance(blocos, dict)):
        MensagemDeConsolePro(f"Os Blocos YML Informados Se Encontram VAZIOS ou CORROMPIDOS!",tipoDeMensagem.FALHA)
        return dadoPadrao
    
    dados = blocos.get(nomeDado)

    if(dados is None):
      MensagemDeConsolePro(f"Erro ao Tentar Localizar o Bloco '{nomeDado}'!",tipoDeMensagem.FALHA)
      return dadoPadrao
    
    if(trechoDado):
        dados = dados.get(trechoDado)
        if(dados is None):
            MensagemDeConsolePro(f"Erro ao Tentar Ler o Trecho '{trechoDado}' no Bloco '{nomeDado}!",tipoDeMensagem.FALHA)
            return dadoPadrao
        
    dadosAchados = []

    def ProcessarTipo(dado):
        if isinstance(dado,str):
            return dado.format(**kwargs)
        return dado
    
    if isinstance(dados,list):
        for i in dados:
            dadosAchados.append(ProcessarTipo(i))
        return dadosAchados[0] if len(dadosAchados) == 1 else dadosAchados
    
    return ProcessarTipo(dados)

def SalvarArquivo(titulo="Salvar Como...",extensaoDoArq=".txt",tiposDeArq=("Arquivos de Texto", "*.txt"),dirInicial=DiretorioAtual(),nomeInicial=""):
    dirArq = filedialog.asksaveasfilename(title=titulo,defaultextension=extensaoDoArq,filetypes=(tiposDeArq,("Todos os Arquivos", "*.*")),initialdir=dirInicial,initialfile=nomeInicial)
    if(dirArq):
        return dirArq

def EscolherArquivo(titulo="Selecione um Arquivo...",tiposDeArq=("Arquivos de áudio", "*.wav *.mp3 *.ogg *.flac"),dirInicial=DiretorioAtual()):
    arq = filedialog.askopenfilename(title=titulo,filetypes=(tiposDeArq,("Todos os Arquivos", "*.*"))) if not dirInicial else filedialog.askopenfilename(title=titulo,filetypes=(tiposDeArq,("Todos os Arquivos", "*.*")),initialdir=dirInicial) 
    if(arq):
        return arq
    
def EscolherDiretorio(titulo="Selecione um Diretório..",dirInicial=DiretorioAtual()):
    dir = filedialog.askdirectory(title=titulo,mustexist=True) if not dirInicial else filedialog.askdirectory(title=titulo,mustexist=True,initialdir=dirInicial)
    if(dir):
        return dir

def TestarConexaoAInternet(tentativasMax=5):
    for i in range (tentativasMax):
        try:
            requests.head("https://www.google.com/",timeout=3)
            return True
        except Exception:
            pass
    return False

def Delay(t=1):
    time.sleep(t)

def Limpar():
    os.system('cls')

def Espaco(qtd=1):
    print(f"{'\n'*qtd}", end='')

def MenuOpcoes(*opcoes,titulo="OPÇÕES",cor="\033[31m"):
    print(f"{(f'『{cor}..:'+titulo.upper()+f':..{Style.RESET_ALL}』').center(50,'=')}\n")
    esp = 0
    for i, opcao in enumerate(opcoes):
        esp += 1
        if(esp > 1):
            print('    ',end='')
            esp = 0
        print(f"｢\033[41;1m' {i+1} '\033[0m｣ - \033[3;40m'{opcao}'\033[0m \n")

def Write(frase, tempo=0.05):
    asni_regex = re.compile(r'\033\[[0-9;]*m')
    m_frase = frase.replace('\r' or '\n', '')

    chars = asni_regex.split(m_frase)
    asnis = asni_regex.findall(m_frase)

    f_frase = []
    for i, char in enumerate(chars):
        f_frase.append(('texto',char))
        if i < len(asnis):
            f_frase.append(('asni',asnis[i]))

    for i, str in f_frase:
        if str == "ansi":
            print(f"{str}",end='',flush=True)
        else:
            for i, char in enumerate(str):
                print(f"{char}", end='', flush=True)
                Delay(tempo)
    print(Style.RESET_ALL,end='')

def EvilWrite(frase="Não me especificaram uma frase, então eu de fato estou puto.", tempo=0.05):
    def MandarFraseCorrupta(f,t):
        chars = len(f)
        fundoV = '\033[40;31;1m'
        corV = '\033[41;30;3m'
        fraseAlt = [f.upper(), f.lower()]
        btd_ch = 0
        for char in range(0, chars):
            bi = random.randint(0,1)
            print(f"{(fundoV, corV)[bi]}{(fraseAlt[bi])[char]}{Style.RESET_ALL}", end='', flush=True)
            btd_ch += 1
            Delay(t)

    if(isinstance(frase,list)):
        for i, f in enumerate(frase):
            MandarFraseCorrupta(f,tempo)
            Espaco()
    else:
        MandarFraseCorrupta(frase,tempo)

def FormatarTempo(tempo,origem="SEGUNDOS",desc=False,modo="TEXTO"):
    match origem:
        case "SEGUNDOS":
            tempoUsuario = tempo
        case "MINUTOS":
            tempoUsuario = tempo * 60
        case "HORAS":
            tempoUsuario = tempo * 3600
            
    def Format(t,tipo):
        formato = ""
        match tipo:
            case "Horas":
                formato = "Horas" if t > 1 else "Hora"
            case "Minutos":
                formato = "Minutos" if t > 1 else "Minuto"
            case "Segundos":
                formato = "Segundos" if t > 1 else "Segundo"
        return f"{t} {formato}"

    minutos, segundos = divmod(int(tempoUsuario),60)
    horas, minutos = divmod(minutos,60)

    match modo:
        case "HH:MM:SS":
            return horas, minutos, segundos
        case "TEXTO":
            if (not desc):
                if(horas > 0):
                    cronometro = '{:02d}:{:02d}:{:02d}'.format(horas, minutos, segundos)
                elif(minutos > 0):
                    cronometro = '{:02d}:{:02d}'.format(minutos, segundos)
                else:
                    cronometro = '{:02d}'.format(segundos)
                return cronometro
            else:
                cronometro = []
                if(horas > 0):
                    cronometro.append(Format(horas,"Horas"))
                if(minutos > 0):
                    cronometro.append(Format(minutos,"Minutos"))
                if(segundos > 0):
                    cronometro.append(Format(segundos,"Segundos"))
                if(len(cronometro) == 1):
                    return cronometro[0]
                
                if len(cronometro) == 0:
                    return "0"

                cronometroDescritivo = ", ".join(cronometro[:-1]) + " e " + cronometro[-1]
                return cronometroDescritivo
            
def ConverterEmUnidadeLite(tempo=0, origem="SEGUNDOS",modo="MINUTOS",converterParaInt=False):
    tempoConvertido = float(0)
    match origem:
        case "SEGUNDOS":
            tempoUsuario = tempo
        case "MINUTOS":
            tempoUsuario = tempo * 60
        case "HORAS":
            tempoUsuario = tempo * 3600
            
    match modo:
        case "SEGUNDOS":
            tempoConvertido = tempoUsuario
        case "MINUTOS":
            tempoConvertido = tempoUsuario / 60
        case "HORAS":
            tempoConvertido = tempoUsuario / 3600
        case "AUTO":
            if tempoUsuario < 60:
                tempoConvertido = tempoUsuario
            elif tempoUsuario < 3600:
                tempoConvertido = tempoUsuario / 60
            else:
                tempoConvertido = tempoUsuario / 3600

    if tempoConvertido.is_integer() or converterParaInt:
        return(int(tempoConvertido))
    else:
        return tempoConvertido
            
def ConverterEmUnidadePro(horas=0, minutos=0, segundos=0, modo="SEGUNDOS",converterParaInt=False):
    tempoConvertido = float(0)
    match modo:
        case "SEGUNDOS":
            tempoConvertido = (horas * 3600) + (minutos * 60) + segundos
        case "MINUTOS":
            tempoConvertido = (horas * 60) + minutos + (segundos / 60)
        case "HORAS":
            tempoConvertido = horas + (minutos / 60) + (segundos / 3600)

    if tempoConvertido.is_integer() or converterParaInt:
        return(int(tempoConvertido))
    else:
        return tempoConvertido
    
def ConverterNumerosEmPalavras(numero, tipoOrdinal=False, idiomaDesejado="pt-br"):
    try:
        return str(num2words(numero,lang=idiomaDesejado,ordinal=tipoOrdinal))
    except:
        return "X"
    
def BinaryFill(vezes,corUm=Fore.RED,corDois=Back.RED,tempo=0.1):
    opcao_cor = [Style.BRIGHT+corUm, Style.BRIGHT+corDois, Style.RESET_ALL]
    linha = 0
    while(vezes > 0):
        linha += 1
        if(linha >= 40):
            print("\n", end='')
            linha = 0
        print(f"{opcao_cor[random.randint(0,1)]}{random.randint(0,1)}{opcao_cor[2]}", end="", flush=True)
        vezes -= 1
        Delay(tempo)
    print(Style.RESET_ALL)

def BinaryWriteAndFill(frase,corUm=Fore.RED,corDois=Back.RED,tempo=0.1):
    writeCors = [f"{Style_Extra.ITALICO}{corUm}", f"{Style.BRIGHT}{corDois}", "\033[0m"]
    chars = len(frase)
    char = 0
    linha = 0
    while(char < chars):
        linha += 1
        if(linha >= 40):
            print("\n", end='')
            linha = 0
        prob = random.randint(0,100)
        if(prob <= 20):
            print(f"{writeCors[1]}{frase[char]}{writeCors[2]}", end="", flush=True)
            char += 1
            print(f"{writeCors[0]}{random.randint(0,1)}{writeCors[2]}", end="", flush=True)
        else:
            print(f"{writeCors[0]}{random.randint(0,1)}{writeCors[2]}", end="", flush=True)
        Delay(tempo)
    print(Style.RESET_ALL)

def MensagemPersonagem(texto="Eu vou assumir uma frase aleatória,\npois esqueceram de me instruir o que dizer.",
                       nomePerso="Cherry Violet",corPerso="\033[45m",simboloPerso="☪️",t=0.05):
    Write(f'{simboloPerso} ',t)
    Write(f'{corPerso}'+'['+'\033[1m'+nomePerso+'\033[0m'+f'{corPerso}'+']',t)
    Write(f': {simboloPerso}',t)
    Espaco()
    Write(f"\033[3;40m{'"'}{texto}{Style.RESET_ALL}\033[3;40m{'"'}",t)
    Espaco()

def Creditos():
    MensagemPersonagem("Script By: CV. Blossom 🌙.","Cherry Violet","\033[45m","☪️")

def LerOpcao(opcoes=1,desc="Opção Escolhida"):
    mensagemOpcaoInvalida = "A Opção Escolhida NÃO ESTÁ DISPONÍVEL!"
    mensagemErroDigitacao = "A Opção NÃO foi INFORMADA ou é INVÁLIDA!"
    quantidadeDeErros = 0

    def LidarComErros(mensagem="ERRO DESCONHECIDO!",quantidadeAtualDeErros=0):
        Espaco(1)
        if(quantidadeAtualDeErros != 5):
            MensagemDeConsole(mensagem,2)
        else:
            BinaryFill(20)
            Espaco(1)
            MensagemPersonagem("...")
            Espaco(1)
            MensagemPersonagem("...LEIA...")
            Espaco(1)
            MensagemPersonagem("... A TELA!..")
            Espaco(2)

    while True:
        try:
            opcaoEscolhida = int(input(f"{Style.BRIGHT}「 {Back.BLACK}{desc}\033[39;49m 」{Style.RESET_ALL}:\n{Style.BRIGHT}>>{Style.RESET_ALL} "))
            if opcaoEscolhida >= 1 and opcaoEscolhida <= opcoes:
                return opcaoEscolhida
            else:
                quantidadeDeErros += 1
                LidarComErros(mensagemOpcaoInvalida,quantidadeDeErros)
                continue
        except:
            quantidadeDeErros += 1
            LidarComErros(mensagemErroDigitacao,quantidadeDeErros)
            continue

def LerInput(tipo=1,desc="Digite Aqui"):
    while True:
        inputDigitado = input(f"{Style.BRIGHT}「 {Back.BLACK}{desc}\033[39;49m 」{Style.RESET_ALL}:\n{Style.BRIGHT}>>{Style.RESET_ALL} ")
        if(not inputDigitado):
            MensagemDeConsole("NADA foi Informado!",2)
            continue
        match tipo:
            case 1: # Input do Tipo String
                return(inputDigitado)
            case 2: # Input do Tipo Número (Inteiro)
                try:
                    return int(inputDigitado)
                except:
                    MensagemDeConsole("Digite um Número VÁLIDO!",2)
                    continue
            case 3: # Input do Tipo Número (Float)
                try:
                    return float(inputDigitado)
                except:
                    MensagemDeConsole("Digite um Número VÁLIDO!",1)
                    continue

def ProcessarPastaDeDados(origem="",nomeDaPasta="",aceitarPastaNova=False):
    caminhoParaPasta = os.path.join(origem,nomeDaPasta)
    def ChecarExistencia():
        return os.path.exists(caminhoParaPasta)
    
    novaPastaFalhou = False
    while not ChecarExistencia():
        Limpar()
        Write(f"\033[1;31mA Pasta Data NÃO Pôde Ser Encontrada!\n") if not novaPastaFalhou else Write(f"\033[1;31mA Pasta Data Substituta NÃO Pôde Ser Gerada!")
        if(aceitarPastaNova and not novaPastaFalhou):
            Write(f"\033[1;31mGerando uma Nova...")
            Delay(0.5)
            Path.mkdir(caminhoParaPasta,exist_ok=True)
            novaPastaFalhou = True
            continue
        Delay(1)
        sys.exit()
        break
    Limpar()
    return os.path.abspath(caminhoParaPasta)

def CriarPasta(diretorioDesejado=""):
    if(os.path.exists(diretorioDesejado)):
        return os.path.abspath(diretorioDesejado)
    diretorioParaCriar = os.path.abspath(diretorioDesejado)
    Path.mkdir(diretorioParaCriar,exist_ok=True)
    return diretorioParaCriar if os.path.exists(diretorioParaCriar) else None
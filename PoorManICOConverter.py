from Bibliotecas import CVLib as CV
import os, traceback
from pathlib import Path
from PIL import Image

pastaData = CV.ProcessarPastaDeDados(CV.DiretorioAtual(),"PMICData",True)

def SelecionarPasta(diretorioInicial):
    CV.MensagemDeConsolePro("Informe o Diretório de Destino..:")
    dirUser = CV.EscolherDiretorio(dirInicial=diretorioInicial)
    if(dirUser and os.path.exists(dirUser)):
        return dirUser

def Main():
    print(f"""
        ==========================
    『 🎨 {CV.Style.BRIGHT}{CV.Back.BLACK}{CV.Fore.YELLOW} ICO - Converter {CV.Style.RESET_ALL} 🖼️ 』
            {CV.Style_Extra.ITALICO}(De Pobreeee! <3){CV.Style.RESET_ALL}
        ==========================
    """)
    CV.MensagemDeConsolePro("Informe o Arquivo de Imagem Desejado..:")
    arq = CV.EscolherArquivo(titulo="Selecione uma Imagem",tiposDeArq=("Arquivos de Imagem","*.jpg *.jpeg *.png *.bmp *.gif *.webp"))
    if(os.path.exists(arq)):
        CV.Limpar()
        try:
            imagemAberta = Image.open(arq)
            nomeImagemConvertida = f"{os.path.splitext(os.path.basename(arq))[0]}.ico"
            diretorioParaSalvar = rf"{SelecionarPasta(Path(arq).parent)}\{nomeImagemConvertida}"
            if(not os.path.exists(os.path.dirname(diretorioParaSalvar))):
                diretorioParaSalvar = rf"{Path(arq).parent}\{nomeImagemConvertida}"
            CV.MenuOpcoes("128x128","64x64","32x32","16x16",titulo="Qual o Tamanho Desejado?")
            match CV.LerOpcao(4):
                case 1:
                    imagemAberta.save(diretorioParaSalvar,format="ICO", sizes=[(128,128),(64,64),(32,32),(16,16)],bitmap_format="bmp")
                case 2:
                    imagemAberta.save(diretorioParaSalvar,format="ICO", sizes=[(64,64),(32,32),(16,16)],bitmap_format="bmp")
                case 3:
                    imagemAberta.save(diretorioParaSalvar,format="ICO", sizes=[(32,32),(16,16)],bitmap_format="bmp")
                case 4:
                    imagemAberta.save(diretorioParaSalvar,format="ICO", sizes=[(16,16)],bitmap_format="bmp")
             
        except:
            traceback.print_exc()

if(os.path.exists(pastaData)):
    Main()

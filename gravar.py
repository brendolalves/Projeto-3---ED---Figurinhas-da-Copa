import csv
from estrutura import Album, FilaHistorico


def carregar_banca_completa(caminho_csv):
    banca = []
    with open(caminho_csv, mode="r", encoding="utf-8") as arq:
        leitor = csv.DictReader(arq)
        for linha in leitor:
            banca.append(linha)
    return banca

def salvar_album_csv(album_objeto: Album, caminho_output):
    with open(caminho_output, mode="w", newline="", encoding="utf-8") as arq:
        escritor = csv.writer(arq)
        escritor.writerow(["id", "nome", "pais", "posicao", "raridade"])
        
        atual = album_objeto.cabeca
        while atual is not None:
            f = atual.figurinha
            escritor.writerow([f.id, f.nome, f.pais, f.posicao, f.raridade])
            atual = atual.proximo

def salvar_historico_csv(fila_historico: FilaHistorico, caminho_output):
    with open(caminho_output, mode="a", newline="", encoding="utf-8") as arq:
        escritor = csv.writer(arq)
        while True:
            registro = fila_historico.dequeue()
            if registro is None:
                break
            escritor.writerow([registro])
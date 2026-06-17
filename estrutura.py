import csv
import random

class figurinhas:
    def __init__(self, id_fig, nome, pais, posicao, raridade):
        self.id = int(id_fig)
        self.nome = nome
        self.pais = pais
        self.posicao = posicao
        self.raridade = raridade

class NodoLista:
    def __init__(self, figurinha):
        self.figurinha = figurinha
        self.proximo = None


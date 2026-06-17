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

class Album:
    def __init__(self, total_album=1200):
        self.cabeca = None
        self.tamanho = 0
        self.TOTAL_ALBUM = total_album

    def adicionar(self, figurinha):
        novo_nodo = NodoLista(figurinha)

        if self.cabeca is None or self.cabeca.figurinha.id > figurinha.id:
            novo_nodo.proximo = self.cabeca
            self.cabeca = novo_nodo
            self.tamanho = self.tamanho + 1
            return True
        
        atual = self.cabeca
        while atual.proximo is not None and atual.proximo.figurinha.id > figurinha.id:
            atual = atual.proximo

        novo_nodo.proximo = atual.proximo
        atual.proximo = novo_nodo
        self.tamanho = self.tamanho + 1
        return True
    
    def existe_id(self, id_buscado = int):
        atual = self.cabeca
        while atual is not None:
            if atual.figurinha.id == id_buscado:
                return True
            atual = atual.proximo
        return False
    
    
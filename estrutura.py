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
    
    def renover(self, id_buscado: int):
        if self.cabeca is None:
            return None
        
        if self.cabeca.figurinha.id == id_buscado:
            removida = self.cabeca.figurinha
            self.cabeca = self.cabeca.proximo
            self.tamanho -= 1
            return removida
        
        atual = self.cabeca
        while atual.proximo is not None:
            if atual.proximo.figurinha.id == id_buscado:
                removida = atual.proximo.figurinha
                atual.proximo = atual.proximo.proximo
                self.tamanho -= 1
                return removida
            atual = atual.proximo
        return None
    
    def buscar_por_filtros(self, filtro_tipo, valor):
        atual = self.cabeca
        encontrou = False
        while atual is not None:
            f = atual.figurinha
            if (filtro_tipo == "id" and f.id == int(valor)) or \
               (filtro_tipo == "pais" and valor.lower() in f.pais.lower()) or \
               (filtro_tipo == "nome" and valor.lower() in f.nome.lower()):
                print(f"[{f.id}] {f.nome} - {f.pais} ({f.posicao}) - {f.raridade}")
                encontrou = True
            atual = atual.proximo
        if not encontrou:
            print("Nenhuma figurinha encontrada com este filtro.")

    def calcular_porcentagem(self):
        return (self.tamanho / self.TOTAL_ALBUM) * 100

    def mostrar_faltantes(self):
        """Varre de 1 a 1200 e mostra quais IDs não estão na lista encadeada"""
        print("IDs que faltam no seu álbum:")
        atual = self.cabeca
        id_esperado = 1
        
        while id_esperado <= self.TOTAL_ALBUM:
            if atual is not None and atual.figurinha.id == id_esperado:
                atual = atual.proximo
            else:
                print(id_esperado, end=" ")
            id_esperado += 1
        print("\n")


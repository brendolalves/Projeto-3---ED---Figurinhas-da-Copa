# Sistema de Álbum de Figurinhas - Copa 2026 ⚽🏆

Este projeto consiste no desenvolvimento de um sistema completo para gerenciamento, coleção, organização e troca de figurinhas de jogadores e seleções da Copa do Mundo de 2026. O sistema foi desenvolvido como parte da terceira avaliação da disciplina de **Estrutura de Dados** na **FATEC Rio Claro**.

## Descrição do Projeto

O objetivo principal é aplicar conceitos fundamentais de estruturas de dados lineares — especificamente **Listas Encadeadas** e **Filas FIFO (First-In, First-Out)** — de forma manual, ou seja, **sem a utilização de estruturas embutidas do Python** (como `list`, `deque`, dicionários ou métodos prontos de ordenação/busca). Todo o encadeamento e gerenciamento de memória/ponteiros foi implementado por meio de nós de dados.


## Arquitetura e Classes Implementadas

O sistema é dividido estruturalmente em classes de entidades, nós de apontamento e estruturas de gerenciamento:

### 1. Entidades Base
* **`Figurinha`**: Classe que representa a entidade de uma figurinha.
    * **Atributos:** `id` (int), `nome` (str), `pais` (str), `posicao` (str) e `raridade` (str).

### 2. Estrutura de Lista Encadeada (Álbum)
* **`NodoLista`**: Nó de manipulação que armazena uma instância de `Figurinha` e a referência para o `proximo` nó da lista.
* **`Album`**: Representação principal do álbum do usuário baseado em uma lista encadeada.
    * **Atributos:** `_cabeca` (NodoLista) e `_tamanho` (int).
    * **Métodos:** `adicionar()`, `remover()` e `buscar()`.

### 3. Estrutura de Fila FIFO (Trocas e Histórico)
* **`NodoFila`**: Nó de manipulação que armazena uma instância de `Figurinha` e a referência para o `proximo` nó da fila.
* **`Fila`**: Implementação própria e manual de uma fila FIFO.
    * **Atributos:** `_inicio` e `_fim`.
    * **Métodos:** `enqueue()`, `dequeue()`, `peek()` e `limpar()`.
* **`Histórico`**: Uma instância separada da classe `Fila` dedicada exclusivamente ao registro cronológico de todas as trocas e disputas efetuadas.


## Funcionalidades Principais

### Gerenciamento do Álbum
* **Inserção e Remoção:** Permite inserir novas figurinhas obtidas ou remover itens se necessário.
* **Consulta:** Busca detalhada de itens pertencentes ao álbum.
* **Visualização Geral:** Exibição do álbum completo de forma organizada.
* **Progresso:** Cálculo em tempo real da porcentagem concluída do álbum.

### Figurinhas Repetidas
* Armazenamento dinâmico de figurinhas repetidas.
* Exibição da listagem detalhada de repetidas disponíveis para troca.
* Contador integrado da quantidade total de repetidas acumuladas.

### Mecanismo de Busca
O sistema possui algoritmos manuais de varredura para buscas por:
1.  Número (ID) da figurinha.
2.  Nome do Jogador.
3.  Nome da Seleção.

### Sistema de Trocas Automáticas
* Registro formal de propostas de trocas em fila.
* Verificação cruzada de redundância (valida se ambos os usuários possuem as repetidas de interesse mútuo).
* Efetivação automática da troca com atualização imediata dos álbuns e envio do registro para a fila de Histórico.

### Persistência de Dados
* Salvamento e carregamento do estado do álbum e das filas através de arquivos de persistência externa (Formatos: TXT, CSV ou JSON).


## Requisitos Técnicos

* **Zero Built-ins:** Nenhuma estrutura nativa do Python foi utilizada para substituir o encadeamento de nós.
* **Tratamento de Exceções:** O sistema valida rigorosamente entradas inválidas, tais como: códigos de seleções inexistentes, IDs de figurinhas fora do escopo do campeonato, caracteres inválidos em campos numéricos, entre outros cenários de erro.

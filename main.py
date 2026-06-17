import random
from estrutura import Album, FilaHistorico, Figurinha
from gravar import carregar_banca_completa, salvar_album_csv, salvar_historico_csv


def menu_principal():
    # 1. Inicializa os álbuns vazios (Listas Encadeadas) e o Histórico (Fila)
    album_A = Album()
    album_B = Album()
    album_repetidas = Album()
    historico = FilaHistorico()
    
    # Carrega os dados base da banca
    try:
        dados_banca = carregar_banca_completa("figurinhas_copa_completo.csv")
    except FileNotFoundError:
        print("Erro: O arquivo 'figurinhas_copa_completo.csv' não foi encontrado.")
        print("Por favor, execute o script que gera a banca primeiro.")
        return

    while True:
        print("\n--- SISTEMA ÁLBUM COPA 2026 ---")
        print("1. Comprar Pacotinho(s)")
        print("2. Ver Álbuns e Estatísticas")
        print("3. Buscar Figurinha por Filtro")
        print("4. Realizar Troca/Envio entre Jogador A e B")
        print("5. Salvar dados em CSV e Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            jogador = input("Quem está a comprar? (A ou B): ").upper()
            if jogador not in ["A", "B"]:
                print("Jogador inválido! Escolha A ou B.")
                continue
                
            alvo_album = album_A if jogador == "A" else album_B
            
            try:
                qtd_pacotes = int(input("Quantos pacotes de 7 figurinhas deseja comprar de uma vez? "))
                if qtd_pacotes <= 0:
                    print("A quantidade deve ser maior que zero.")
                    continue
            except ValueError:
                print("Por favor, digite um número inteiro válido.")
                continue

            total_figurinhas_ganhas = qtd_pacotes * 7
            print(f"\n--- A abrir {qtd_pacotes} pacote(s) ({total_figurinhas_ganhas} figurinhas) para o Jogador {jogador} ---")
            
            pacotao = random.choices(dados_banca, k=total_figurinhas_ganhas)
            
            for item in pacotao:
                fig = Figurinha(item['id'], item['nome'], item['pais'], item['posicao'], item['raridade'])
                print(f"Ganhou: ID {fig.id:4} | {fig.nome:<35} | {fig.pais:<15} ({fig.raridade})")
                
                if alvo_album.existe_id(fig.id):
                    print(f"   --> [REPETIDA] Enviada para o álbum de repetidas.")
                    album_repetidas.adicionar(fig)
                    historico.enqueue(f"Jogador {jogador} tirou ID {fig.id} repetida.")
                else:
                    alvo_album.adicionar(fig)
                    historico.enqueue(f"Jogador {jogador} colou a ID {fig.id} no seu álbum.")
            
            print(f"\nCompra concluída com sucesso! {total_figurinhas_ganhas} figurinhas processadas.")

        elif opcao == "2":
            print(f"\nStatus Jogador A: {album_A.calcular_porcentagem():.2f}% concluído ({album_A.tamanho} coladas)")
            print(f"Status Jogador B: {album_B.calcular_porcentagem():.2f}% concluído ({album_B.tamanho} coladas)")
            print(f"Total no monte de repetidas: {album_repetidas.tamanho} figurinhas")
            
            sub = input("Deseja ver os IDs faltantes de quem? (A, B ou 'N' para não ver): ").upper()
            if sub == "A": album_A.mostrar_faltantes()
            elif sub == "B": album_B.mostrar_faltantes()

        elif opcao == "3":
            quem = input("Buscar no álbum de quem? (A, B ou R para Repetidas): ").upper()
            tipo = input("Filtrar por (id, pais ou nome): ").lower()
            valor = input("Digite o termo de busca: ")
            
            if quem == "A": album_A.buscar_por_filtros(tipo, valor)
            elif quem == "B": album_B.buscar_por_filtros(tipo, valor)
            elif quem == "R": album_repetidas.buscar_por_filtros(tipo, valor)

        elif opcao == "4":
            print("\n--- Troca Direta ---")
            origem = input("Quem vai enviar a figurinha? (A ou B): ").upper()
            
            try:
                id_troca = int(input("Digite o ID da figurinha a ser enviada: "))
            except ValueError:
                print("ID inválido!")
                continue
            
            if origem == "A":
                fig_movida = album_A.remover(id_troca)
                if fig_movida:
                    if album_B.existe_id(id_troca):
                        album_repetidas.adicionar(fig_movida)
                        print(f"Jogador B já tinha. ID {id_troca} foi para o Álbum de Repetidas.")
                        historico.enqueue(f"Jogador A enviou ID {id_troca} para B (Virou repetida).")
                    else:
                        album_B.adicionar(fig_movida)
                        print(f"Sucesso! ID {id_troca} colada no álbum do Jogador B.")
                        historico.enqueue(f"Jogador A enviou ID {id_troca} para o álbum do Jogador B.")
                else:
                    print("Jogador A não possui essa figurinha colada para enviar.")
            
            elif origem == "B":
                fig_movida = album_B.remover(id_troca)
                if fig_movida:
                    if album_A.existe_id(id_troca):
                        album_repetidas.adicionar(fig_movida)
                        print(f"Jogador A já tinha. ID {id_troca} foi para o Álbum de Repetidas.")
                        historico.enqueue(f"Jogador B enviou ID {id_troca} para A (Virou repetida).")
                    else:
                        album_A.adicionar(fig_movida)
                        print(f"Sucesso! ID {id_troca} colada no álbum do Jogador A.")
                        historico.enqueue(f"Jogador B enviou ID {id_troca} para o álbum do Jogador A.")
                else:
                    print("Jogador B não possui essa figurinha colada para enviar.")
            else:
                print("Origem inválida!")

        elif opcao == "5":
            # Salva os estados atuais e o histórico
            salvar_album_csv(album_A, "album_jogador_A.csv")
            salvar_album_csv(album_B, "album_jogador_B.csv")
            salvar_album_csv(album_repetidas, "album_repetidas.csv")
            salvar_historico_csv(historico, "historico_trocas.csv")
            print("Todos os estados e arquivos .csv foram salvos com sucesso! A encerrar...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu_principal()
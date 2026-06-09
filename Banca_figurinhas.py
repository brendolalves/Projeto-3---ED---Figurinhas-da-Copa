import csv
import random
import re
from faker import Faker

# Configurações do álbum
SELECOES_TOTAIS = 48
TITULARES_POR_SELECAO = 11
RESERVAS_POR_SELECAO = 13
ARQUIVO_OUTPUT = "figurinhas_copa_completo.csv"

# Mapeamento com as localidades nativas para manter a acentuação e nomes típicos de cada país
PAISES_CONFIG = [
    # América do Sul / América Latina
    {"nome": "Brasil", "faker_loc": "pt_BR"},
    {"nome": "Argentina", "faker_loc": "es_AR"},
    {"nome": "Uruguai", "faker_loc": "es_AR"},
    {"nome": "Colômbia", "faker_loc": "es_CO"},
    {"nome": "Chile", "faker_loc": "es_CL"},
    {"nome": "México", "faker_loc": "es_MX"},
    {"nome": "Peru", "faker_loc": "es_MX"},
    {"nome": "Venezuela", "faker_loc": "es_MX"},
    
    # Europa (com todos os seus acentos nativos e exóticos preservados)
    {"nome": "Alemanha", "faker_loc": "de_DE"},
    {"nome": "França", "faker_loc": "fr_FR"},
    {"nome": "Itália", "faker_loc": "it_IT"},
    {"nome": "Espanha", "faker_loc": "es_ES"},
    {"nome": "Portugal", "faker_loc": "pt_PT"},
    {"nome": "Inglaterra", "faker_loc": "en_GB"},
    {"nome": "Holanda", "faker_loc": "nl_NL"},
    {"nome": "Bélgica", "faker_loc": "nl_BE"},
    {"nome": "Croácia", "faker_loc": "hr_HR"},  # Mantém os acentos eslavos (š, ć, đ)
    {"nome": "Polônia", "faker_loc": "pl_PL"},    # Mantém os acentos polacos (ł, ę, ó)
    {"nome": "Suécia", "faker_loc": "sv_SE"},     # Mantém os nórdicos (å, ä, ö)
    {"nome": "Turquia", "faker_loc": "tr_TR"},    # Mantém os turcos (ç, ğ, ı)
    {"nome": "Grécia", "faker_loc": "en_US"},     # Mantém alfabeto latino em inglês para representação comercial
    {"nome": "Romênia", "faker_loc": "ro_RO"},
    {"nome": "Ucrânia", "faker_loc": "en_US"},    
    {"nome": "Suíça", "faker_loc": "de_CH"},
    {"nome": "Áustria", "faker_loc": "de_AT"},
    {"nome": "República Checa", "faker_loc": "cs_CZ"},
    {"nome": "Finlândia", "faker_loc": "fi_FI"},
    {"nome": "Dinamarca", "faker_loc": "da_DK"},
    {"nome": "Noruega", "faker_loc": "no_NO"},
    
    # Ásia / Oceania (Alinhado para alfabeto latino ocidental)
    {"nome": "Japão", "faker_loc": "en_US"},
    {"nome": "Coréia do Sul", "faker_loc": "en_US"},
    {"nome": "Austrália", "faker_loc": "en_AU"},
    {"nome": "China", "faker_loc": "en_US"},
    {"nome": "Índia", "faker_loc": "en_TH"},
    {"nome": "Nova Zelândia", "faker_loc": "en_NZ"},
    
    # África / Oriente Médio
    {"nome": "Egito", "faker_loc": "fr_FR"},
    {"nome": "Arábia Saudita", "faker_loc": "en_US"},
    {"nome": "Marrocos", "faker_loc": "fr_FR"},
    {"nome": "Nigéria", "faker_loc": "en_NG"},
    {"nome": "África do Sul", "faker_loc": "en_ZA"},
    
    # América do Norte
    {"nome": "Estados Unidos", "faker_loc": "en_US"},
    {"nome": "Canadá", "faker_loc": "en_CA"},
    
    # Países adicionais
    {"nome": "Irlanda", "faker_loc": "en_IE"},
    {"nome": "Escócia", "faker_loc": "en_GB"},
    {"nome": "País de Gales", "faker_loc": "en_GB"},
    {"nome": "Paraguai", "faker_loc": "es_AR"},
    {"nome": "Equador", "faker_loc": "es_CO"},
    {"nome": "Costa Rica", "faker_loc": "es_MX"},
]

fakers_cache = {}
for pais in PAISES_CONFIG:
    loc = pais["faker_loc"]
    if loc not in fakers_cache:
        try:
            fakers_cache[loc] = Faker(loc)
        except (AttributeError, ValueError):
            fakers_cache[loc] = Faker("en_US")

POSICOES_LINHA = ["Goleiro", "Zagueiro", "Lateral", "Meio-Campo", "Atacante"]
RARIDADES = ["Muito Raro", "Raro", "Comum"]
PESOS_RARIDADES = [0.05, 0.05, 0.90]

def limpar_e_normalizar_nome(nome_cru):
    # 1. Lista expandida de pronomes de tratamento comuns gerados pelo Faker
    lista_pronomes = r"\b(Sr|Sra|Dr|Dra|Mr|Mrs|Ms|Miss|Ing|Prof|Pan|Hr|Fr|Mme|Mlle|Doc|Srta)\b\.?\s*"
    nome_limpo = re.sub(lista_pronomes, "", nome_cru, flags=re.IGNORECASE)
    
    # 2. Remove especificamente o termo (a) ou (a). que costuma aparecer
    # O hífen ou espaço extra antes/depois do (a) também será tratado
    nome_limpo = re.sub(r"\s*\(a\)\.?\s*", " ", nome_limpo, flags=re.IGNORECASE)
    
    # 3. Substitui múltiplos espaços em branco por apenas um espaço simples
    nome_limpo = re.sub(r"\s+", " ", nome_limpo)
    
    # Retorna o nome retirando espaços extras no início ou no fim
    return nome_limpo.strip()

def gerar_nome_masculino_limpo(faker_instancia):
    try:
        nome_cru = faker_instancia.name_male()
    except AttributeError:
        nome_cru = faker_instancia.name()
        
    return limpar_e_normalizar_nome(nome_cru)

def gerar_album_completo():
    figurinhas = []
    id_atual = 1

    for pais_info in PAISES_CONFIG:
        nome_pais = pais_info["nome"]
        faker_pais = fakers_cache[pais_info["faker_loc"]]

        # 1. TITULARES
        for _ in range(TITULARES_POR_SELECAO):
            nome = gerar_nome_masculino_limpo(faker_pais)
            posicao = random.choice(POSICOES_LINHA)
            raridade = random.choices(RARIDADES, weights=PESOS_RARIDADES, k=1)[0]
            
            figurinhas.append({
                "id": id_atual, "nome": nome, "pais": nome_pais,
                "posicao": f"{posicao} (Titular)", "raridade": raridade
            })
            id_atual += 1

        # 2. RESERVAS
        for _ in range(RESERVAS_POR_SELECAO):
            nome = gerar_nome_masculino_limpo(faker_pais)
            posicao = random.choice(POSICOES_LINHA)
            raridade = random.choices(RARIDADES, weights=PESOS_RARIDADES, k=1)[0]
            
            figurinhas.append({
                "id": id_atual, "nome": nome, "pais": nome_pais,
                "posicao": f"{posicao} (Reserva)", "raridade": raridade
            })
            id_atual += 1

        # 3. TÉCNICO
        nome_tecnico = gerar_nome_masculino_limpo(faker_pais)
        raridade_tecnico = random.choices(RARIDADES, weights=PESOS_RARIDADES, k=1)[0]
        
        figurinhas.append({
            "id": id_atual, "nome": nome_tecnico, "pais": nome_pais,
            "posicao": "Técnico", "raridade": raridade_tecnico
        })
        id_atual += 1

    return figurinhas


import pandas as pd

# Configurações globais de exibição
pd.set_option("display.max_columns", None)   # mostra todas as colunas
pd.set_option("display.max_rows", None)      # mostra todas as linhas
pd.set_option("display.width", None)         # não limita largura
pd.set_option("display.colheader_justify", "center")  # centraliza cabeçalhos


def parse_valor(valor_str):
    """
    Converte string no formato brasileiro (ex: '2.035,34') para float.
    """
    valor_str = valor_str.replace(".", "").replace(",", ".")
    return float(valor_str)

def simulador_financas():
    # Coleta de informações do usuário
    saldo_inicial = parse_valor(input("Digite o saldo inicial (R$): "))
    aporte_mensal = parse_valor(input("Digite o valor do aporte mensal (R$): "))
    taxa_mensal = float(input("Digite a taxa de rendimento mensal (ex: 0.0075 para 0,75%): "))
    meses = int(input("Digite o número de meses da simulação: "))

    # Objetivo do usuário
    renda_objetivo = parse_valor(input("Digite a renda passiva desejada (R$): "))
    prazo_objetivo = int(input("Digite o prazo em anos para atingir (ex: 10): "))
    montante_alvo = renda_objetivo / taxa_mensal
    n = prazo_objetivo * 12
    i = taxa_mensal

    # cálculo do aporte fixo necessário (sem considerar saldo inicial)
    aporte_necessario_fixo = (montante_alvo * i) / ((1+i)**n - 1)

    # Aportes extras
    aportes_extra = {}
    while True:
        resp = input("Deseja adicionar aporte extra em algum mês? (s/n): ").lower()
        if resp == "s":
            mes = int(input("Digite o mês do aporte extra: "))
            valor = parse_valor(input("Digite o valor do aporte extra (R$): "))
            aportes_extra[mes] = valor
        else:
            break

    # Saques
    saques = {}
    while True:
        resp = input("Deseja adicionar saque em algum mês? (s/n): ").lower()
        if resp == "s":
            mes = int(input("Digite o mês do saque: "))
            valor = parse_valor(input("Digite o valor do saque (R$): "))
            saques[mes] = valor
        else:
            break

    # Simulação
    saldo = saldo_inicial
    historico = []
    aporte_sugerido = aporte_mensal

    for mes in range(1, meses+1):
        valor_aporte_extra = aportes_extra.get(mes, 0)
        valor_saque = saques.get(mes, 0)

        saldo_mes = saldo + aporte_sugerido + valor_aporte_extra - valor_saque
        rendimento = saldo_mes * taxa_mensal
        saldo = saldo_mes + rendimento

        if meses > 12 and mes % 12 == 0:
            aporte_sugerido *= 1.10

        historico.append({
            "Mês": mes,
            "Aporte atual": round(aporte_sugerido + valor_aporte_extra - valor_saque, 2),
            "Montante acumulado": round(saldo, 2),
            "Rendimento (~0,75%)": round(rendimento, 2),
            "Aporte necessário p/ objetivo": round(aporte_necessario_fixo, 2)
        })

    df = pd.DataFrame(historico)

    # Linha final de resumo
    df.loc[len(df)] = [
        "Resumo",
        aporte_mensal,
        round(saldo, 2),
        round(saldo * taxa_mensal, 2),
        round(aporte_necessario_fixo, 2)
    ]

    print("\nEvolução do saldo:")
    print(df)

    # Cenário mantendo aporte atual
    saldo = saldo_inicial
    aporte = aporte_mensal
    meses_para_alvo = 0
    while saldo < montante_alvo:
        saldo_mes = saldo + aporte
        rendimento = saldo_mes * taxa_mensal
        saldo = saldo_mes + rendimento
        meses_para_alvo += 1
    anos_para_alvo = round(meses_para_alvo / 12, 1)

    print(f"\n➡ Mantendo o aporte atual de R$ {aporte_mensal} + 10% a cada 12 meses [correção da inflação] você atingirá a renda desejada em aproximadamente {anos_para_alvo} anos.")
    print(f"➡ Para atingir em {prazo_objetivo} anos, o aporte mensal necessário seria de aproximadamente R$ {round(aporte_necessario_fixo,2)}.")

# Executa o simulador
simulador_financas()

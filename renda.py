import pandas as pd

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

        # saldo do mês antes do rendimento
        saldo_mes = saldo + aporte_sugerido + valor_aporte_extra - valor_saque

        # rendimento calculado sobre o saldo do mês
        rendimento = saldo_mes * taxa_mensal
        saldo = saldo_mes + rendimento

        # regra da sugestão de aporte:
        if meses > 12 and mes % 12 == 0:
            aporte_sugerido *= 1.10  # aumenta aporte em 10% a cada 12 meses

        historico.append({
            "Mês": mes,
            "Valor": round(aporte_sugerido + valor_aporte_extra - valor_saque, 2),
            "Montante": round(saldo, 2),
            "Rendimento (~0,75%)": round(rendimento, 2),
            "Sugestão de aporte": round(aporte_sugerido, 2)
        })

    # Exibe resultado
    df = pd.DataFrame(historico)
    print("\nEvolução do saldo:")
    print(df)

# Executa o simulador
simulador_financas()

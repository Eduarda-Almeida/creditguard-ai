print("=== CreditGuard AI ===")
print("Assistente de análise preliminar de crédito")
print()

renda = float(input("Informe a renda mensal fictícia (R$): "))
parcela = float(input("Informe o valor da parcela fictícia (R$): "))

if renda <= 0 or parcela < 0:
    print("Erro: informe valores válidos.")
else:
    comprometimento = (parcela / renda) * 100

    print()
    print(f"Comprometimento de renda: {comprometimento:.1f}%")
    print("Resultado demonstrativo. Não representa aprovação de crédito.")
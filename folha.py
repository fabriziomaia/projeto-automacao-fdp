from dataclasses import dataclass
from fpdf import FPDF
import csv
from datetime import datetime

@dataclass
class Funcionario:
    nome: str
    matricula: str
    cargo: str
    salario_base: float
    adicional_periculosidade: float = 0.0
    adicional_insalubridade: float = 0.0
    adicional_noturno: float = 0.0
    horas_extras_50: float = 0.0
    horas_extras_100: float = 0.0
    comissoes: float = 0.0
    premios: float = 0.0
    plr: float = 0.0
    ferias: float = 0.0
    decimo_terceiro: float = 0.0

    # Descontos
    vale_transporte: float = 0.0
    vale_refeicao: float = 0.0
    plano_saude: float = 0.0
    pensao_alimenticia: float = 0.0
    emprestimo_consignado: float = 0.0

def calcular_inss(salario):
    # Tabela 2025 simplificada (valores fictícios)
    if salario <= 1518:
        return salario * 0.075
    elif salario <= 2793.88:
        return (salario * 0.09) - 22.77
    elif salario <= 4190.83:
        return (salario * 0.12) - 106.59
    elif salario <= 8157.41:
        return (salario * 0.14) - 190.4
    else:
        return 1906.04  # Teto do INSS
    
def calcular_irrf(salario, inss):
    # Dedução padrão IRRF (2025)
    deducao_padrao = 607.20

    # Se o valor do INSS for menor que a dedução padrão, usa-se a dedução padrão
    deducao_utilizada = deducao_padrao if inss < deducao_padrao else inss

    # Base de cálculo do IRRF
    base = salario - deducao_utilizada

    # Tabela 2025 simplificada
    if base <= 2428.80:
        return 0.0
    elif base <= 2826.65:
        return base * 0.075 - 182.16
    elif base <= 3751.05:
        return base * 0.15 - 394.16
    elif base <= 4664.68:
        return base * 0.225 - 675.49
    else:
        return base * 0.275 - 908.73

def calcular_folha(f: Funcionario):
    # VENCIMENTOS
    proventos = (
        f.salario_base +
        f.adicional_periculosidade +
        f.adicional_insalubridade +
        f.adicional_noturno +
        f.horas_extras_50 +
        f.horas_extras_100 +
        f.comissoes +
        f.premios +
        f.plr +
        f.ferias +
        f.decimo_terceiro
    )

    # DESCONTOS LEGAIS
    inss = calcular_inss(proventos)
    irrf = calcular_irrf(proventos, inss)

    # OUTROS DESCONTOS
    descontos = (
        inss +
        irrf +
        f.vale_transporte +
        f.vale_refeicao +
        f.plano_saude +
        f.pensao_alimenticia +
        f.emprestimo_consignado
    )

    # RESULTADOS
    liquido = proventos - descontos
    fgts = proventos * 0.08  # Apenas como exemplo de encargo
    custo_empresa = proventos + fgts

    return {
        "salario_bruto": round(proventos, 2),
        "inss": round(inss, 2),
        "irrf": round(irrf, 2),
        "total_descontos": round(descontos, 2),
        "salario_liquido": round(liquido, 2),
        "fgts": round(fgts, 2),
        "custo_empresa": round(custo_empresa, 2),
        "vale_transporte": round(f.vale_transporte, 2),
        "plano_saude": round(f.plano_saude, 2)
    }

def gerar_pdf_folha(funcionario: Funcionario, calculo: dict):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_title(f"Folha de Pagamento - {funcionario.nome}")
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, f"Folha de Pagamento", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Funcionário: {funcionario.nome}", ln=True)
    pdf.cell(0, 10, f"Matrícula: {funcionario.matricula}", ln=True)
    pdf.cell(0, 10, f"Cargo: {funcionario.cargo}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, f"Salário Base: R$ {funcionario.salario_base:.2f}", ln=True)
    pdf.cell(0, 10, f"Salário Bruto: R$ {calculo['salario_bruto']:.2f}", ln=True)
    pdf.cell(0, 10, f"Vale Transporte: R$ {calculo['vale_transporte']:.2f}", ln=True)
    pdf.cell(0, 10, f"Plano Saúde: R$ {calculo['plano_saude']:.2f}", ln=True)
    pdf.cell(0, 10, f"INSS: R$ {calculo['inss']:.2f}", ln=True)
    pdf.cell(0, 10, f"IRRF: R$ {calculo['irrf']:.2f}", ln=True)
    pdf.cell(0, 10, f"Total de Descontos: R$ {calculo['total_descontos']:.2f}", ln=True)
    pdf.cell(0, 10, f"Salário Líquido: R$ {calculo['salario_liquido']:.2f}", ln=True)
    pdf.cell(0, 10, f"FGTS (8%): R$ {calculo['fgts']:.2f}", ln=True)
    pdf.cell(0, 10, f"Custo Total da Empresa: R$ {calculo['custo_empresa']:.2f}", ln=True)

    caminho_pdf = f"./relatorios/folha_{funcionario.matricula}.pdf"
    pdf.output(caminho_pdf)

    # Salvar no histórico
    with open("relatorios.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            funcionario.nome,
            funcionario.matricula,
            funcionario.cargo,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            caminho_pdf
        ])

# funcionario = Funcionario(
#     nome=input('Nome: '),
#     matricula=input('Matrícula: '),
#     cargo=input('Cargo: '),
#     salario_base=float(input('Salário base: ')),
#     horas_extras_50=float(input('Horas Extras 50%: ')),
#     comissoes=float(input('Comissões: ')),
#     vale_transporte=float(input('Vale transporte: ')),
#     plano_saude=float(input('plano de saude: '))
# )

# resultado = calcular_folha(funcionario)
# print(resultado)

# gerar_pdf_folha(funcionario, resultado)

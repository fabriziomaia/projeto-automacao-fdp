from dataclasses import dataclass
from fpdf import FPDF
import csv
from datetime import datetime
import pandas as pd

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

class PDF(FPDF):
    def header(self):
        # Logo no canto superior esquerdo (ajuste o caminho e tamanho conforme necessário)
        self.image("logo.png", x=10, y=8, w=30)

        self.set_font("Arial", "B", 14)
        self.set_text_color(40, 40, 40)
        self.set_xy(50, 10)  # Move o cursor para a direita da logo
        self.cell(0, 10, "Decision - Desenvolvimento Humano & Organizacional", border=False, ln=True, align='C')
        self.set_draw_color(200, 200, 200)
        self.line(50, 20, 200, 20)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')


def gerar_pdf_folha(funcionario: Funcionario, calculo: dict):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Folha de Pagamento", ln=True, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0)
    pdf.cell(0, 8, "Dados do Funcionário:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Nome: {funcionario.nome}", ln=True)
    pdf.cell(0, 8, f"Matrícula: {funcionario.matricula}", ln=True)
    pdf.cell(0, 8, f"Cargo: {funcionario.cargo}", ln=True)
    pdf.ln(5)

    # Cabeçalho da tabela com Rubrica no início
    pdf.set_fill_color(230, 230, 250)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(30, 8, "Rubrica", border=1, fill=True)
    pdf.cell(70, 8, "Descrição", border=1, fill=True)
    pdf.cell(50, 8, "Valor (R$)", border=1, ln=True, fill=True)

    pdf.set_font("Arial", "", 12)
    def linha(rubrica, descricao, valor):
        pdf.cell(30, 8, rubrica, border=1)
        pdf.cell(70, 8, descricao, border=1)
        pdf.cell(50, 8, f"{valor:.2f}", border=1, ln=True)

    linha("", "Salário Base", funcionario.salario_base)
    linha("", "Salário Bruto", calculo['salario_bruto'])
    linha("", "Vale Transporte", calculo['vale_transporte'])
    linha("", "Plano de Saúde", calculo['plano_saude'])
    linha("", "INSS", calculo['inss'])
    linha("", "IRRF", calculo['irrf'])
    linha("", "Total de Descontos", calculo['total_descontos'])

    pdf.set_font("Arial", "B", 12)
    linha("", "Salário Líquido", calculo['salario_liquido'])
    pdf.set_font("Arial", "", 12)
    linha("", "FGTS (8%)", calculo['fgts'])
    linha("", "Custo Total da Empresa", calculo['custo_empresa'])

    caminho_pdf = f"./relatorios/folha_{funcionario.nome}.pdf"
    pdf.output(caminho_pdf)



    # Salvar no histórico
    with open("relatorios.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            funcionario.nome,
            funcionario.matricula,
            funcionario.cargo,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

def gerar_excel_folha(funcionario: Funcionario, calculo: dict):
    dados = {
        "Funcionário": [funcionario.nome],
        "Matrícula": [funcionario.matricula],
        "Cargo": [funcionario.cargo],
        "Salário Base": [funcionario.salario_base],
        "Salário Bruto": [calculo["salario_bruto"]],
        "Vale Transporte": [calculo["vale_transporte"]],
        "Plano Saúde": [calculo["plano_saude"]],
        "INSS": [calculo["inss"]],
        "IRRF": [calculo["irrf"]],
        "Total de Descontos": [calculo["total_descontos"]],
        "Salário Líquido": [calculo["salario_liquido"]],
        "FGTS (8%)": [calculo["fgts"]],
        "Custo Total Empresa": [calculo["custo_empresa"]],
        "Data": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    df = pd.DataFrame(dados)
    caminho_excel = f"./relatorios/folha_{funcionario.nome}.xlsx"
    df.to_excel(caminho_excel, index=False)
    
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

from flask import Flask, render_template, request, send_file
from folha import Funcionario, calcular_folha, gerar_pdf_folha
import os
import csv

app = Flask(__name__)
os.makedirs("relatorios", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    dados = request.form

    funcionario = Funcionario(
        nome=dados["nome"],
        matricula=dados["matricula"],
        cargo=dados["cargo"],
        salario_base=float(dados["salario_base"]),
        adicional_periculosidade=float(dados.get("adicional_periculosidade", 0)),
        adicional_insalubridade=float(dados.get("adicional_insalubridade", 0)),
        adicional_noturno=float(dados.get("adicional_noturno", 0)),
        horas_extras_50=float(dados.get("horas_extras_50", 0)),
        horas_extras_100=float(dados.get("horas_extras_100", 0)),
        comissoes=float(dados.get("comissoes", 0)),
        premios=float(dados.get("premios", 0)),
        plr=float(dados.get("plr", 0)),
        ferias=float(dados.get("ferias", 0)),
        decimo_terceiro=float(dados.get("decimo_terceiro", 0)),
        vale_transporte=float(dados.get("vale_transporte", 0)),
        vale_refeicao=float(dados.get("vale_refeicao", 0)),
        plano_saude=float(dados.get("plano_saude", 0)),
        pensao_alimenticia=float(dados.get("pensao_alimenticia", 0)),
        emprestimo_consignado=float(dados.get("emprestimo_consignado", 0)),
    )

    resultado = calcular_folha(funcionario)
    gerar_pdf_folha(funcionario, resultado)      
    return send_file(f"./relatorios/folha_{funcionario.matricula}.pdf", as_attachment=True)

@app.route("/relatorios")
def relatorios():
    registros = []
    if os.path.exists("relatorios.csv"):
        with open("relatorios.csv", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                registros.append({
                    "nome": row[0],
                    "matricula": row[1],
                    "cargo": row[2],
                    "data": row[3],
                    "caminho": row[4],
                })
    return render_template("relatorios.html", relatorios=registros)

@app.route("/download/<path:filename>")
def download(filename):
    caminho = os.path.join("relatorios", filename)
    return send_file(caminho, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

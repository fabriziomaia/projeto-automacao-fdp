require("dotenv").config();
const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const PDFDocument = require("pdfkit");

const app = express();
app.use(cors());
app.use(express.json());

// Configuração do banco de dados
const db = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
});

db.connect(err => {
    if (err) throw err;
    console.log("Banco de dados conectado!");
});

// Rota para buscar todos os funcionários
app.get("/funcionarios", (req, res) => {
    db.query("SELECT * FROM funcionarios", (err, result) => {
        if (err) throw err;
        res.json(result);
    });
});

// Rota para calcular a folha de pagamento de um funcionário
app.get("/calcular-folha/:id", (req, res) => {
    const funcionarioId = req.params.id;

    db.query("SELECT * FROM funcionarios WHERE id = ?", [funcionarioId], (err, result) => {
        if (err) throw err;

        if (result.length > 0) {
            const funcionario = result[0];
            const salarioBase = funcionario.salario;
            const descontos = salarioBase * 0.1; // 10% de desconto
            const beneficios = 500; // Exemplo de benefício fixo

            const salarioLiquido = salarioBase - descontos + beneficios;

            res.json({
                nome: funcionario.nome,
                cargo: funcionario.cargo,
                salarioBase,
                descontos,
                beneficios,
                salarioLiquido
            });
        } else {
            res.status(404).json({ message: "Funcionário não encontrado." });
        }
    });
});

// Rota para adicionar um novo funcionário
app.post("/funcionarios", (req, res) => {
    const { nome, cargo, salario, data_contratacao } = req.body;

    const query = "INSERT INTO funcionarios (nome, cargo, salario, data_contratacao) VALUES (?, ?, ?, ?)";
    db.query(query, [nome, cargo, salario, data_contratacao], (err, result) => {
        if (err) throw err;
        res.status(201).json({ message: "Funcionário cadastrado com sucesso!" });
    });
});

// Rota para editar um funcionário
app.put("/funcionarios/:id", (req, res) => {
    const { id } = req.params;
    const { nome, cargo, salario, data_contratacao } = req.body;

    const query = "UPDATE funcionarios SET nome = ?, cargo = ?, salario = ?, data_contratacao = ? WHERE id = ?";
    db.query(query, [nome, cargo, salario, data_contratacao, id], (err, result) => {
        if (err) {
            return res.status(500).json({ error: "Erro ao atualizar funcionário" });
        }
        res.json({ message: "Funcionário atualizado com sucesso!" });
    });
});

// Rota para gerar o relatório de funcionários em PDF
app.get("/relatorio-funcionarios", (req, res) => {
    console.log("Rota /relatorio-funcionarios chamada");

    const filePath = path.join(__dirname, "relatorios", "relatorio-funcionarios.pdf");
    const dir = path.join(__dirname, "relatorios");

    if (!fs.existsSync(dir)) {
        console.log("Criando diretório...");
        fs.mkdirSync(dir);
    }

    const doc = new PDFDocument();
    doc.pipe(fs.createWriteStream(filePath));

    doc.fontSize(18).text("Relatório de Funcionários", { align: "center" });
    doc.moveDown();
    doc.fontSize(12).text("ID | Nome | Cargo | Salário");
    doc.moveDown();

    db.query("SELECT * FROM funcionarios", (err, result) => {
        if (err) {
            console.error("Erro ao buscar funcionários:", err);
            return res.status(500).send("Erro no banco de dados");
        }

        result.forEach(funcionario => {
            doc.text(`${funcionario.id} | ${funcionario.nome} | ${funcionario.cargo} | R$ ${funcionario.salario}`);
        });

        doc.end();

        doc.on("finish", () => {
            console.log("PDF gerado com sucesso");

            if (fs.existsSync(filePath)) {
                console.log("Enviando o arquivo para o cliente...");
                res.download(filePath, "relatorio-funcionarios.pdf", err => {
                    if (err) {
                        console.error("Erro ao enviar o arquivo:", err);
                        return res.status(500).send("Erro ao enviar o arquivo");
                    }
                    console.log("Arquivo enviado com sucesso!");
                    fs.unlinkSync(filePath); // Exclui o arquivo após o envio
                });
            } else {
                console.log("Arquivo não encontrado!");
                return res.status(500).send("Erro ao encontrar o arquivo gerado");
            }
        });

        doc.on("error", error => {
            console.error("Erro ao gerar o PDF:", error);
            res.status(500).send("Erro ao gerar o relatório");
        });
    });
});

// Iniciar o servidor na porta 3001
app.listen(3001, () => {
    console.log("Servidor rodando em http://localhost:3001");
});

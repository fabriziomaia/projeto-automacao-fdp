require("dotenv").config();
const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

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

// Iniciar o servidor
app.listen(3001, () => {
    console.log("Servidor rodando em http://localhost:3001");
});

// Rota para calcular a folha de pagamento de um funcionário
app.get("/calcular-folha/:id", (req, res) => {
    const funcionarioId = req.params.id;

    // Buscar o funcionário no banco
    db.query("SELECT * FROM funcionarios WHERE id = ?", [funcionarioId], (err, result) => {
        if (err) throw err;

        if (result.length > 0) {
            const funcionario = result[0];

            // Exemplo simples de cálculo de salário
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

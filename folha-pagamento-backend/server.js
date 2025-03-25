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

import React, { useState } from "react";
import axios from "axios";

function CadastrarFuncionario() {
    const [nome, setNome] = useState("");
    const [cargo, setCargo] = useState("");
    const [salario, setSalario] = useState("");
    const [dataContratacao, setDataContratacao] = useState("");

    const cadastrarFuncionario = async () => {
        const novoFuncionario = {
            nome,
            cargo,
            salario,
            data_contratacao: dataContratacao,
        };

        try {
            const response = await axios.post("http://localhost:3001/funcionarios", novoFuncionario);
            alert(response.data.message);
        } catch (error) {
            console.error("Erro ao cadastrar funcionário", error);
            alert("Erro ao cadastrar funcionário.");
        }
    };

    return (
        <div>
            <h2>Cadastrar Funcionário</h2>
            <input
                type="text"
                placeholder="Nome"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
            />
            <input
                type="text"
                placeholder="Cargo"
                value={cargo}
                onChange={(e) => setCargo(e.target.value)}
            />
            <input
                type="number"
                placeholder="Salário"
                value={salario}
                onChange={(e) => setSalario(e.target.value)}
            />
            <input
                type="date"
                value={dataContratacao}
                onChange={(e) => setDataContratacao(e.target.value)}
            />
            <button onClick={cadastrarFuncionario}>Cadastrar</button>
        </div>
    );
}

export default CadastrarFuncionario;

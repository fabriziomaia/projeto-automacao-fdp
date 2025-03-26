import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

function EditarFuncionario() {
    const { id } = useParams(); // Captura o ID da URL
    const navigate = useNavigate();
    const [funcionario, setFuncionario] = useState({
        nome: "",
        cargo: "",
        salario: "",
        data_contratacao: ""
    });

    // Busca os dados do funcionário ao carregar a página
    useEffect(() => {
        axios.get(`http://localhost:3001/funcionarios/${id}`)
            .then(response => setFuncionario(response.data))
            .catch(error => console.error("Erro ao buscar funcionário:", error));
    }, [id]);

    // Atualiza os dados no backend
    const handleSubmit = (e) => {
        e.preventDefault();
        axios.put(`http://localhost:3001/funcionarios/${id}`, funcionario)
            .then(() => {
                alert("Funcionário atualizado com sucesso!");
                navigate("/"); // Volta para a lista de funcionários
            })
            .catch(error => console.error("Erro ao atualizar funcionário:", error));
    };

    return (
        <div>
            <h2>Editar Funcionário</h2>
            <form onSubmit={handleSubmit}>
                <label>Nome:</label>
                <input type="text" value={funcionario.nome} onChange={e => setFuncionario({...funcionario, nome: e.target.value})} />

                <label>Cargo:</label>
                <input type="text" value={funcionario.cargo} onChange={e => setFuncionario({...funcionario, cargo: e.target.value})} />

                <label>Salário:</label>
                <input type="number" value={funcionario.salario} onChange={e => setFuncionario({...funcionario, salario: e.target.value})} />

                <label>Data de Contratação:</label>
                <input type="date" value={funcionario.data_contratacao} onChange={e => setFuncionario({...funcionario, data_contratacao: e.target.value})} />

                <button type="submit">Salvar Alterações</button>
            </form>
        </div>
    );
}

export default EditarFuncionario;

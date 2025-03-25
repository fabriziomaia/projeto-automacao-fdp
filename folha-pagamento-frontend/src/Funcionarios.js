import React, { useEffect, useState } from "react";
import axios from "axios";

function Funcionarios() {
    const [funcionarios, setFuncionarios] = useState([]);

    useEffect(() => {
        axios.get("http://localhost:3001/funcionarios")
            .then(response => setFuncionarios(response.data))
            .catch(error => console.error("Erro ao buscar funcionários", error));
    }, []);

    return (
        <div>
            <h2>Funcionários</h2>
            <ul>
                {funcionarios.map(func => (
                    <li key={func.id}>
                        {func.nome} - {func.cargo} - R$ {func.salario}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Funcionarios;

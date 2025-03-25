import React, { useState } from "react";
import axios from "axios";

function CalcularFolha() {
    const [id, setId] = useState("");
    const [resultado, setResultado] = useState(null);

    const calcularFolha = async () => {
        try {
            const response = await axios.get(`http://localhost:3001/calcular-folha/${id}`);
            setResultado(response.data);
        } catch (error) {
            console.error("Erro ao calcular folha:", error);
            alert("Funcionário não encontrado.");
        }
    };

    return (
        <div>
            <h2>Cálculo de Folha de Pagamento</h2>
            <input
                type="number"
                placeholder="Digite o ID do Funcionário"
                value={id}
                onChange={(e) => setId(e.target.value)}
            />
            <button onClick={calcularFolha}>Calcular Folha</button>

            {resultado && (
                <div>
                    <h3>Resultado</h3>
                    <p>Nome: {resultado.nome}</p>
                    <p>Cargo: {resultado.cargo}</p>
                    <p>Salário Base: R$ {resultado.salarioBase}</p>
                    <p>Descontos: R$ {resultado.descontos}</p>
                    <p>Benefícios: R$ {resultado.beneficios}</p>
                    <p>Salário Líquido: R$ {resultado.salarioLiquido}</p>
                </div>
            )}
        </div>
    );
}

export default CalcularFolha;

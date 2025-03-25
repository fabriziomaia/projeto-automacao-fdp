import React from "react";
import axios from "axios";

function Relatorio() {
    const gerarRelatorio = async () => {
        try {
            const response = await axios.get("http://localhost:3001/relatorio-funcionarios", {
                responseType: "blob", // Definindo o tipo de resposta como blob (arquivo)
            });

            // Criar um link temporário para baixar o arquivo
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'relatorio-funcionarios.pdf');
            document.body.appendChild(link);
            link.click();
        } catch (error) {
            console.error("Erro ao gerar relatório:", error);
            alert("Erro ao gerar o relatório.");
        }
    };

    return (
        <div>
            <button onClick={gerarRelatorio}>Gerar Relatório de Funcionários</button>
        </div>
    );
}

export default Relatorio;

import React from "react";
import Funcionarios from "./Funcionarios";
import CalcularFolha from "./CalcularFolha";
import CadastrarFuncionario from "./CadastrarFuncionario";
import Relatorio from "./Relatorio";

function App() {
    return (
        <div>
            <h1>Folha de Pagamento</h1>
            <Funcionarios />
            <CalcularFolha />
            <CadastrarFuncionario />
            <Relatorio />
        </div>
    );
}

export default App;

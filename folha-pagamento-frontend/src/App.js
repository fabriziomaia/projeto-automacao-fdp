import React from "react";
import Funcionarios from "./Funcionarios";
import CalcularFolha from "./CalcularFolha";
import CadastrarFuncionario from "./CadastrarFuncionario";

function App() {
    return (
        <div>
            <h1>Folha de Pagamento</h1>
            <Funcionarios />
            <CalcularFolha />
            <CadastrarFuncionario />
        </div>
    );
}

export default App;

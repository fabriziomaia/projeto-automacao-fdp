import React from "react";
import Funcionarios from "./Funcionarios";
import CalcularFolha from "./CalcularFolha";

function App() {
    return (
        <div>
            <h1>Folha de Pagamento</h1>
            <Funcionarios />
            <CalcularFolha />
        </div>
    );
}

export default App;

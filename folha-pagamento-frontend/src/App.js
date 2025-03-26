import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Funcionarios from "./Funcionarios";
import CalcularFolha from "./CalcularFolha";
import CadastrarFuncionario from "./CadastrarFuncionario";
import Relatorio from "./Relatorio";
import EditarFuncionario from "./EditarFuncionario"; // A rota de edição

function App() {
    return (
        <Router>
            <div>
                <h1>Folha de Pagamento</h1>
                {/* Menu de navegação */}
                <nav>
                    <ul>
                        <li><Link to="/">Funcionários</Link></li>
                        <li><Link to="/calcular/1">Calcular Folha</Link></li> {/* Aqui você pode alterar o "1" para um ID válido */}
                        <li><Link to="/cadastrar">Cadastrar Funcionário</Link></li>
                        <li><Link to="/relatorio">Relatório</Link></li>
                    </ul>
                </nav>

                {/* Definição das Rotas */}
                <Routes>
                    <Route path="/" element={<Funcionarios />} />
                    <Route path="/calcular/:id" element={<CalcularFolha />} />
                    <Route path="/cadastrar" element={<CadastrarFuncionario />} />
                    <Route path="/relatorio" element={<Relatorio />} />
                    <Route path="/editar/:id" element={<EditarFuncionario />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;

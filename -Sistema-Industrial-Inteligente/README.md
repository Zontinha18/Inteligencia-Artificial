🏭 Industrial System

> **Projeto Acadêmico — Sistema Inteligente para Classificação e Gestão Industrial**

O **Industrial System** é um sistema inteligente de **análise e gerenciamento de setores industriais**, desenvolvido com **Python (Flask)** no backend e **React (Vite)** no frontend.  
Seu principal objetivo é **classificar automaticamente produtos por setor com base em sua composição**, além de **gerenciar empresas e departamentos** em um ambiente intuitivo e totalmente integrado.

---

📘 Sobre o Projeto

O projeto foi desenvolvido com foco em:
- Estruturação **modular** e **escalável**.
- Integração completa entre **backend e frontend**.
- Uso de **inteligência artificial baseada em regras (sistema especialista)**.
- Padrão de arquitetura **MVC (Model-View-Controller)** para clareza e organização.

---

🎯 Objetivos do Sistema

### 🎓 Objetivo Geral
Automatizar a **análise, categorização e gerenciamento de produtos industriais**, criando uma base inteligente de decisão para empresas do setor.

🎯 Objetivos Específicos
- Implementar um **backend com sistema especialista** baseado em inferências lógicas.  
- Desenvolver um **frontend interativo**, moderno e responsivo.  
- Garantir comunicação eficiente entre camadas via **API REST**.  
- Organizar o código em conformidade com o padrão **MVC**.  
- Oferecer documentação detalhada para **instalação e execução independente** do sistema.

---

🧠 Funcionalidades Principais

| Funcionalidade | Descrição |
|----------------|------------|
| 🧩 Classificação Inteligente | Identifica e classifica produtos automaticamente conforme sua composição. |
| 🏢 Gestão de Empresas | Permite cadastrar e gerenciar empresas e seus departamentos. |
| ⚙️ Integração Completa | Comunicação direta entre backend Flask e frontend React. |
| 📊 Interface Responsiva | Interface moderna, desenvolvida com TailwindCSS e React. |
| 🧠 Sistema Especialista | Lógica baseada em regras para tomada de decisões automáticas. |
| 🐳 Suporte Docker | Permite execução isolada e portável em qualquer ambiente. |

---

⚙️ Estrutura do Projeto

industrial-system/
```text
industrial-system/
├── backend/
│   ├── app.py                # Aplicação principal (API Flask)
│   ├── models.py             # Modelos e classes de dados
│   ├── expert_system.py      # Lógica do sistema especialista
│   ├── config.py             # Configurações gerais (banco, variáveis, etc.)
│   ├── requirements.txt      # Dependências do backend
│   └── Dockerfile            # Configuração Docker do backend
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes reutilizáveis
│   │   ├── pages/            # Páginas principais do sistema
│   │   ├── services/         # Comunicação com o backend (API)
│   │   ├── assets/           # Imagens, ícones e arquivos estáticos
│   │   └── App.jsx           # Ponto de entrada do frontend
│   ├── package.json          # Dependências do React
│   └── vite.config.js        # Configuração do Vite
│
└── README.md                 # Documentação oficial do projeto

```` 

🧩 Arquitetura MVC


**Resumo das camadas MVC:**

| Camada      | Descrição                                           | Arquivos / Pastas Principais                         |
|------------|----------------------------------------------------|-----------------------------------------------------|
| **Model**   | Regras de negócio e estrutura dos dados           | `backend/models.py`                                 |
| **View**    | Interface do usuário e exibição de informações   | `frontend/src/pages`, `frontend/src/components`    |
| **Controller** | Comunicação entre usuário e lógica do sistema | `backend/app.py`, `backend/expert_system.py`, `frontend/src/services` |


---

💻 Tecnologias Utilizadas

🔹**Backend**
- **Python 3.x**
- **Flask**
- **Sistema especialista baseado em regras**
- **Docker**

🔹 **Frontend**
- **React + Vite**
- **TailwindCSS**
- **Axios**
- **Shadcn/UI**

---

🚀 Guia Completo de Instalação e Execução

Este guia garante que o projeto rode em **qualquer computador**, mesmo fora da faculdade ou da máquina principal.

---

🔧 Pré-requisitos

Antes de começar, certifique-se de ter instalado:
- [Python 3.x](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/)
- [npm](https://www.npmjs.com/)
- (Opcional) [Docker](https://www.docker.com/)

---

🧾 Passo a Passo — Rodando o Projeto Localmente

1️⃣ Clonar o repositório

git clone https://github.com/PauloBumba/-Sistema-Industrial-Inteligente.git
cd industrial-system

---

2️⃣ Configurar o Backend (Flask)

cd backend
pip install -r requirements.txt
python app.py

---

3️⃣ Configurar o Frontend (React)

cd ../frontend
npm install
npm run dev

O frontend será iniciado em: http://localhost:5173

---

4️⃣ Testar o sistema

Certifique-se de que ambos os servidores (frontend e backend) estão ativos.

Acesse o endereço do frontend no navegador:
👉 http://localhost:5173

Interaja com o sistema, cadastre produtos e veja as classificações automáticas.

---

🧱 Executando com Docker (opcional)

Caso prefira rodar via Docker (sem precisar instalar dependências):

# No diretório raiz do projeto
docker-compose up --build

Isso iniciará automaticamente o backend e o frontend em containers isolados.

---

👨‍💻 Equipe de Desenvolvimento

Paulo Mario Bumba        |          
Leonardo Meimberg Zonta  |         
Kaua Camargo             |           
Alexandre José Ribeiro   |  

---

🧾 Licença

Este projeto foi desenvolvido exclusivamente para fins acadêmicos, sem fins comerciais.
Todos os direitos reservados à equipe de desenvolvimento.

---

💬 Considerações Finais

O Industrial System representa um avanço no contexto de automação e inteligência aplicada à gestão industrial.
Combinando um backend inteligente e um frontend moderno, o projeto foi planejado para:

- Ser fácil de instalar e executar.
- Possuir documentação completa e didática.
- Servir como base para futuras expansões e integrações empresariais.

---

🧭 Links Úteis

📘 Documentação do Flask

⚛️ Documentação do React

🐳 Guia Docker



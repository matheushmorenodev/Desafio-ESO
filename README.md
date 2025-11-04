# Desafio Técnico - Sistema ESO (Processo Seletivo)

Esta é uma aplicação web full-stack (Frontend + Backend) que implementa uma loja de cosméticos do Fortnite. O projeto foi desenvolvido conforme os requisitos do processo seletivo e está **100% implantado  na nuvem**.

---

## 🚀 Links da Aplicação (Deploy)

* **Frontend (React):** [https://desafio-eso.vercel.app](https://desafio-eso.vercel.app)
* **Backend (FastAPI):** [https://eso-api.onrender.com](https://eso-api.onrender.com)
* **(Endpoint de Teste):** [https://eso-api.onrender.com/api/cosmetics?limit=1](https://eso-api.onrender.com/api/cosmetics?limit=1)

*(**Nota Importante:** O plano gratuito do Render "adormece" a API após 15 minutos de inatividade. O primeiro carregamento do catálogo ou o primeiro login podem demorar de **30 a 50 segundos** enquanto o servidor "acorda". Após a primeira requisição, a aplicação volta à velocidade normal.)*

---

## 🛠️ Tecnologias Utilizadas

* **Frontend:** React 20, Vite, React Router, Axios, Context API.
* **Backend:** Python 3.11, FastAPI, SQLAlchemy, JWT (Passlib).
* **Banco de Dados:** PostgreSQL (Hospedado no Render).
* **Plataforma de Deploy:**
    * **Frontend:** Vercel (CI/CD a partir do GitHub).
    * **Backend:** Render (Hospedado como um Web Service).

---

## 🏛️ Decisões Técnicas e Arquitetura

Com base nos requisitos do PDF sobre "Organização, clareza e simplicidade do código", as seguintes decisões foram tomadas:

### Backend (Render)

* **Arquitetura Limpa:** A API utiliza um padrão de **Repositório** para desacoplar a lógica de negócio (nos "routers") da lógica de acesso ao banco de dados (nos "repositórios").
* **Servidor de Produção:** A API é servida usando **Gunicorn** com workers `uvicorn` e a flag `--preload` para gerenciar a inicialização de múltiplos workers sem conflitos de banco de dados (`deadlock`).
* **Sincronização Automatizada (Lifespan):**
    1.  **"Seeding" (População):** Para contornar o limite de 512MB de RAM do Render, o banco de dados PostgreSQL foi populado ("semeado") manualmente uma vez com os +13.000 cosméticos usando um script local (`seed_prod_db.py`).
    2.  **Atualização da Loja:** A API usa o `lifespan` do FastAPI para **atualizar a loja automaticamente** (`update_shop_status`) toda vez que o servidor inicia (ou "acorda"). Isso garante que os dados de preço e status (`is_on_sale`) estejam sempre corretos e ao vivo, sem necessidade de CRON.
* **Segurança (CORS):** O `CORSMiddleware` do FastAPI foi configurado para aceitar requisições apenas dos domínios de produção do Vercel (`desafio-eso.vercel.app`) e do `localhost` (para desenvolvimento).

### Frontend (Vercel)

* **Gerenciamento de Estado Global:** O estado global (usuário, saldo de V-Bucks e inventário) é gerenciado centralmente pelo **`AuthContext`** (Context API).
* **Experiência de Usuário (UX) Reativa:** Quando um usuário compra ou devolve um item, o `AuthContext` é atualizado (o saldo de V-Bucks e o inventário). Isso faz com que todos os componentes (Navbar, Catálogo e Painel de Detalhes) **atualizem instantaneamente**, sem a necessidade de o usuário recarregar a página (F5).
* **Refatoração:** Componentes de UI reutilizáveis (como `Button.jsx` e `Input.jsx`) foram criados para manter o código das páginas (como `Login.jsx`) limpo e fácil de manter.
* **Rotas Protegidas:** O `ProtectedRoute.jsx` protege rotas privadas (como `/profile`) e o `get_optional_current_user` no backend permite que rotas públicas (como `/cosmetics`) mostrem informações "bônus" (como `is_acquired`) se o usuário estiver logado.

---
*(Nota: O setup de desenvolvimento local anterior (com Docker Compose para MySQL) foi adaptado para o deploy de produção (PostgreSQL) para atender ao requisito de um link de "deploy" funcional.)*

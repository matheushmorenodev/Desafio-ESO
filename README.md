# Desafio Técnico - Sistema ESO (Processo Seletivo)

Esta é uma aplicação web full-stack (Frontend + Backend) que implementa uma loja de cosméticos do Fortnite, conforme os requisitos.

A aplicação é 100% orquestrada com Docker Compose em uma arquitetura de "dois terminais", separando os serviços de frontend e backend.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.11, FastAPI, SQLAlchemy, JWT (Passlib), PyMySQL (via `mysqlclient`).
* **Frontend:** React 20, Vite, React Router, Axios, Context API.
* **Banco de Dados:** MySQL 8.0
* **Infraestrutura:** Docker & Docker Compose

---

## 🚀 Como Rodar a Aplicação (Método de 2 Terminais)

Você precisará de dois terminais abertos para rodar o backend e o frontend simultaneamente.

### Pré-requisitos
* Docker e Docker Compose instalados.
* Git.

### 1. Clonar o Repositório
```bash
git clone <url-do-seu-repositorio>
cd desafio-eso
```
### 2. Terminal 1
```bash
cd backend
docker-compose up --build
Espere até aparecer a seguinte mensagem:
eso_api_service | Sincronização da loja na inicialização concluída.
eso_api_service | INFO:    Application startup complete.
eso_api_service | INFO:    Uvicorn running on [http://0.0.0.0:8000](http://0.0.0.0:8000) (Press CTRL+C to quit)
```
### 3. Terminal 2
```bash
cd frontend
docker-compose up --build
Espere até aparecer a seguinte mensagem:
eso_frontend_service | > Local: http://localhost:5173/
```
### 4. Para acessar a aplicação
```bash
http://localhost:5173
```
---

## Endpoints da API

A API estará disponível em `http://localhost:8000`. Todos os endpoints principais são prefixados com `/api/`.

Endpoints marcados com **[PROTEGIDO]** requerem um `Bearer Token` no cabeçalho `Authorization`.

### Autenticação (`/api/auth`)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Registra um novo usuário. Requer `email` e `password` (com regras de complexidade). Retorna o usuário criado com 10.000 V-Bucks. |
| `POST` | `/api/auth/login` | Autentica um usuário (usando `username` e `password` em `x-www-form-urlencoded`). Retorna um token JWT. |

### Cosméticos (`/api/cosmetics`)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/cosmetics` | Lista todos os cosméticos com filtros e paginação. É público, mas exibe o status `is_acquired` se um token de login for fornecido. |
| `GET` | `/api/cosmetics/{cosmetic_id}` | Retorna os detalhes de um cosmético específico. Também é público, mas exibe `is_acquired` se logado. |
| `POST` | `/api/cosmetics/{cosmetic_id}/buy` | **[PROTEGIDO]** Compra um item cosmético individual. Retorna o perfil do usuário atualizado (com novo saldo). |
| `POST` | `/api/cosmetics/{cosmetic_id}/return` | **[PROTEGIDO]** Devolve um item cosmético individual. Retorna o perfil do usuário atualizado (com novo saldo). |

### Loja e Bundles (`/api/shop`)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/shop` | Retorna os dados da loja *ao vivo* da API do Fortnite, enriquecidos com o status `is_acquired` do usuário (se logado). |
| `POST` | `/api/shop/buy` | **[PROTEGIDO]** Compra uma oferta da loja (item único ou bundle) usando o `offerId`. Retorna o perfil do usuário atualizado. |

### Perfil do Usuário (`/api/profile/me`)

*Todos os endpoints nesta seção são protegidos e requerem um token JWT.*

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/profile/me` | Retorna os dados do usuário logado (incluindo `id`, `email`, e `vbucks`). |
| `GET` | `/api/profile/me/inventory` | Retorna o inventário de cosméticos (lista de objetos `CosmeticPublic`) do usuário logado. |
| `GET` | `/api/profile/me/history` | Retorna o histórico de transações (compras/devoluções) do usuário logado, com os dados dos cosméticos aninhados. |

### Usuários Públicos (`/api/users`)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/users` | Retorna uma lista pública e paginada de todos os usuários registrados. |
| `GET` | `/api/users/{user_id}/inventory` | Retorna o inventário público de cosméticos de um usuário específico. |

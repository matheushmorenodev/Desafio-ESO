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
# 1. Imagem base
FROM python:3.11-slim

# 2. Diretório de trabalho
WORKDIR /app

# 3. Variáveis
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Instala dependências do sistema (ADICIONA 'netcat-openbsd')
RUN apt-get update \
    && apt-get -y install default-libmysqlclient-dev build-essential pkg-config netcat-openbsd \
    && apt-get clean

# 5. Copia os requisitos
COPY requirements.txt .

# 6. Limpa e instala libs do Python
RUN pip install --upgrade pip \
    && pip uninstall -y bcrypt py-bcrypt \
    && pip install --no-cache-dir -r requirements.txt

# 7. Copia o script de espera
COPY ./scripts/wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# 8. Copia o código da aplicação
COPY ./app ./app

# 9. Expõe a porta
EXPOSE 8000

# 10. Comando final (MUDADO)
#    Ele roda o script de espera, e o script de espera
#    então roda o uvicorn.
#    As variáveis 'db' e '3306' vêm do .env e docker-compose
CMD ["/wait-for-db.sh", "db", "3306", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
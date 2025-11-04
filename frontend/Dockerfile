# 1. Imagem base do Node.js (versão 20, como o Vite pedia)
FROM node:20-alpine

# 2. Define o diretório de trabalho
WORKDIR /app

# 3. Copia o package.json (e lock)
COPY package.json package-lock.json ./

# 4. Instala as dependências
RUN npm install

# 5. Copia o resto do código
COPY . .

# 6. Expõe a porta do Vite
EXPOSE 5173

# 7. Comando para iniciar (com --host 0.0.0.0)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
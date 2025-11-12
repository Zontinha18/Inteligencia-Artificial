FROM node:20-alpine  

# Atualiza o npm e instala o yarn globalmente
RUN npm install -g npm@10.9.0 yarn --force

# Define diretório de trabalho
WORKDIR /app

# Copia package.json e package-lock.json
COPY package*.json ./

# Instala dependências
RUN yarn install --frozen-lockfile

# Copia o restante do código
COPY . .

# Expose port
EXPOSE 5173

# Comando para rodar a aplicação com host 0.0.0.0
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
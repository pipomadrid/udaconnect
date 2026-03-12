FROM node:24.1.0-alpine

WORKDIR /app

COPY package.json ./

RUN npm install
RUN npm install react-scripts@5.0.1 -g

COPY . ./


# Establecer variables para no abrir navegador
ENV BROWSER=none
ENV HOST=0.0.0.0

EXPOSE 3000

CMD ["npm", "start"]


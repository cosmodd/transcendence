FROM node:current-alpine

WORKDIR /app

ENTRYPOINT npm i && npm run start:dev
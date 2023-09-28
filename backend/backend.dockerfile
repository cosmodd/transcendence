FROM node:current-alpine

RUN npm install -g @nestjs/cli

EXPOSE 3000

WORKDIR /app

ENTRYPOINT ["/bin/sh", "-c", "npm install && npm run build && npm run start:dev"]

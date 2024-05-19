FROM node:lts-alpine as build-stage

WORKDIR /app

COPY . .
RUN npm install
RUN npm run build

FROM nginx:stable-alpine as deploy-stage

COPY --from=build-stage /app/build /var/www/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
RUN chown -R nginx:nginx /var/www/html

RUN apk update && apk add openssl
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes \
	-subj "/C=FR/ST=Nice/L=Nice/O=42 Nice/OU=pforesti/CN=pforesti"

ENTRYPOINT [ "nginx", "-g", "daemon off;" ]
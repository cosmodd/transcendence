FROM node:lts-alpine as build-stage

WORKDIR /app

COPY . .
RUN npm install
RUN npm run build

FROM nginx:stable-alpine as deploy-stage

COPY --from=build-stage /app/build /var/www/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
RUN chown -R nginx:nginx /var/www/html

ENTRYPOINT [ "nginx", "-g", "daemon off;" ]
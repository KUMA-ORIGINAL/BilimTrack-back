FROM nginx:1.26.0

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY ./nginx_entrypoint.sh /docker-entrypoint.d/.
RUN chmod +x /docker-entrypoint.d/nginx_entrypoint.sh
RUN apt update
RUN apt install certbot python3-certbot-nginx -y
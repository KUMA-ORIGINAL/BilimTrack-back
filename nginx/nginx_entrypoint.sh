#!/bin/sh

get_certs_lower=$(echo "$GET_CERTS" | tr '[:upper:]' '[:lower:]')

if [ "$get_certs_lower" = "true" ]; then
    echo "🆕 Получаем или обновляем сертификаты для доменов: $DOMAINS..."

    # собираем список аргументов -d
    domains_args=""
    for domain in $DOMAINS; do
        domains_args="$domains_args -d $domain"
    done

    certbot --nginx \
        --email "$CERTBOT_EMAIL" \
        --agree-tos \
        --no-eff-email \
        --non-interactive \
        --expand \
        $domains_args

    nginx -s stop
    sleep 2
fi

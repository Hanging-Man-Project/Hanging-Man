FROM nginx:1.25-alpine

# Supprimer la config par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Copier notre config
COPY nginx.conf /etc/nginx/nginx.conf

# Créer un utilisateur non-root
RUN adduser -D nginxuser \
    # Créer dossiers nginx accessibles
    && mkdir -p /var/cache/nginx /var/run /tmp/nginx-run \
    && chown -R nginxuser:nginxuser /var/cache/nginx /var/run /tmp/nginx-run

USER nginxuser

EXPOSE 8080

# Lancer nginx avec le pid dans /tmp/nginx-run
CMD ["nginx", "-g", "daemon off; pid /tmp/nginx-run/nginx.pid;"]
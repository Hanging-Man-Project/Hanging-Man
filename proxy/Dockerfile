FROM nginx:1.25-alpine

# Ajouter un utilisateur non-root
RUN adduser -D nginxuser

# Copier notre configuration
COPY nginx.conf /etc/nginx/nginx.conf

USER nginxuser

EXPOSE 80

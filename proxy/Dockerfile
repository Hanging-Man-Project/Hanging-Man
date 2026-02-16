FROM nginx:1.25-alpine

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create a non-root user
RUN adduser -D nginxuser \
    # Create accessible nginx folders
    && mkdir -p /var/cache/nginx /var/run /tmp/nginx-run \
    && chown -R nginxuser:nginxuser /var/cache/nginx /var/run /tmp/nginx-run

USER nginxuser

EXPOSE 8080

# Start nginx with the pid in /tmp/nginx-run
CMD ["nginx", "-g", "daemon off; pid /tmp/nginx-run/nginx.pid;"]
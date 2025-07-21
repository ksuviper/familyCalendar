# Use Alpine 3.20 as the base image
FROM alpine:3.20

# Install Nginx, PHP 8.2, Git, and dependencies
RUN apk update && apk add --no-cache \
    nginx \
    php82 \
    php82-fpm \
    php82-sqlite3 \
    sqlite \
    curl \
    git

# Set working directory
WORKDIR /app

# Create directories for Nginx and PHP-FPM
RUN mkdir -p /run/nginx /run/php

# Configure PHP-FPM
RUN sed -i 's|;listen = 127.0.0.1:9000|listen = /run/php/php-fpm82.sock|' /etc/php82/php-fpm.d/www.conf \
    && sed -i 's|;listen.owner = nobody|listen.owner = nginx|' /etc/php82/php-fpm.d/www.conf \
    && sed -i 's|;listen.group = nobody|listen.group = nginx|' /etc/php82/php-fpm.d/www.conf

# Clone the GitHub repository
RUN git clone https://github.com/ksuviper/familyCalendar.git ./

# Copy Nginx configuration
#COPY nginx.conf /etc/nginx/nginx.conf

# Set permissions
#RUN chown -R nginx:nginx /var/www/html \
#    && chmod -R 644 /var/www/html/* \
#    && chmod 664 /var/www/html/family_calendar.db 2>/dev/null || true

# Expose port 80
EXPOSE 80

# Start PHP-FPM and Nginx
CMD ["/bin/sh", "-c", "php-fpm82 -F & nginx -g 'daemon off;'"]
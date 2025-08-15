# Step 1: Aufbauen der Vite app
FROM node:18 AS builder
WORKDIR /app

COPY package.json package-lock.json ./  
RUN npm install                        

COPY . .

# No build arguments needed - using Nginx proxy

RUN npm run build          

# Step 2: Serve with Nginx
FROM nginx:stable-alpine

# Copy built app
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Create nginx user and set permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Set default environment variables
ENV SERVER_NAME=simplex4learning.disy.net
ENV BACKEND_HOST=backend
ENV BACKEND_PORT=8000
ENV PROXY_TIMEOUT=1800
ENV PROXY_PORT=80

EXPOSE $PROXY_PORT
CMD ["nginx", "-g", "daemon off;"]

# Stage 1: Build React using Node.js 22 minimal
FROM quay.io/fedora/nodejs-22-minimal:latest AS build

USER 1001

WORKDIR /app

COPY --chown=1001:1001 package*.json ./
RUN npm install

COPY --chown=1001:1001 ./ ./

# Generates static files in /app/dist
RUN npm run build


# Stage 2: Serve with unprivileged Nginx
FROM quay.io/nginx/nginx-unprivileged:alpine

COPY --chown=nginx:nginx --from=build /app/dist /usr/share/nginx/html

COPY --chown=nginx:nginx --from=build /app/nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]

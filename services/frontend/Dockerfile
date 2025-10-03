FROM node:22-slim AS builder

WORKDIR /app

# copy lockfile first to leverage docker cache
COPY package.json package-lock.json* ./

# install production deps (and dev deps needed for build)
RUN npm ci --no-audit --progress=false

# copy source and build
COPY . .
COPY .env.production .env.production

RUN npm run build

### Runtime image
FROM nginx:stable-alpine AS runner

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

COPY env.sh /docker-entrypoint.d/env.sh
RUN chmod +x /docker-entrypoint.d/env.sh

EXPOSE 80
FROM node:22-slim AS builder

WORKDIR /app

# copy lockfile first to leverage docker cache
COPY package.json package-lock.json* ./

# install production deps (and dev deps needed for build)
RUN npm ci --no-audit --progress=false

ENV VITE_BACKEND_URL="http://localhost:8000"

# copy source and build
COPY . .
RUN npm run build

### Runtime image
FROM nginx:stable-alpine AS runner

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

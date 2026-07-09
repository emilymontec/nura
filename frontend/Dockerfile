FROM node:20-alpine

WORKDIR /app

# Install pnpm using corepack
RUN corepack enable pnpm && corepack prepare pnpm@latest --activate

# Install dependencies
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

# Copy project
COPY . .

EXPOSE 5173

CMD ["pnpm", "run", "dev"]

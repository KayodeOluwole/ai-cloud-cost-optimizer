# --- Stage 1: Build React/Vite App ---
FROM node:18-alpine AS build

WORKDIR /app

# Copy only package files first (better caching)
COPY package.json package-lock.json* ./

RUN npm install

# Now copy the rest of the frontend source code
COPY . .

# Build Vite production files
RUN npm run build


# --- Stage 2: Serve with NGINX ---
FROM nginx:alpine

# Copy built frontend files from Stage 1
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

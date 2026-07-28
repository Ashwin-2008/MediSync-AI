FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Build the frontend
RUN npm run build

# Install serve to run the build
RUN npm install -g serve

CMD ["serve", "-s", "dist", "-l", "3000"]

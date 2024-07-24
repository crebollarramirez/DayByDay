# client/Dockerfile

# Use the official Node.js image.
FROM node:18 AS build

# Set the working directory.
WORKDIR /app

# Install dependencies.
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Copy the source code.
COPY . .

# Build the application.
RUN npm run build

# Use a lightweight web server to serve the static files.
FROM nginx:alpine

# Copy the build files from the previous stage.
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for the web server.
EXPOSE 80

# Start the Nginx server.
CMD ["nginx", "-g", "daemon off;"]
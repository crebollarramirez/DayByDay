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
# RUN npm run build
RUN npm install

COPY . .

ENV PORT=8080

# # Use a lightweight web server to serve the static files.
# FROM nginx:alpine

# # Copy the build files from the previous stage.
# COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for the web server.
EXPOSE 8080

# Start the Nginx server.
CMD ["npm", "start"]
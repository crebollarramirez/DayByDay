# server/Dockerfile

# Use the official Node.js image.
FROM node:18

# Set the working directory.
WORKDIR /app

# Install dependencies.
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Copy the source code.
COPY . .

# Expose port 5000 for the Node.js server.
EXPOSE 5000

# Start the Node.js server.
CMD ["node", "server.js"]
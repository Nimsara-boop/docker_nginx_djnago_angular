FROM node:18-alpine AS build
RUN mkdir/app
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

FROM node:18-alpine 
WORKDIR /app
COPY --from=bui;ld /usr/local/lib/python3:13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

EXPOSE 4200

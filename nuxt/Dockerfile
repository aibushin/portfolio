# build stage
FROM node:24.11.0-alpine AS build
WORKDIR /app
COPY package*.json package-lock.json* ./ 
RUN npm install
COPY . .
# RUN npm run build

# production stage
FROM nginx:stable-alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


# docker build -f vue/Dockerfile -t vue --target build .
# docker run -it --rm -p 5173:5173 -v ${PWD}:/app/vue-project vue sh

# docker build -t vuejs-cookbook/dockerize-vuejs-app .
# docker run -it --rm -p 8080:80 -v ${PWD}:/app/vue-project vuejs-cookbook/dockerize-vuejs-app
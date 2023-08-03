
FROM node:latest

RUN mkdir -p /home/app

COPY . /home/app
WORKDIR /home/app

RUN npm install

EXPOSE 2229

CMD [ "node", "main.js" ]  

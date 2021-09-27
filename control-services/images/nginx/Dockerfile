FROM nginx
WORKDIR /etc/nginx/conf.d/
COPY ./nginx.conf ../nginx.conf
RUN mkdir sites-available -p
RUN mkdir sites-enabled -p
COPY ./servers/semaphore.conf sites-available/
RUN ls -n sites-available/semaphore.conf sites-enabled/

RUN nginx -t

#COPY --from=build /app/build /usr/share/nginx/html

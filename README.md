# Web application for publishing articles
Application for creating and administering articles.
Includes:
* Subscribe to the newsletter
* Share an article (Google SMTP)
* Mailing after article publication (Celery/Rabbitmq)
* Ability to publish articles with images (CKEditor)
* RSS subscription support
* Ability to comment on articles
* Search
* Tagging
* Daily database dump (Cron)

## Requirements
- Docker
- Docker Compose

## For development
1. Clone the repository
2. Move to blog_app directory
```
cd blog_app
```
4. Rename .env.example to .env and change the variables to yours if needed
```
mv .env.example .env
```
3. Run the docker-compose.dev.yml file
```
docker-compose -f docker-compose.dev.yml up -d
```
4. Create a superuser to enter the admin area
```
docker exec -it blog_app_web_1 python manage.py createsuperuser
```
5. Install ckeditor html5video plugin
```
wget -P blog/static/ckeditor/ckeditor/plugins  https://download.ckeditor.com/html5video/releases/html5video_1.2.zip &&
unzip blog/static/ckeditor/ckeditor/plugins/html5video_1.2.zip -d blog/static/ckeditor/ckeditor/plugins/ && 
rm blog/static/ckeditor/ckeditor/plugins/html5video_1.2.zip &&
mv blog/static/ckeditor/ckeditor/plugins/ckeditor-html5-video-master/html5video blog/static/ckeditor/ckeditor/plugins && 
rm -rf blog/static/ckeditor/ckeditor/plugins/ckeditor-html5-video-master
```
6. Visit localhost:8000

## For production
1. Clone the repository
2. Move to blog_app directory
```
cd blog_app
```
3. Rename .env.example to .env and and change the variables to yours if needed
```
mv .env.example .env
```
4. Run the docker-compose.prod.yml file
```
docker-compose -f docker-compose.prod.yml up -d
```
5. Create a superuser to enter the admin area
```
docker exec -it blog_app_web_1 python manage.py createsuperuser
```
6. Install ckeditor html5video plugin
```
wget -P blog/static/ckeditor/ckeditor/plugins  https://download.ckeditor.com/html5video/releases/html5video_1.2.zip &&
unzip blog/static/ckeditor/ckeditor/plugins/html5video_1.2.zip -d blog/static/ckeditor/ckeditor/plugins/ && 
rm blog/static/ckeditor/ckeditor/plugins/html5video_1.2.zip &&
mv blog/static/ckeditor/ckeditor/plugins/ckeditor-html5-video-master/html5video blog/static/ckeditor/ckeditor/plugins && 
rm -rf blog/static/ckeditor/ckeditor/plugins/ckeditor-html5-video-master
```
7. Run the Nginx container as shown in the link 
https://github.com/GrigorevEv/Nginx_config_for_two_apps
8. Visit your host address

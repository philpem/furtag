# References

- Minimal Docker containers:
    - https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3
- Docker composing a Flask app line by line:
    - https://medium.com/bitcraft/docker-composing-a-python-3-flask-app-line-by-line-93b721105777
- scalable app w/ Gunicorn and Nginx:
    - https://medium.com/@kmmanoj/deploying-a-scalable-flask-app-using-gunicorn-and-nginx-in-docker-part-1-3344f13c9649
    - https://medium.com/@kmmanoj/deploying-a-scalable-flask-app-using-gunicorn-and-nginx-in-docker-part-2-fb33ec234113
- Dockerizing a Python3 Flask app, line by line:
    - https://medium.com/bitcraft/dockerizing-a-python-3-flask-app-line-by-line-400aef1ded3a
- From Localhost to the Cloud:
    - https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/
    - http://www.patricksoftwareblog.com/how-to-use-docker-and-docker-compose-to-create-a-flask-application/
- Dockerfile reference: https://docs.docker.com/engine/reference/builder/
- Pruning: https://docs.docker.com/config/pruning/
- Databases:
    - Customising MySQL in Docker: https://medium.com/better-programming/customize-your-mysql-database-in-docker-723ffd59d8fb
    - Example postgres docker-compose script: https://gist.github.com/onjin/2dd3cc52ef79069de1faa2dfd456c945


https://github.com/xiaopeng163/docker-compose-flask

https://nickjanetakis.com/blog/dockerize-a-flask-celery-and-redis-application-with-docker-compose


Deploying:

- https://www.google.com/search?client=ubuntu&channel=fs&q=flask+auto-deploy&ie=utf-8&oe=utf-8
- http://flask.pocoo.org/docs/0.12/patterns/fabric/
- https://semaphoreci.com/community/tutorials/continuous-deployment-of-a-python-flask-application-with-docker-and-semaphore
- https://github.com/realpython/flask-deploy
- https://github.com/reddimohan/flask-auto-deploy-with-fabric-python



# Docker commands:

## Prune:
	`docker system prune`

## Build:
	`docker build --tag myapp_app .`

## Run in the background:
	`docker run -td -p 5000:8000 myapp_app`



# Current issues:

- Database setup isn't great


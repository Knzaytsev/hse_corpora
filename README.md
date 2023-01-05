# HSE Corpora App
HSE Corpora App is a corpus manager for exam texts written in English by Russian students. The corpus manager can be deployed by using Vagranfile. Also you can not to use Vagrant, but you can run the project using only docker.

## Vagrant use
You can deploy the project using Vagrantfile. To do it, you should execute commands as follow:
```
vagrant up
vagrant ssh
cd /vagrant
```

## Docker deployment
In the project folder you should run the next command:
```
docker compose --project_name="<your project name>" up -d --build
```
To down the docker you should write:
```
docker compose --project_name="<your project name>" down
```

## Data load
To load corpora, run in the "rest" folder or in the docker shell command:
```
dvc pull
```

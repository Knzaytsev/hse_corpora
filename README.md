# HSE Corpora App
HSE Corpora App is a corpus manager for exam texts written in English by Russian students. The corpus manager can be deployed by using Vagranfile. Alternatively, it is possible to run the project using only docker.

## Vagrant use
You can deploy the project using Vagrantfile. To do it, you should execute the commands as follows:
```
vagrant up
vagrant ssh
cd /vagrant
```

## Docker environments
You can see environment variables and example values in the file ".env.example". To use your own variables, replace ".example" suffix and write needed values.

## Docker deployment
In the project folder you should run the following command:
```
docker compose --project-name="<your project name>" up -d --build
```
To down the docker you should write:
```
docker compose --project-name="<your project name>" down
```

## Data load
To load the corpus data, you have to have "service_account.json" in the "rest" folder. This file can be requested from google API. For detailed information, see "User service accounts" in https://dvc.org/doc/user-guide/how-to/setup-google-drive-remote.

After loading the service account file you have to connect to the docker container by `docker exec -it python_api bash` and run `sh /code/load_data.sh`. By the last command you will run script execution that imports tsv-files to the database. This script will take about 30-60 minutes depending on your machine. You can execute `curl localhost:8080/fulfill_tables/status` to check execution status.

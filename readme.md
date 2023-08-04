## Setup database and network

```
git clone https://github.com/fantozy/Fantozy-test-o-parser
```

```
docker volume create mysqlvol
```

```
docker network create trenbolone
```

## Run containers
```
docker run -e MYSQL_ROOT_PASSWORD=1234 -p 3307:3306 --name=scraperdb -v mysqlvol:/var/lib/mysql --network trenbolone -d mysql:latest
```

```
docker run -p 8001:8000 --network trenbolone -d tren
```
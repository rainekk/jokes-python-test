# joke-api

Simple Python Flask application that manages jokes

## Overview

Jokes are ordered in **categories** and stored in a **SQLite** database. They can have an optional **ranking** (*from 1 for bad to 10 for good*).

## Requirements

For using this application, you will need:

- Python 3
- Flask
- SQLite 3

## Docker container

There is a [`Dockerfile`](dockerfile) for running this application inside a container based on [Alpine Linux](https://www.alpinelinux.org).
To create the image, run the following command:

```shell
$ docker build -t joke_api .
```

This will take a couple of minutes, afterwards you should see the image:
```shell
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
joke_api            latest              84572d3b8826        1 hour ago          59.8MB
...
```

To start a new container based on this image, execute:

```shell
$ docker run -d -p 5000:5000 joke_api
b4735f102afb6e288b0a35d17b0e63da4d6bd2652467709c5c28538088ae5d30

$ docker ps
CONTAINER ID        IMAGE                      COMMAND                   CREATED             STATUS                PORTS                                                                                                  NAMES
b4735f102afb        joke_api                   "/bin/sh -c \"/opt/jo…"   16 seconds ago      Up 14 seconds         0.0.0.0:6000->5000/tcp                                                                                 boring_chebyshev
...
```

It is also possible to use shipped [docker-compose file](docker-compose.yml):

```shell
$ docker-compose create
$ docker-compose up
Starting joke_api ... done
Attaching to joke_api
...
joke_api    |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## API calls

There is also a pre-defined [Postman collection](postman.json).

### Categories

| Call | Method | Parameters | Description |
| ---- | ------ | ---------- | ----------- |
| `/api/categories` | `GET` | - | returns all available categories |
| `/api/categories/<id,name>` | `GET` | category ID/name | returns a particular category |
| `/api/categories` | `POST` | `{ "item": { "name": "<str>" } }` | creates a new category |
| `/api/categories/<id>` | `PUT,POST` | category ID, `{ "item": {"id": <int>, "name": "<str>"} }` | updates an existing category |
| `/api/categories/<id>` | `DELETE` | category ID | removes a category |

### Jokes

| Call | Method | Parameters | Description |
| ---- | ------ | ---------- | ----------- |
| `/api/jokes/<id>` | `GET` | joke ID | retrieves a particular joke |
| `/api/jokes/random` | `GET` | - | retrieves a random joke |
| `/api/jokes/random/<id,name>` | `GET` | category ID/name | retrieves a random joke from a particular category |
| `/api/jokes/random/<id,name>/<rank>` | `GET` | category ID/name | retrieves a random joke from a particular category with a specific minimum ranking |
| `/api/jokes` | `POST` | `{ "item": { "category_id": <int>, "text": "<str>", "rank": <int> } }` | creates a new joke within a category |
| `/api/jokes/<id>` | `PUT/POST` | joke ID, `{ "item": {"newid": <int>, "category_id": <int>, "text": "<str>", "rank": <int>} }` | updates an existing joke |
| `/api/jokes/<id>` | `DELETE` | joke ID | removes a joke |

## Database layout

### `categories`

| Field name | Field type | Description |
| ---------- | ---------- | ----------- |
| `category_id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | category ID |
| `category_name` | `TEXT NOT NULL` | category name |

### `jokes`

| Field name | Field type | Description |
| ---------- | ---------- | ----------- |
| `joke_id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | joke ID |
| `category_id` | INTEGER NOT NULL (*FOREIGN KEY*) | category ID |
| `joke_text` | `TEXT NOT NULL` | joke |
| `joke_rank`| INTEGER NULL | joke ranking (*1 - 10*) |

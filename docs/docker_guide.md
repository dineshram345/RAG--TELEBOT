# Docker Guide

## What is Docker?

Docker is a platform that packages applications into containers - lightweight, standalone units that include everything needed to run: code, runtime, libraries, and system tools. Containers run the same way on any machine, solving the "works on my machine" problem.

## What is the difference between an image and a container?

An image is a read-only template that defines what goes into a container. A container is a running instance of an image. Think of an image as a class and a container as an object. You can run multiple containers from the same image, and each one is isolated from the others.

## How do I write a Dockerfile?

A Dockerfile is a text file with instructions to build an image. A simple Python example:

```
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Each line creates a layer. Docker caches layers, so put things that change less often (like installing dependencies) before things that change more (like copying your code).

## What are the basic Docker commands?

- `docker build -t myapp .` - build an image from a Dockerfile
- `docker run myapp` - run a container from an image
- `docker run -p 8080:80 myapp` - map port 80 in the container to 8080 on your host
- `docker ps` - list running containers
- `docker stop <container_id>` - stop a running container
- `docker images` - list all images on your machine

## What is Docker Compose?

Docker Compose lets you define and run multi-container applications using a YAML file. Instead of running multiple `docker run` commands, you describe all your services in `docker-compose.yml` and start everything with `docker compose up`. It handles networking between containers automatically.

## How do volumes work?

Volumes persist data beyond the lifetime of a container. Without a volume, any data written inside a container is lost when the container is removed. Use `-v /host/path:/container/path` to mount a directory from your machine into the container, or use named volumes with `docker volume create`.

## What is the difference between CMD and ENTRYPOINT?

CMD sets the default command that runs when the container starts and can be overridden easily. ENTRYPOINT sets a fixed command that always runs. In practice, use ENTRYPOINT for the main executable and CMD for default arguments that users might want to change.

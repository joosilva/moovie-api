IMAGE_NAME = moovie-api

PORT = 8080

APP_PATH = main:app

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d -p $(PORT):$(PORT) $(IMAGE_NAME)

test:
	docker run --rm $(IMAGE_NAME) pytest

stop:
	docker ps -q --filter ancestor=$(IMAGE_NAME) | xargs -r docker stop

clean:
	docker ps -a -q --filter ancestor=$(IMAGE_NAME) | xargs -r docker rm
	docker images -q $(IMAGE_NAME) | xargs -r docker rmi

rebuild: 
	stop clean build run

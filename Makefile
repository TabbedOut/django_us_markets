build:
	docker-compose build

download:
	docker-compose run app download_us_markets

test:
	docker-compose run app test --noinput

bash:
	docker run -it --entrypoint /bin/bash django_us_markets

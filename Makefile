build:
	docker-compose build

download:
	docker-compose run app download_us_markets

test:
	docker-compose run app test --noinput

bash:
	docker run -it --entrypoint /bin/bash django_us_markets

fixtures:
	ogr2ogr -where "ZCTA5CE10 in ('78404', '78704')" \
		django_us_markets/tests/fixtures/us_census_bureau/tl_2015_us_zcta510.shp \
		django_us_markets/data/us_census_bureau/tl_2015_us_zcta510.shp

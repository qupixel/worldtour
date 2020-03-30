all: cities.csv

cities.csv: data/book.txt data/around.json
	python src/places.py
	
test:
	pytest --cov=reader --cov=analyzer --cov-report term-missing . && flake8 .

docker: 
	docker container run --name devtest --mount type=bind,source=$$(pwd),target=/app -it worldtour

clean: 
	docker rm devtest

build: 
	docker image build -t worldtour .
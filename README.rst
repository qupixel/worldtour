A 'word' tour in 80 days
************************


Cities appearing in The World Tour in 80 Days ebook. Cities extracted using python, spacy, and a few other things. Visualization in D3.js with geojson. 

`Interactive visualization here
<https://qupixel.github.io/d3/worldtour.htm>`_ 

This was a for-fun project developed in a few weekends. 


Pre-requisites
--------------

- Find the ebook and save it as data/book.txt
- Download worldcities.csv from https://simplemaps.com/data/world-cities into the `data/` folder (creative commons license). 

Running
-------

- Run `src/places.py` to extract the list of cities. 

- A Dockerfile is provided for Docker users. 

 - To run the image, run `make build`. 
 - Once the image is built, to start the container,  run `make docker` (after that you can run `make clean docker`.  
 - From inside the container, you can run `make test` to check everything is fine
 - From inside the container `make cities.csv` to launch the process of extracting cities. 


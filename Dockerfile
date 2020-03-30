FROM fnndsc/ubuntu-python3
LABEL maintainer="jose"
RUN pip install numpy spacy pytest pytest-cov flake8 pandas && python -m spacy download en_core_web_sm
WORKDIR /app/
#RUN pytest --cov=reader --cov-report term-missing . && flake8 .
#ENTRYPOINT ["python", "src/places.py"]
ENTRYPOINT ["/bin/bash"]
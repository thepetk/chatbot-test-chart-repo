FROM registry.access.redhat.com/ubi9/python-39:latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "create_github_repos.py"]
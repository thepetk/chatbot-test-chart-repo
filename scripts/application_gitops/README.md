# AI Software Template Helm Chart - Application GitOps Python Script

The python script is responsible to create the application repository related with the deployment of the ai software template deployment. More details about the ai-software-templates helm chart can be found [here](../../charts/ai-software-templates/chatbot/0.1.0/).

## Actions

The script performs the following actions:

1. Creates a repository with the given name and inside the given github organization.
2. Sets the default branch to the given one.
3. Populates the new repository with the contents of the ai software template and the tekton pipeline run.

## Build

You can build the image of the script by running:

```
docker build -t <your-registry>/<your-repo>/<image-name>:<tag>
```

## Required Environment Variables

The script requires the following environment variables to be set beforehand:

- `APP_NAME`: Your application's name.
- `APP_NAMESPACE`: The OpenShift Namespace that your application is deployed.
- `GITHUB_TOKEN`: A github token with sufficient access to the organization you are planning to create your repo. See [here](../../charts/ai-software-templates/chatbot/0.1.0/README.md#gitops) for more information.
- `GITHUB_ORG_NAME`: The github organization name in which you're planning to create the application repo.
- `GITHUB_SOURCE_REPO`: The repository containing the ai software template content. Example value `organization/name`.
- `GITHUB_TETKON_SOURCE_REPO`: The repository containing the `docker-push.yaml` PipelineRun. Example value `organization/name`.
- `GITHUB_DEFAULT_BRANCH`: The default branch of the created github repository.

## Running the script

You can either run the script locally or with docker/podman.

### Running Locally

Locally you have to:

- Export all env vars mentioned above.
- Install all necessary requirements by running:

```
pip install -r requirements.txt
```

- Run the script with the command `python application_gitops.py`

### Running with Docker/Podman

Using docker or podman you have to:

- Follow the instructions in [build section](#build).
- Run with a command having the following format:

```
docker run -e <set all the env vars> ... <your-image>
```

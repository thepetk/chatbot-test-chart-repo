# AI Software Template Helm Chart

This repo is a Helm chart for building and deploying an AI Software Template on OpenShift. The application deployed is a Large language model (LLM)-enabled [chat application](https://github.com/redhat-ai-dev/ai-lab-samples/tree/main/chatbot).

For more information about helm charts see the official [Helm Charts Documentation](https://helm.sh/).

The deployment flow, will create an application instance, a model server and a github repository with all the application contents in the given github organization.

## Requirements

- You have a Github APP created with sufficient permissions for the organization that the application repository will be created. Detailed instructions for the github application creation can be found [here](https://github.com/redhat-ai-dev/ai-rhdh-installer/blob/3682de381c88c1e00bb4c363b58174b427d32429/docs/APP-SETUP.md#github-app)
- You need to have access to a cluster for each operation with OpenShift 4, like deploying and testing.
- Your cluster should have [Openshift Pipelines Operator](https://www.redhat.com/en/technologies/cloud-computing/openshift/pipelines) installed and should be connected to your Github APP's webhook. In case your cluster is not configured yet, check the ["Setup Openshift Pipelines Operator"](#setup-openshift-pipelines-operator) below for further instructions.
- A Secret is already created in the Namespace that you are planning to install your helm release, containing a [Github Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic) with sufficient access to the given Github Organization. You can find the exact permissions [here].

## Setup Openshift Pipelines Operator

The suggested way to subscribe to, configure and connect the Openshift Pipelines and your Github App, is the usage of [ai-rhdh-installer](https://github.com/redhat-ai-dev/ai-rhdh-installer/blob/main/README.md). The steps to follow are:

- Keep in mind that, for the helm chart installation we only need the `openshift-pipelines` so before running the installer, you can disable `openshift-gitops` and `developer-hub` in the [values.yaml](https://github.com/redhat-ai-dev/ai-rhdh-installer/blob/main/chart/values.yaml).
- Then you can run:

```
helm upgrade --install <helm-release-name> ./chart --namespace <your-application-namespace> --create-namespace

```

Where `helm-release-name` is the name of the configuration release and `your-application-namespace` is the Namespace you are planning to install your AI Software Template helm release.

## Values

Below is a table of each value used to configure this chart.

### Application

| Value          | Description                                                   | Default                                | Additional Information |
| -------------- | ------------------------------------------------------------- | -------------------------------------- | ---------------------- |
| `name`         | The name of the application.                                  | `chatbot-helm-chart`                   |                        |
| `namespace`    | The namespace that the application will be deployed.          | `ai-software-templates-dev`            |                        |
| `appPort`      | The exposed port of the application                           | 8501                                   |                        |
| `appContainer` | The initial image used for the chatbot application interface. | `quay.io/redhat-ai-dev/chatbot:latest` |                        |

### Model

| Value                   | Description                                                           | Default                                                 | Additional Information |
| ----------------------- | --------------------------------------------------------------------- | ------------------------------------------------------- | ---------------------- |
| `modelServicePort`      | The exposed port of the model service.                                | 8001                                                    |                        |
| `modelServiceContainer` | The image used for the model service.                                 | `quay.io/ai-lab/llamacpp_python:latest`                 |                        |
| `initContainer`         | The image used for the initContainer of the model service deployment. | `quay.io/redhat-ai-dev/granite-7b-lab:latest`           |                        |
| `modelInitCommand`      | The model service initContainer command.                              | `['/usr/bin/install', '/model/model.file', '/shared/']` |                        |
| `modelPath`             | The path of the model file inside the model service container.        | `/model/model.file`                                     |                        |

### Gitops

| Value               | Description                                                                                            | Default                            | Additional Information |
| ------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------- | ---------------------- |
| `gitSecretName`     | The name of the Secret containing the required Github token.                                           | `git-secrets`                      |                        |
| `gitSecretKeyToken` | The name of the Secret's key with the Github token value.                                              | `GITHUB_TOKEN`                     |                        |
| `githubOrgName`     | `[REQUIRED]` The Github Organization name that the chatbot application repository will be created into |                                    |                        |
| `gitSourceRepo`     | The Github Repository with the contents of the chatbot application.                                    | `"thepetk/chatbot-test-chart-repo` |                        |
| `gitDefaultBranch`  | The default branch for the chatbot application Github repository.                                      | `main`                             |                        |

# Chatbot AI Sample Helm Chart

This repo is a Helm chart for building and deploying a Large language model (LLM)-enabled [chat application](https://github.com/redhat-ai-dev/ai-lab-samples/tree/main/chatbot). For more information about helm charts see the official [Helm Charts Documentation](https://helm.sh/).

The deployment flow, will create an application instance, a model server and a github repository with all the application contents in the given github organization. See the [background](#background) section for more information.

## Requirements

- You have a Github APP created with sufficient permissions for the organization that the application repository will be created. Detailed instructions for the github application creation can be found [here](https://github.com/redhat-ai-dev/ai-rhdh-installer/blob/main/docs/APP-SETUP.md#github-app).
- You need to have access to a cluster for each operation with OpenShift 4, like deploying and testing.
- The Namespace that your application will run is already created in your cluster.
- Your cluster should have [Openshift Pipelines Operator](https://www.redhat.com/en/technologies/cloud-computing/openshift/pipelines) installed and should be connected to your Github App's webhook. In case your cluster is not configured yet, check the ["Pipelines Configuration Guide"](https://github.com/redhat-ai-dev/ai-lab-helm-charts/blob/main/docs/PIPELINES_CONFIGURATION.md) for further instructions.
- A `key/value` Secret is already created in the Namespace that you are planning to install your helm release, containing a [Github Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic) with sufficient access to the given Github Organization. You can find the exact permissions [here](https://github.com/redhat-ai-dev/ai-rhdh-installer/blob/main/docs/APP-SETUP.md#procedure). Your Secret's name and the Key of the github token will be provided as values to the helm chart.

## Background

The chatbot helm chart utilizes two main deployments:

1. The model service deployment, based on `llama.cpp` inference server and related to the [ai-lab-recipes model server](https://github.com/containers/ai-lab-recipes/tree/main/model_servers/llamacpp_python).
2. The application deployment, a Streamlit based application to interact with the model service. The application is based on the related [Chatbot Template](https://github.com/redhat-ai-dev/ai-lab-template/tree/main/templates/chatbot/content).

Apart from the two main deployments, the gitops & OpenShift Pipelines parts are handled by the following:

1. The [application-gitops-job](./templates/application-gitops-job.yaml) which takes care of the application github repository creation.
2. The [tekton Repository](./templates/tekton-repository.yaml) which connects our application with the `pipeline-as-code-controller` and we are able to manage all webhooks received from our Github App.

## Installation

The helm chart can be directly installed from the OpenShift Dev Console. Check [here](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/building_applications/working-with-helm-charts#understanding-helm) for more information.

### Install using Helm

In order to install Chatbot AI Sample Helm chart using helm directly, you can run:

```
export APP_NAMESPACE='the-namespace-your-release-will-be-installed'
export RELEASE_NAME='the-name-of-your-release'

helm upgrade --install $RELEASE_NAME --namespace $APP_NAMESPACE .
```

## Values

Below is a table of each value used to configure this chart. Note:

- Your helm release's name will be used to as the name of the application github repository.

### Application

| Value                      | Description                                                   | Default                                | Additional Information |
| -------------------------- | ------------------------------------------------------------- | -------------------------------------- | ---------------------- |
| `application.appPort`      | The exposed port of the application                           | 8501                                   |                        |
| `application.appContainer` | The initial image used for the chatbot application interface. | `quay.io/redhat-ai-dev/chatbot:latest` |                        |

### Model

| Value                         | Description                                                           | Default                                                 | Additional Information |
| ----------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------- | ---------------------- |
| `model.modelServicePort`      | The exposed port of the model service.                                | 8001                                                    |                        |
| `model.modelServiceContainer` | The image used for the model service.                                 | `quay.io/ai-lab/llamacpp_python:latest`                 |                        |
| `initContainer`               | The image used for the initContainer of the model service deployment. | `quay.io/redhat-ai-dev/granite-7b-lab:latest`           |                        |
| `model.modelInitCommand`      | The model service initContainer command.                              | `['/usr/bin/install', '/model/model.file', '/shared/']` |                        |
| `model.modelPath`             | The path of the model file inside the model service container.        | `/model/model.file`                                     |                        |

### Gitops

| Value                      | Description                                                                                                                                         | Default                        | Additional Information |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ---------------------- |
| `gitops.gitSecretName`     | The name of the Secret containing the required Github token.                                                                                        | `git-secrets`                  |                        |
| `gitops.gitSecretKeyToken` | The name of the Secret's key with the Github token value.                                                                                           | `GITHUB_TOKEN`                 |                        |
| `gitops.githubOrgName`     | `[REQUIRED]` The Github Organization name that the chatbot application repository will be created into                                              |                                |                        |
| `gitops.gitSourceRepo`     | The Github Repository with the contents of the ai-lab sample chatbot application. It must be either the `redhat-ai-dev/ai-lab-samples` or its fork. | `redhat-ai-dev/ai-lab-samples` |
| `gitops.gitDefaultBranch`  | The default branch for the chatbot application Github repository.                                                                                   | `main`                         |                        |
| `gitops.quayAccountName`   | `[REQUIRED]` The quay.io account that the application image will be pushed.                                                                         |                                |                        |

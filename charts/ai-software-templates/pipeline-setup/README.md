# OpenShift Pipelines Application Namespace setup for Devtools AI Sample Applications.

This repo is a Helm chart that a user admin level privileges to his application namespace would run to set up OpenShift Pipelines for the Devtools AI sample applications. For more information about helm charts see the official [Helm Charts Documentation](https://helm.sh/).


## Requirements

- You have sufficient permissions to create a namespace.
- You have sufficient permissions to create RBAC and ServiceAccounts in your namespace.

## Background

This chart assumes the [OpenShift Pipelines install chart](../pipeline-install/README.md) has been run, something equivalent to what it does, so 
that OpenShift Pipelines can run the Tekton Pipelines under the [rhdh-pipelines](https://github.com/redhat-ai-dev/rhdh-pipelines) repo, and that
Pipelines As Code has sufficient credentials to process events from you GitHub Application.

This chart will then set up the Quay and Git credentials in Secrets so that the Tekton Pipelines can interact with your
applications GitHub repository and push you versions of your application's image to your Quay repository.

## Installation

The helm chart can be directly installed from the OpenShift Dev Console. Check [here](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/building_applications/working-with-helm-charts#understanding-helm) for more information.

### Install using Helm

To install the Pipelines Setup Helm chart using Helm directly, you can run:

```
helm upgrade --install <release-name> --namespace <helm-release-and-chatbot-application-namespace> --create-namespace .
```

The `.gitignore` file in this repository filters files named `private-values.yaml`.  Thus, you can maintain in 
your local fork of this repository a value settings file outside of git management.  Copy `values.yaml` in this directory to `private-values.yaml` and make any necessary edits to `private-values.yaml`.  Then change your helm invocation to the following:

```shell
helm upgrade --install <release-name> --namespace <helm-release-and-chatbot-application-namespace> --create-namespace -f ./private-values.yaml .
```

## Values

Below is a table of each value used to configure this chart. 

### Tekton

| Value                      | Description                                                                             | Default                       | Additional Information |
|----------------------------|-----------------------------------------------------------------------------------------|-------------------------------| ---------------------- |
| `tekton.quayConfigJSON`    | `[REQUIRED]` The quay.io config.json used when the application image will be pushed.    |                               |                        |
| `tekton.quaySecretName`    | The name of the Secret containing the required Quay token.                              | 'ai-lab-image-registry-token' |                        |
| `tekton.gitSecretName`     | The name of the Secret containing the required Github token.                            | 'github-secrets'              |                        |
| `tekton.gitSecretKeyToken` | The name of the Secret's key with the Github token value.                               | 'password'                    |                        |
| `tekton.gitSecretToken`    | `[REQUIRED]` The Github token value.                                                    |                               |                        |

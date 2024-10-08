# OpenShift Pipelines Configuration - AI Software Template Helm Chart

This helm chart tries to provide an easy way to configure OpenShift Pipelines on your cluster and set everything up for the installation of the [AI Software Template Chat Application Helm Chart](../ai-software-templates/chatbot/0.1.0/).

## Requirements

Before installing the pipelines configuration helm chart, make sure you have created a Secret inside the Namespace you plan to release your Chat Application. The necessary fields are mentioned in the [values.gitops](#gitops) section.

## Usage

To install the configuration helm chart simply run:

```
helm upgrade --install <release-name> --namespace <release-namespace> .
```

## Values

### application

| Value       | Description                                               | Default                     | Additional Information |
| ----------- | --------------------------------------------------------- | --------------------------- | ---------------------- |
| `name`      | The name of the configuration helm chart release.         | `chatbot-configuration`     |                        |
| `namespace` | The namespace that the chat application will be released. | `ai-software-templates-dev` |                        |

### gitops

| Value                              | Description                                                                         | Default                     | Additional Information |
| ---------------------------------- | ----------------------------------------------------------------------------------- | --------------------------- | ---------------------- |
| `gitSecretName`                    | The name of the Secret containing the required Github credentials.                  | `git-secrets`               |                        |
| `gitSecretKeyToken`                | The name of the Secret's key with your Github token value.                          | `GITHUB_TOKEN`              |                        |
| `gitSecretKeyAppId`                | The name of the Secret's key with your Github App's application id value.           | `GITHUB_APP_APP_ID`         |                        |
| `gitSecretKeyWebhookURL`           | The name of the Secret's key with your Github App's webhook url value.              | `GITHUB_APP_WEBHOOK_URL`    |                        |
| `gitSecretKeyWebhookSecret`        | The name of the Secret's key with your Github App's webhook secret value.           | `GITHUB_APP_WEBHOOK_SECRET` |                        |
| `gitSecretKeyPrivateKey`           | The name of the Secret's key with your Github App's private key value.              | `GITHUB_APP_PRIVATE_KEY`    |                        |
| `gitSecretKeyQuayDockerConfigJSON` | The name of the Secret's key with your Github App's quay.io DockerConfigJson value. | `QUAY_DOCKERCONFIGJSON`     |                        |

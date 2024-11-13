# AI Software Templates Helm Charts

This project aims to convert the [AI Software Templates](https://github.com/redhat-ai-dev/ai-lab-template) functionality into helm charts. Therefore, it aims to reproduce the flow of AI Software Templates without the usage of RHDH.

## Available Helm Charts

At the moment one template has helm chart support and this is the [chatbot application template](https://github.com/redhat-ai-dev/ai-lab-template/tree/main/templates/chatbot). The chatbot helm chart can be found [here](/charts/ai-software-templates/chatbot/).

## Gitops

The gitops component, handled by ArgoCD for the RHDH case, is replaced by the `application_gitops` project. Therefore, post application deployment a kubernetes Job is taking care of the github application repository creation. The source code is [here](https://github.com/redhat-ai-dev/developer-images/tree/main/helm-charts/application-gitops)

## OpenShift Pipelines

For OpenShift Pipelines configuration there's an [OpenShift Pipelines Configuration Guide](/docs/PIPELINES_CONFIGURATION.md) that the user can follow to configure their pipelines, prior to installing the helm chart.

The helm chart mainly uses the tekton pipelines under [rhdh-pipelines](https://github.com/redhat-ai-dev/rhdh-pipelines) repo. The only customized resources used for the helm chart case are:

- The [.tekton/docker-push.yaml](/pac/pipelineRuns/.tekton/docker-push.yaml) PipelineRun used to manage `push` events received from the github app webhook.
- The [update-deployment.yaml](/pac/tasks/update-deployment.yaml) Task which is used to update the application deployment whenever a new image is pushed to the image registry.
- The [docker-build-ai-software-templates-chart.yaml](./pac/pipelines/docker-build-ai-software-templates-chart.yaml) Pipeline, again used for the application deployment update.

## Testing with a Custom Helm Repository

In case you're interested to test your updates by importing the `ai-lab-helm-charts` fork as a custom helm chart repository, you can follow the instructions [here](./docs/SETUP_CUSTOM_HELM_REPO.md)

## Release process

The ai-lab-helm-charts are created on demand.

- A `tag` should be created with the version of the release as name. ai-lab-helmcharts follows the v{major}.{minor}.{bugfix} format (e.g v0.1.0).
- Before proceeding, make sure that all the `Chart.yaml` `version` fields have this tag as value. For example in case the tag is `v0.1.0` the `version` should be `0.1.0`.
- After the new release is published, the updated helm packages will be pinned on the release.

# AI Software Templates Helm Charts

This project aims to convert the [AI Software Templates](https://github.com/redhat-ai-dev/ai-lab-template) functionality into helm charts. Therefore, it aims to reproduce the flow of AI Software Templates without the usage of RHDH.

## Available Helm Charts

At the moment one template has helm chart support and this is the [chatbot application template](https://github.com/redhat-ai-dev/ai-lab-template/tree/main/templates/chatbot). The chatbot helm chart can be found [here](/charts/ai-software-templates/chatbot/).

## Gitops

The gitops component, handled by ArgoCD for the RHDH case, is replaced by the `application_gitops` project. Therefore, post application deployment a kubernetes Job is taking care of the github application repository creation. The source code is [here](https://github.com/redhat-ai-dev/developer-images/tree/main/helm-charts/application-gitops)

## OpenShift Pipelines Configuration

For OpenShift Pipelines configuration there's a separate (optional) helm chart, that a user can use to install and configure the pipelines for their project. The configuration helm chart is [here](/charts/openshift-pipelines/).

The helm chart mainly uses the pipelines under [rhdh-pipelines](https://github.com/redhat-ai-dev/rhdh-pipelines) repo. The only customized resources used for the helm chart case are:

- The [.tekton/docker-push.yaml](/pac/pipelineRuns/.tekton/docker-push.yaml) PipelineRun used to manage `push` events received from the github app webhook.
- The [update-deployment.yaml](/pac/tasks/update-deployment.yaml) Task which is used to update the application deployment whenever a new image is pushed to the image registry.
- The [docker-build-ai-software-templates-chart.yaml](./pac/pipelines/docker-build-ai-software-templates-chart.yaml) Pipeline, again used for the application deployment update.

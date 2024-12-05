# AI Software Templates Helm Charts

This project aims to convert the [AI Software Templates](https://github.com/redhat-ai-dev/ai-lab-template) functionality into helm charts. Therefore, it aims to reproduce the flow of AI Software Templates without the usage of RHDH.

## Available Helm Charts

At the moment one template has helm chart support and this is the [chatbot application template](https://github.com/redhat-ai-dev/ai-lab-template/tree/main/templates/chatbot). The chatbot helm chart can be found [here](/charts/ai-software-templates/chatbot/).

In addition the helm chart for the application, there are also two helm charts for setting up OpenShift Pipelines detailed [below](#openshift-pipelines).

## Gitops

The gitops component, handled by ArgoCD for the RHDH case, is replaced by a Kubernetes Job created by the Helm chart, where this Job:
- Creates the GitHub repository for the application.
- Copies the application source code into the new repository.
- Copies the Tekton Pipelines As Code PipelineRun/Pipeline/Task that build new images for the application as pull requests 
are merged and updates the Deployment of the application with the new version of the image.
- Commits these changes and pushes the commit to the preferred branch of the new repository.

The source code is [here](charts/ai-software-templates/chatbot/templates/application-gitops-job.yaml).

## OpenShift Pipelines

For OpenShift Pipelines configuration the two Helm charts provided are:

- The [Pipeline Install Helm Chart](/charts/ai-software-templates/pipeline-install) that makes Cluster Administrative level changes to OpenShift Pipelines to make sure that:
  - OpenShift Pipelines Operator is installed.
  - The correct Tekton Pipelines features are configured for our purposes.
  - The Pipelines As Code component is set up with the requisite credentials to process GitHub events for you GitHub Application.
- The [Pipeline Setup Helm Chart](/charts/ai-software-templates/pipeline-setup) that makes the User/Tenant changes in your application Namespace:
  - The Pipelines As Code PipelinesRuns in your Namespace have the requisite credentials to push your application's image to your Quay repository.
  - The [Gitops component](#gitops) has the requisite credentials to interact with the GitHub repository for your application. 

The `chatbot-ai-sample` helm chart mainly uses the tekton pipelines under [rhdh-pipelines](https://github.com/redhat-ai-dev/rhdh-pipelines) repo. The only customized resources used for the helm chart case are:

- The [.tekton/docker-push.yaml](/pac/pipelineRuns/.tekton/docker-push.yaml) PipelineRun used to manage `push` events received from the github app webhook.
- The [update-deployment.yaml](/pac/tasks/update-deployment.yaml) Task which is used to update the application deployment whenever a new image is pushed to the image registry.
- The [docker-build-ai-software-templates-chart.yaml](./pac/pipelines/docker-build-ai-software-templates-chart.yaml) Pipeline, again used for the application deployment update.

## Testing with a Custom Helm Repository

To test your updates by importing the `ai-lab-helm-charts` fork as a custom Helm chart repository, you can follow the instructions [here](./docs/SETUP_CUSTOM_HELM_REPO.md)

## Release Process

The ai-lab-helm-charts are created on demand.

- A `tag` should be created with the version of the release as the name. `ai-lab-helmcharts` follows the v{major}.{minor}.{bugfix} format (e.g v0.1.0).
- Before proceeding, make sure that all the `version` fields within `Chart.yaml` have this tag as the value. For example in the case where the tag is `v0.1.0`, the `version` should be `0.1.0`.
- After the new release is published, the updated Helm packages will be pinned on the release.

# Chatbot AI Software template helm chart

A Helm chart for building and deploying an AI Software Template based [Chatbot Application](https://github.com/redhat-ai-dev/ai-lab-samples/tree/main/chatbot) on OpenShift.

For more information about helm charts see the official [Helm Charts Documentation](https://helm.sh/).

You need to have access to a cluster for each operation with OpenShift 4, like deploying and testing.

## Values

Below is a table of each value used to configure this chart.

| Value                   | Description                                                                                             | Default                                   | Additional Information |
| ----------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------------------- |
| `name`                  | The name assigned to all of the frontend objects defined in this helm chart.                            | `django-example`                          |                        |
| `namespace`             | The OpenShift Namespace where the ImageStream resides.                                                  | `openshift`                               |                        |
| `modelServicePort`      | The exposed port of the model server, if left blank a value will be defaulted to 8001.                  | 8082                                      |                        |

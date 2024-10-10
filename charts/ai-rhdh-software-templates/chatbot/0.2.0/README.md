# Chatbot AI Software template helm chart

A Helm chart for building and deploying an AI Software Template based [Chatbot Application](https://github.com/redhat-ai-dev/ai-lab-samples/tree/main/chatbot) on OpenShift.

For more information about helm charts see the official [Helm Charts Documentation](https://helm.sh/).

You need to have access to a cluster for each operation with OpenShift 4, like deploying and testing.

## Values

Below is a table of each value used to configure this chart.

| Value                       | Description                                                                                                                                                                                           | Default                                                 | Additional Information |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ---------------------- |
| `name`                      | The name assigned to all of the frontend objects defined in this helm chart.                                                                                                                          | `chatbot`                                               |                        |
| `namespace`                 | The OpenShift Namespace where the ImageStream resides.                                                                                                                                                | `ai-software-templates-dev`                             |                        |
| `modelServicePort`          | The exposed port of the model server, if left blank a value will be defaulted to 8001.                                                                                                                | 8001                                                    |                        |
| `appPort`                   | The exposed port of the chatbot application, if left blank a value will be defaulted to 8501.                                                                                                         | 8501                                                    |                        |
| `initContainer`             | The image used for the initContainer of the chatbot app deployment, if left blank a value will be defaulted to 'quay.io/redhat-ai-dev/granite-7b-lab:latest'.                                         | `quay.io/redhat-ai-dev/granite-7b-lab:latest`           |                        |
| `appContainer`              | The image used for the chatbot application interface, if left blank a value will be defaulted to 'quay.io/redhat-ai-dev/chatbot:latest'.                                                              | `quay.io/redhat-ai-dev/chatbot:latest`                  |                        |
| `modelInitCommand`          | The command of the model server initContainer, if left blank a value will be defaulted to ['/usr/bin/install', '/model/model.file', '/shared/']. Is used only for the `llama.cpp` model service case. | `['/usr/bin/install', '/model/model.file', '/shared/']` |                        |
| `modelPath`                 | The path of the model file inside the model server container, if left blank a value will be defaulted to '/model/model.file'.                                                                         | `/model/model.file`                                     |                        |
| `modelName`                 | The name of the model inside the given `vllm` service. Only used for vllm model service type.                                                                                                         | `instructlab/granite-7b-lab`                            |                        |
| `modelMaxLength`            | The maximum length of tokens used for the vllm service. Only used for vllm model service type.                                                                                                        | `4096`                                                  |                        |
| `modelServiceContainer`     | The image used for the model server, if left blank a value will be defaulted to 'quay.io/ai-lab/llamacpp_python:latest'.                                                                              | `quay.io/ai-lab/llamacpp_python:latest`                 |                        |
| `modelServiceType`          | The model service type used for the deployment. Can be one of `llama.cpp` or `vllm`, it defaults to llama.cpp                                                                                         | `llama.cpp`                                             |                        |
| `vllmModelServiceContainer` | The image used for the vllm model service, if left blank a value will be defaulted to `quay.io/rh-aiservices-bu/vllm-openai-ubi9:0.4.2`                                                               | `quay.io/rh-aiservices-bu/vllm-openai-ubi9:0.4.2`       |                        |

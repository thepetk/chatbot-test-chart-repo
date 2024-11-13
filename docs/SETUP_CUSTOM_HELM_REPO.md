## Testing with a Custom Helm Repository

To setup a custom Helm repository on your fork and be able to import and test the `ai-lab-helm-charts` repo on your OCP cluster, you can follow the steps below:

### Setup gh-pages

- Create a new branch (`gh-pages` could be a good candidate) in your fork.

- Go to your fork's `settings` > `Pages` > `Build and Deployment`.

- Select `Deploy from a branch` & choose your new as the branch we will be deploying from.

### Add Helm Package and Index

- Package the Helm chart you want to test:

```
# from project root dir
helm package <path-of-the-helm-chart-dir>

# example
helm package charts/ai-software-templates/chatbot/
```

- Create the `index.yaml`:

```
# from project root dir
helm repo index .
```

- Push to your branch. A deployment will start after the push event.

- On your OCP cluster you can create a custom Helm repo by applying this yaml file:

```
apiVersion: helm.openshift.io/v1beta1
kind: HelmChartRepository
metadata:
  name: 'ai-lab-helm-charts'
spec:
  connectionConfig:
    url: '<your-gh-pages-url>'

```

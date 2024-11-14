# Openshift Pipelines Configuration Instructions

The OpenShift Pipelines configuration is a requirement in order to support CI/CD between your app's github repository and your application's deployment in OpenShift. To configure the pipelines you'll need to:

1. Install the [Openshift Pipelines Operator](https://docs.redhat.com/en/documentation/openshift_container_platform/4.6/html/pipelines/installing-pipelines#installing-pipelines).

2. Ensure that the `pipeline-as-code-controller` is up by getting its route:

```
kubectl get route -n openshift-pipelines pipelines-as-code-controller
```

3. Download `cosign` depending on your platform, which will be used to generate the updated `signing-secrets`.

```
curl -sL https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64 -o /usr/bin/cosign && chmod +x /usr/bin/cosign
```

or

```
curl -sL https://github.com/sigstore/cosign/releases/latest/download/cosign-darwin-amd64 -o /usr/bin/cosign && chmod +x /usr/bin/cosign
```

4. In the `openshift-pipelines` Namespace, delete (if exists) the `signing-secrets` Secret.

5. Generate the new `signing-secrets` in the `openshift-pipelines` Namespace and patch the new secret as immutable:

```
export KUBERNETES_SERVICE_PORT=<your-kubernetes-service port>
export KUBERNETES_SERVICE_HOST=<your-kubernetes-service host>"
cosign generate-key-pair k8s://openshift-pipelines/signing-secrets
kubectl patch secret -n openshift-pipelines signing-secrets -o yaml --patch='{"immutable": true}'
```

6. Ensure that the `tektonconfigs` CRDs are available. You can verify that if the below command returns 1 as response:

```
kubectl api-resources | grep "tektonconfigs"
```

7. Update the `TektonConfig`, by enabling the necessary resolvers:

```
kubectl patch tektonconfig config --type 'merge' --patch "$( cat <<EOF
spec:
  pipeline:
    enable-bundles-resolver: true
    enable-cluster-resolver: true
    enable-custom-tasks: true
    enable-git-resolver: true
    enable-hub-resolver: true
    enable-tekton-oci-bundles: true
  chain:
    artifacts.oci.storage: oci
    artifacts.pipelinerun.format: in-toto
    artifacts.pipelinerun.storage: oci
    artifacts.taskrun.format: in-toto
    artifacts.taskrun.storage: oci
EOF
)"
```

8. Create the pipelines secret, containing your Github App's `Webhook URL` and `Webhook Secret`.

```
export APP_NAMESPACE=<your-app's namespace>
export PIPELINES_SECRET_NAME="ai-lab-pipelines-secret"
export GITHUB_APP_WEBHOOK_SECRET=<your github app's webhook secret>
export GITHUB_APP_WEBHOOK_URL=<your github app's webhook url>
kubectl -n "$APP_NAMESPACE" create secret generic "$PIPELINES_SECRET_NAME" \
    --from-literal="webhook-github-secret=$GITHUB_APP_WEBHOOK_SECRET" \
    --from-literal="webhook-url=$GITHUB_APP_WEBHOOK_URL"
```

9. Create the `pipelines-as-code-secret`, containing your Github App's `App ID`, `Private Key`, `Webhook Secret`. Note, that your `Private Key` value needs to be passed as a multilined string and not flattened.

```
export GITHUB_APP_APP_ID=<your-github-app's-app-id-value>
export GITHUB_APP_PRIVATE_KEY="
<your-multi-lined-github-app-private-key>
"
kubectl -n openshift-pipelines create secret generic pipelines-as-code-secret \
    --from-literal github-application-id="$GITHUB_APP_APP_ID" \
    --from-literal github-private-key="$GITHUB_APP_PRIVATE_KEY" \
    --from-literal webhook.secret="$GITHUB_APP_WEBHOOK_SECRET"
```

10. Fetch the codesign public key from the `signing-secrets` Secret inside the Operator's Namespace.

```
export COSIGN_SIGNING_PUBLIC_KEY=$(kubectl get secrets -n openshift-pipelines signing-secrets -o jsonpath='{.data.cosign\.pub}')
cat <<EOF | kubectl apply -f - >/dev/null
apiVersion: v1
data:
    cosign.pub: $COSIGN_SIGNING_PUBLIC_KEY
kind: Secret
metadata:
    labels:
        app.kubernetes.io/instance: default
        app.kubernetes.io/part-of: tekton-chains
        operator.tekton.dev/operand-name: tektoncd-chains
    name: cosign-pub
    namespace: $APP_NAMESPACE
type: Opaque
EOF
```

11. Create the `pipelines-secret` in your application's Namespace, containing your Github App's `Webhook Secret`:

```
kubectl -n $APP_NAMESPACE create secret generic pipelines-secret --from-literal=webhook.secret=$GITHUB_APP_WEBHOOK_SECRET
```

12. Similarly with the previous step, create the `ai-lab-image-registry-token` in your application's Namespace, containing the docker `config.json` file of your Quay.io account (see more info [here](https://docs.redhat.com/en/documentation/red_hat_quay/3.6/html-single/use_red_hat_quay/index#allow-robot-access-user-repo)):

```
export IMAGE_REGISTRY_TOKEN_SECRET="ai-lab-image-registry-token"
kubectl -n $APP_NAMESPACE create secret docker-registry "$IMAGE_REGISTRY_TOKEN_SECRET" --from-file=.dockerconfigjson=<your-docker-config.json-file-path>
```

1.  Patch the `default` and `pipeline` ServiceAccounts in your application Namespace by adding the image registry token secret created above:

```
for SA in default pipeline; do
    kubectl -n $APP_NAMESPACE patch serviceaccounts "$SA" --patch "
    secrets:
    - name: $IMAGE_REGISTRY_TOKEN_SECRET
    imagePullSecrets:
    - name: $IMAGE_REGISTRY_TOKEN_SECRET
    "
done
```

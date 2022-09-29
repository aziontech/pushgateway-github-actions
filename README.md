# Pushgateway github action

Quick way to versioning and push deployment metrics to [Prometheus](https://github.com/prometheus/prometheus) through [Pushgateway](https://github.com/prometheus/pushgateway).


## Example usage

```
      - name: POST on Pushgateway
        uses: aziontech/pushgateway-github-actions@v1
        with:
          pushgateway_url: 'http://pushgateway.infra.azion.net:9091'
          job: "deployments"
          metric_name: "deployment_success"
          metric_description: "Deployment Frequency of Azion CICD pipeline"
          metric_labels: "{'stack':'tools','app':'pushgateway-github-actions','env':'stage','version':'$VERSION'}"

```

Complete context (bump version, tag it, push the metric):
```
  example:
    runs-on: self-hosted
    container:
      image: azionedge/python-base:latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: Bumping version
        id: bump
        continue-on-error: true
        run: |
          VERSION=$(curl -O https://raw.githubusercontent.com/aziontech/pushgateway-github-actions/main/version.py && python version.py bump)
          git tag $VERSION
          git push origin $VERSION --force
          echo "::set-output name=VERSION::$VERSION"
          echo Current ver: $VERSION

      - name: POST on Pushgateway
        uses: aziontech/pushgateway-github-actions@v1
        with:
          pushgateway_url: 'http://pushgateway.infra.azion.net:9091'
          job: "deployments"
          metric_name: "deployment_success"
          metric_description: "Deployment Frequency of Azion CICD pipeline"
          metric_labels: "{'stack':'tools','app':'pushgateway-github-actions','env':'stage','version':'$VERSION'}"
```

Please use the information from the [Risk Managment](https://docs.google.com/document/d/1Ys2p-eEB3o7y12E__BfJ2kF6-LeBeOdx5ptTXidLlHo/edit#) for your `stack` and `app` values.

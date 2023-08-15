
import logging
import os

from kubernetes import client, config


logger = logging.getLogger('django')

class KubeSaAutoConfig(client.configuration.Configuration):
    def __init__(self):
        super().__init__()

        # set api_key
        with open("/run/secrets/kubernetes.io/serviceaccount/token") as f:
            self.api_key["authorization"] = f.read()

        # set api_key_prefix
        self.api_key_prefix["authorization"] = "Bearer"

        # set host
        self.host = f"https://{os.environ['KUBERNETES_SERVICE_HOST']}"

        # set ssl_ca_cert
        self.ssl_ca_cert = "/run/secrets/kubernetes.io/serviceaccount/ca.crt"

class Kubectl:
    def __init__(self, config, namespace):
        self.config = config
        self.namespace = namespace

        self.api_apps = client.AppsV1Api(client.ApiClient(config))
        self.api_batch = client.BatchV1Api(client.ApiClient(config))

        # test namespace
        self.api_apps.list_namespaced_deployment(self.namespace)

    def _get_x_name(self, x_name):
        return f"{self.instance_prefix}-{self.instance_name}-{x_name}"

    def _list_deployments(self):
        items = self.api_apps.list_namespaced_deployment(self.namespace).items
        return list(map(lambda deployment: deployment.metadata.name, items))

    def _list_jobs(self):
        items = self.api_batch.list_namespaced_job(self.namespace).items
        return list(map(lambda job: job.metadata.name, items))

    #def filter_main(self, include_controller = True):
    #    result = list()
    #    for d in self._list_deployments():
    #        if include_controller and \
    #                d.startswith(self._get_x_name("controller")):
    #            result.append(d)
#
    #        if d.startswith(self._get_x_name("vnc")) or \
    #                d.startswith(self._get_x_name("master")):
    #            result.append(d)
    #    return result

    def list_all(self):
        result = list()
        for j in self._list_deployments():
            if j.startswith("s"):
                result.append(j)
        return result

    def create_namespace(self):
        logger.error("not implemented")

    def delete_namespace(self):
        logger.error("not implemented")

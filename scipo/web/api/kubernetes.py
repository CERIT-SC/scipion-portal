
import logging
import os
import hashlib
import requests

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
    def __init__(self, config):
        self.config = config

        # set Scipion Portal's namespace identification
        # the IDs are required when creating child namespaces to avoid losing control of the child namespaces
        self.ns_name = f"{os.environ['KUBERNETES_NS_NAME']}"
        self.ns_id_label = f"{os.environ['KUBERNETES_NS_ID_LABEL']}"
        self.ns_id_annotation = f"{os.environ['KUBERNETES_NS_ID_ANNOTATION']}"

        with client.ApiClient(config) as api_client:
            self.api_apps = client.AppsV1Api(api_client)
            self.api_batch = client.BatchV1Api(api_client)
            self.api_core = client.CoreV1Api(api_client)

        # test namespace
        self.api_apps.list_namespaced_deployment(self.ns_name)

    def _get_pod_name(self, x_name):
        return f"{self.instance_prefix}-{self.instance_name}-{x_name}"

    def _get_child_ns_name(self, username):
        username_hash = hashlib.sha1(bytes(username, 'utf-8')).hexdigest()[0:8]
        return f"scipo-{username_hash}-ns"

    def _list_deployments(self):
        items = self.api_apps.list_namespaced_deployment(self.ns_name).items
        return list(map(lambda deployment: deployment.metadata.name, items))

    def _list_jobs(self):
        items = self.api_batch.list_namespaced_job(self.ns_name).items
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

    def get_instance_info(self, instance_name):
        """Get info from the running controller of the given instance"""
        # sent HTTP GET request to the controller's service
        target_svc = f"http://scipo-{instance_name}-rest:8000/info"
        try:
            r = requests.get(url = target_svc, timeout=3)
            if r.status_code != 200:
                return None

            return r.text
        except:
            return None

    def create_namespace(self, username):
        ns_name = self._get_child_ns_name(username)
        namespace = client.V1Namespace(
            api_version="v1",
            kind="Namespace",
            metadata=client.V1ObjectMeta(
                name=ns_name,
                labels={"field.cattle.io/projectId": self.ns_id_label},
                annotations={"field.cattle.io/projectId": self.ns_id_annotation}
            )
        )
        self.api_core.create_namespace(namespace)

        logger.error("not implemented")

    def delete_namespace(self, username):
        ns_name = self._get_child_ns_name(username)
        logger.error("not implemented")

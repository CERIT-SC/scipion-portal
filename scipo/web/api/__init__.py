
from .datahub import Datahubctl
from .helm import Helmctl
from .kubernetes import Kubectl, KubeSaAutoConfig

datahubctl = Datahubctl()
helmctl = Helmctl()
kubectl = Kubectl(KubeSaAutoConfig())

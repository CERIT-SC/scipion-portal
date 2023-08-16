
from .kubernetes import Kubectl, KubeSaAutoConfig
from .helm import Helmctl

kubectl = Kubectl(KubeSaAutoConfig())
helmctl = Helmctl()

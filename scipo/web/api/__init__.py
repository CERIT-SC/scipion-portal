
from .kubernetes import Kubectl, KubeSaAutoConfig

kubectl = Kubectl(KubeSaAutoConfig(), 'scipion-portal-ns')

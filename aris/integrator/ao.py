import torch
from torch import Tensor

from aris.core.scene import Scene
from aris.integrator import Integrator, integrator_registry


class AmbientOcclusionIntegrator(Integrator):
    def render(self, scene: Scene, rays_o: Tensor, rays_d: Tensor) -> Tensor:
        result = torch.zeros_like(rays_o)
        # YOUR TASK: implement ambient occlusion rendering
        return result


integrator_registry.add("ao", AmbientOcclusionIntegrator)

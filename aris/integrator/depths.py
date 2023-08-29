import torch
from torch import Tensor

from aris.core.scene import Scene
from aris.integrator import Integrator, integrator_registry


class DepthsIntegrator(Integrator):
    def render(self, scene: Scene, rays_o: Tensor, rays_d: Tensor) -> Tensor:
        # YOUR TASK: complete this integrator
        return torch.zeros_like(rays_o)


integrator_registry.add("depths", DepthsIntegrator)

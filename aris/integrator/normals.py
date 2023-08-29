from torch import Tensor

from aris.core.scene import Scene
from aris.integrator import Integrator, integrator_registry


class NormalsIntegrator(Integrator):
    def render(self, scene: Scene, rays_o: Tensor, rays_d: Tensor) -> Tensor:
        # cast the rays to find the intersection points
        geometry = scene.geometry.ray_intersect(rays_o, rays_d)

        # return the normals (interpret them as colors)
        return geometry.sh_normals.abs()


integrator_registry.add("normals", NormalsIntegrator)

import logging

import torch
from torch import Tensor

from aris.core.scene import Scene
from aris.integrator import Integrator, integrator_registry

logger = logging.getLogger(__name__)


class WhittedIntegrator(Integrator):
    def __init__(self, max_path_length: int, cont_prob: float) -> None:
        super().__init__()
        self.max_path_length = max_path_length
        self.cont_prob = cont_prob

    def render(self, scene: Scene, rays_o: Tensor, rays_d: Tensor) -> Tensor:
        result = torch.zeros_like(rays_d)

        # For Whitted: keep track of the 1/p multiplications
        throughput = torch.ones_like(rays_d)

        # Note: you can also start by initializing the active_indices with all indices,
        # and move the first ray_intersect inside the loop.
        # Doing so may or may not simplify the implementaion, it's up to your preferences.

        # start by shooting the rays into the scene
        geo_out = scene.geometry.ray_intersect(rays_o, rays_d)

        # indices of rays that are being traced
        # these are indices in the inputs, for indexing result and throughput
        active_indices = torch.nonzero(geo_out.mask)[:, 0]  # (N, 1) -> (N,)

        # Whitted loop: we keep tracing the rays that hit specular surfaces,
        # until they hit a diffuse surface (so we sample an emitter),
        # or goes into the void (result is zero),
        # or is terminated by Russian-roulette (result is zero)
        for i_path in range(self.max_path_length):
            if len(active_indices) == 0:
                break

            # YOUR TASK: Distribution Ray Tracing (DRT)
            # DRT 1: Check if a ray hits an emitter; if so, add its contribution

            # DRT 2: Sample an emitter for all the remaining hit points
            #   First, choose an emitter for every hit point
            #   Then, query each emitter with the assigned points, and add their contribution
            #   (You can find an example in emitter_check.py)

            # END OF DRT

            # Whitted 1: change (DRT 2) code above to only points that hit a diffuse surface
            # Whitted 2: continue trace points that hit a specular surface
            pass

            if i_path > 3:
                # Do Russian-roulette after at least 3 bounces
                pass

            # Whitted 3: remove this break
            break

        return result


integrator_registry.add("whitted", WhittedIntegrator)

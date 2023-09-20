import logging

import numpy as np
import torch
import torch.nn.functional as F
from torch import Tensor

from aris.core.scene import Scene
from aris.integrator import Integrator, integrator_registry

logger = logging.getLogger(__name__)


class EmitterCheckIntegrator(Integrator):
    def render(self, scene: Scene, rays_o: Tensor, rays_d: Tensor) -> Tensor:
        device = rays_o.device
        result = torch.zeros_like(rays_d)

        geo_out = scene.geometry.ray_intersect(rays_o, rays_d)

        # indices of rays that are being traced
        active_indices = torch.nonzero(geo_out.mask)[:, 0]  # (N, 1) -> (N,)
        if len(active_indices) == 0:
            return result

        wo = -rays_d[active_indices]

        # sample an emitter for each hit point
        emitter_choices = torch.from_numpy(
            np.random.choice(len(scene.emitters), [len(active_indices)])
        ).to(device)

        # process per emitter
        for i_emitter in range(len(scene.emitters)):
            emitter = scene.emitters[i_emitter]

            # mask for points that are selected to sample this emitter
            em_mask = emitter_choices == i_emitter
            if em_mask.sum() == 0:
                continue

            # sample a point on the emitter
            em_query = emitter.sample(em_mask.sum(), device)

            # query the emitter for luminance towards hit point
            em_query.targets = geo_out.points[active_indices][em_mask]
            em_query.d_target_point = F.normalize(em_query.points - em_query.targets, dim=1)
            emitter.pos_pdf(em_query)
            emitter.le(em_query, scene.geometry)

            # evaluate surface BRDF at hit point towards the emitter
            normals = geo_out.sh_normals[active_indices][em_mask]
            dxy = em_query.d_target_point
            em_brdf = scene.eval_brdf(wo[em_mask], normals, dxy, geo_out.brdf_i[active_indices][em_mask])

            # square distance
            dist = (em_query.targets - em_query.points)
            dist = torch.sum(dist * dist, dim=1, keepdim=True)

            # add contribution
            # note: this is a simplified version of Distributed Ray Tracing
            result[active_indices[em_mask]] = (
                em_query.le / dist * em_brdf.values *
                len(scene.emitters) / em_query.pdf.view(-1, 1)
            )

        return result


integrator_registry.add("emitter_check", EmitterCheckIntegrator)

from dataclasses import dataclass

from aris.config.object_config import ObjectConfig


@dataclass
class SceneConfig:
    brdf: list[ObjectConfig]
    camera: ObjectConfig
    environment: ObjectConfig
    geometry: ObjectConfig
    emitters: list[ObjectConfig]
    width: int
    height: int

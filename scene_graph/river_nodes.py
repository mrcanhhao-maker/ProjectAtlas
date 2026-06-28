from river_geometry import RiverGeometry

from .scene import SceneNode


class RiverSceneNodeFactory:
    """
    Converts river geometry into renderer-independent scene nodes.
    """

    def create(self, geometry: RiverGeometry) -> SceneNode:
        return SceneNode(
            node_type="river",
            payload={
                "polygon_points": geometry.polygon.points,
                "mesh_vertices": geometry.mesh.vertices,
                "mesh_triangles": geometry.mesh.triangles,
            },
        )

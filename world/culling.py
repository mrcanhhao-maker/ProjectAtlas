from typing import Iterable, Tuple

from world.objects import VisibleObject, WorldObject
from world.viewport import Viewport


class ViewportCuller:
    def visible_objects(
        self,
        objects: Iterable[WorldObject],
        viewport: Viewport,
    ) -> Tuple[VisibleObject, ...]:
        visible = []

        for obj in objects:
            if viewport.contains_circle(obj.position, obj.radius):
                visible.append(
                    VisibleObject(
                        object_id=obj.object_id,
                        kind=obj.kind,
                        screen_x=obj.position.x - viewport.left,
                        screen_y=obj.position.y - viewport.top,
                        radius=obj.radius,
                    )
                )

        return tuple(visible)

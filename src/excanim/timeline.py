from __future__ import annotations

from collections import defaultdict

from excanim.anim.base import KeyFrame


class Timeline:
    def __init__(self):
        self._keyframes: list[KeyFrame] = []
        # Index: (element_id, prop) → list of keyframes sorted by t_start
        self._index: dict[tuple[str, str], list[KeyFrame]] = defaultdict(list)

    def add(self, *keyframes: KeyFrame):
        for kf in keyframes:
            self._keyframes.append(kf)
            self._index[(kf.element_id, kf.prop)].append(kf)

    def is_empty(self) -> bool:
        return len(self._keyframes) == 0

    @property
    def duration(self) -> float:
        if not self._keyframes:
            return 0.0
        return max(kf.t_end for kf in self._keyframes)

    def resolve_frame(self, t: float) -> dict[str, dict[str, float]]:
        """Given a time t, return {element_id: {prop: value}} for all animated properties.

        For each (element_id, prop), finds the correct keyframe:
        - If t is within a keyframe's range: interpolate
        - If t is after a keyframe's end: use that keyframe's end value
        - If t is before all keyframes for this prop: use the first keyframe's start value
        """
        result: dict[str, dict[str, float]] = {}

        for (el_id, prop), kfs in self._index.items():
            val = self._resolve_prop(kfs, t)
            if val is not None:
                result.setdefault(el_id, {})[prop] = val

        return result

    def _resolve_prop(self, kfs: list[KeyFrame], t: float) -> float | None:
        """Resolve a single property's value at time t from its keyframes."""
        if not kfs:
            return None

        # Check if t is before the first keyframe
        first = kfs[0]
        if t < first.t_start:
            return first.val_start

        # Find the active or most recently completed keyframe
        for kf in reversed(kfs):
            if t >= kf.t_start:
                return kf.interpolate(t)

        return first.val_start

    def initial_state(self) -> dict[str, dict[str, float]]:
        """Return the state at t=0 — used to set initial values for animated elements."""
        return self.resolve_frame(0.0)

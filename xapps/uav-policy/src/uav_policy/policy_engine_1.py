from dataclasses import dataclass
from typing import Optional, List


@dataclass
class UavState:
    uav_id: str
    x: float
    y: float
    z: float
    slice_id: Optional[str] = None


@dataclass
class RadioSnapshot:
    serving_cell_id: str
    neighbor_cell_ids: List[str]
    rsrp_serving: float
    rsrp_best_neighbor: float
    prb_utilization_serving: float
    prb_utilization_slice: Optional[float] = None


@dataclass
class ResourceDecision:
    uav_id: str
    target_cell_id: str
    slice_id: Optional[str]
    prb_quota: Optional[int]
    reason: str


def simple_path_aware_policy(uav: UavState, radio: RadioSnapshot, overloaded_threshold: float = 0.8) -> ResourceDecision:
    if (
        radio.prb_utilization_serving > overloaded_threshold
        and radio.rsrp_best_neighbor > radio.rsrp_serving + 3.0
        and radio.neighbor_cell_ids
    ):
        target_cell = radio.neighbor_cell_ids[0]
        reason = "Serving cell overloaded, neighbor stronger."
    else:
        target_cell = radio.serving_cell_id
        reason = "Stay on serving cell."

    prb_quota = 20

    return ResourceDecision(
        uav_id=uav.uav_id,
        target_cell_id=target_cell,
        slice_id=uav.slice_id,
        prb_quota=prb_quota,
        reason=reason,
    )

"""Small driver to exercise the policy engine with toy data."""

from uav_policy.policy_engine import (
    UavState,
    RadioSnapshot,
    PathSegmentPlan,
    FlightPlanPolicy,
    ServiceProfile,
    path_aware_rc_policy,
)


def demo() -> None:
    plan = FlightPlanPolicy(
        uav_id="uav-001",
        segments=[
            PathSegmentPlan(
                start_pos=0.0,
                end_pos=0.5,
                planned_cell_id="cell-A",
                slice_id="uav-hd-video",
                base_prb_quota=20,
            ),
            PathSegmentPlan(
                start_pos=0.5,
                end_pos=1.0,
                planned_cell_id="cell-B",
                slice_id="uav-hd-video",
                base_prb_quota=30,
            ),
        ],
    )

    uav = UavState(
        uav_id="uav-001",
        x=100.0,
        y=50.0,
        z=120.0,
        path_position=0.8,
    )
    radio = RadioSnapshot(
        serving_cell_id="cell-A",
        neighbor_cell_ids=["cell-B"],
        rsrp_serving=-90.0,
        rsrp_best_neighbor=-84.0,
        prb_utilization_serving=0.95,
        prb_utilization_slice=0.7,
    )
    service = ServiceProfile(name="uav-hd-video", target_bitrate_mbps=10.0, min_sinr_db=-5.0)

    decision = path_aware_rc_policy(uav, radio, plan=plan, service=service)
    print(decision)


if __name__ == "__main__":
    demo()

from uav_policy.policy_engine import UavState, RadioSnapshot, simple_path_aware_policy
from rc_grpc_client.client import RcGrpcClient, ResourceDecision as RcResourceDecision


def main() -> None:
    client = RcGrpcClient()
    uav = UavState(uav_id="uav-001", x=0.0, y=0.0, z=100.0)
    radio = RadioSnapshot(
        serving_cell_id="cell-A",
        neighbor_cell_ids=["cell-B"],
        rsrp_serving=-90.0,
        rsrp_best_neighbor=-84.0,
        prb_utilization_serving=0.95,
        prb_utilization_slice=0.8,
    )
    decision = simple_path_aware_policy(uav, radio)
    rc_decision = RcResourceDecision(
        uav_id=decision.uav_id,
        target_cell_id=decision.target_cell_id,
        slice_id=decision.slice_id,
        prb_quota=decision.prb_quota,
        notes=decision.reason,
    )
    client.apply_decision(rc_decision)


if __name__ == "__main__":
    main()

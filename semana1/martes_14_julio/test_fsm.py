from fsm_demo import TrafficLightFSM, TrafficLightState


def test_initial_state_is_red():
    fsm = TrafficLightFSM()
    assert fsm.state == TrafficLightState.RED


def test_transition_from_red_to_green():
    fsm = TrafficLightFSM()
    fsm.transition()
    assert fsm.state == TrafficLightState.GREEN


def test_three_transitions_return_to_red():
    fsm = TrafficLightFSM()
    fsm.transition()
    fsm.transition()
    fsm.transition()
    assert fsm.state == TrafficLightState.RED


def test_transition_counter_increments_correctly():
    fsm = TrafficLightFSM()
    assert fsm.cycle_count == 0
    fsm.transition()
    assert fsm.cycle_count == 1
    fsm.transition()
    assert fsm.cycle_count == 2

#!/usr/bin/env python3
"""
EU_10-12 – Practical Task: Logistics State Machine
Task 4: Execute a Logistics Task using FlexBE State Machines

Theory:
  This is the capstone exercise combining EU05 (CV), EU06 (Navigation),
  and EU08 (State Machines). A real iRobot Create 3 robot is used.

  Logistics Workflow:
    S (Start)
     ↓
    [NavToA]     Navigate to Position A
     ↓ reached
    [CheckObj]   Check if object is detected by YOLO camera
     ↓ object    ↓ no_object
    [NavToB]    [NavToC]    Navigate to B (with object) OR C (without)
     ↓           ↓  reached
     ↓          [Wait10s]   Wait 10 seconds (simulate unloading)
     ↓           ↓  done
    [NavToStart]             Return to Start
     ↓
    finished

  Key interfaces:
    /cmd_vel (geometry_msgs/Twist)    → Control robot velocity
    /odom    (nav_msgs/Odometry)      → Get robot position
    YOLO topics (via yolo_ros)        → Object detection
    Nav2 action (/navigate_to_pose)   → Autonomous navigation

  Robot: iRobot Create 3 + Nvidia Jetson Orin Nano
  This file is a FlexBE behavior state machine (Python).
"""

from flexbe_core import (Behavior, Autonomy,
                          OperatableStateMachine,
                          ConcurrencyContainer, PriorityContainer, Logger)

# ── Import the FlexBE states used in this behavior ────────────────────────────
# drive2goal_state: sends a Nav2 navigation goal and waits for completion
# find_object_state: subscribes to YOLO topics, returns 'found' or 'not_found'
# stop_state: sends zero-velocity Twist and confirms robot stopped
from rof_flexbe_states.drive2goal_state import Drive2GoalState
from rof_flexbe_states.find_object_state import FindObjectState
from rof_flexbe_states.stop_state import StopState
from rof_flexbe_states.twist_state import TwistState


class LogisticsTaskSM(Behavior):
    """
    EU_10-12 Logistics Task State Machine.

    Combines navigation, object detection, and timed stops to implement
    an automated logistics workflow on the iRobot Create 3.
    """

    def __init__(self, node):
        super(LogisticsTaskSM, self).__init__()
        self.name = 'logistics_task'

        # ── Initialise ROS2-aware FlexBE containers ───────────────────────────
        OperatableStateMachine.initialize_ros(node)
        ConcurrencyContainer.initialize_ros(node)
        PriorityContainer.initialize_ros(node)
        Logger.initialize(node)
        Drive2GoalState.initialize_ros(node)
        FindObjectState.initialize_ros(node)
        StopState.initialize_ros(node)
        TwistState.initialize_ros(node)

    def create(self):
        """
        Build the state machine graph.
        Outcomes: 'finished' (success), 'failed' (error)

        Positions (adjust for your lab layout):
          Position A: where robot picks up / inspects object
          Position B: destination if object detected
          Position C: destination if no object (unloading bay)
          Start (S): home/dock position
        """
        # Top-level state machine with two final outcomes
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        with _state_machine:
            # ── State 1: Navigate to Position A ──────────────────────────────
            # Drive2GoalState sends a /navigate_to_pose action goal to Nav2.
            # The goal_x, goal_y, goal_yaw are in the 'map' frame.
            # Returns 'arrived' when Nav2 reports SUCCESS.
            OperatableStateMachine.add(
                'NavToA',
                Drive2GoalState(
                    goal_x=1.5,         # meters in map frame
                    goal_y=0.5,
                    goal_yaw=0.0,       # radians (0 = facing +x)
                    cmd_topic='cmd_vel',
                    odom_topic='odom',
                ),
                transitions={
                    'arrived': 'CheckObject',
                    'failed':  'failed',
                },
                autonomy={
                    'arrived': Autonomy.Off,
                    'failed':  Autonomy.Off,
                },
            )

            # ── State 2: Check for Object with YOLO ───────────────────────────
            # FindObjectState subscribes to YOLO detection topics.
            # Waits up to timeout seconds, then returns 'found' or 'not_found'.
            # object_class: COCO class name or index, e.g. 'bottle', 'cup'
            OperatableStateMachine.add(
                'CheckObject',
                FindObjectState(
                    object_class='bottle',    # target object class
                    timeout=5.0,             # seconds to wait for detection
                    confidence_threshold=0.5,
                    camera_topic='/camera/image_raw',
                ),
                transitions={
                    'found':     'NavToB',
                    'not_found': 'NavToC',
                    'failed':    'failed',
                },
                autonomy={
                    'found':     Autonomy.Off,
                    'not_found': Autonomy.Off,
                    'failed':    Autonomy.Off,
                },
            )

            # ── State 3a: Navigate to Position B (object detected) ────────────
            OperatableStateMachine.add(
                'NavToB',
                Drive2GoalState(
                    goal_x=2.5,
                    goal_y=1.0,
                    goal_yaw=1.57,      # facing +y
                    cmd_topic='cmd_vel',
                    odom_topic='odom',
                ),
                transitions={
                    'arrived': 'ReturnToStart',
                    'failed':  'failed',
                },
                autonomy={
                    'arrived': Autonomy.Off,
                    'failed':  Autonomy.Off,
                },
            )

            # ── State 3b: Navigate to Position C (no object) ─────────────────
            OperatableStateMachine.add(
                'NavToC',
                Drive2GoalState(
                    goal_x=0.5,
                    goal_y=2.0,
                    goal_yaw=3.14,      # facing -x
                    cmd_topic='cmd_vel',
                    odom_topic='odom',
                ),
                transitions={
                    'arrived': 'WaitAtC',
                    'failed':  'failed',
                },
                autonomy={
                    'arrived': Autonomy.Off,
                    'failed':  Autonomy.Off,
                },
            )

            # ── State 4: Wait 10 seconds at C (simulate unloading) ────────────
            # TwistState with velocity=0 effectively acts as a timer wait.
            OperatableStateMachine.add(
                'WaitAtC',
                TwistState(
                    target_time=10.0,   # 10 seconds
                    velocity=0.0,       # Don't move
                    rotation_rate=0.0,
                    cmd_topic='cmd_vel',
                ),
                transitions={'done': 'ReturnToStart'},
                autonomy={'done': Autonomy.Off},
            )

            # ── State 5: Return to Start Position ─────────────────────────────
            OperatableStateMachine.add(
                'ReturnToStart',
                Drive2GoalState(
                    goal_x=0.0,
                    goal_y=0.0,
                    goal_yaw=0.0,
                    cmd_topic='cmd_vel',
                    odom_topic='odom',
                ),
                transitions={
                    'arrived': 'StopAtHome',
                    'failed':  'failed',
                },
                autonomy={
                    'arrived': Autonomy.Off,
                    'failed':  Autonomy.Off,
                },
            )

            # ── State 6: Stop and confirm stopped ─────────────────────────────
            OperatableStateMachine.add(
                'StopAtHome',
                StopState(
                    timeout=2.0,
                    cmd_topic='cmd_vel',
                    odom_topic='odom',
                ),
                transitions={
                    'done':   'finished',
                    'failed': 'failed',
                },
                autonomy={
                    'done':   Autonomy.Off,
                    'failed': Autonomy.Off,
                },
            )

        return _state_machine

# Copyright 2024 TIER IV, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import launch
from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.actions import IncludeLaunchDescription
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import PushRosNamespace
from launch_ros.substitutions import FindPackageShare
import yaml


def create_traffic_light_occlusion_predictor(namespace):
    package = FindPackageShare("traffic_light_occlusion_predictor")
    include = PathJoinSubstitution([package, "launch/traffic_light_occlusion_predictor.launch.xml"])

    input_camera_info = f"/sensing/camera/{namespace}/camera_info"
    output_rois = f"/perception/traffic_light_recognition/{namespace}/detection/rois"
    output_traffic_signals = (
        f"/perception/traffic_light_recognition/{namespace}/classification/traffic_signals"
    )

    arguments = {
        "input/cloud": LaunchConfiguration("input/cloud"),
        "input/camera_info": input_camera_info,
        "input/rois": output_rois,
        "input/car/traffic_signals": "classified/car/traffic_signals",
        "input/pedestrian/traffic_signals": "classified/pedestrian/traffic_signals",
        "output/traffic_signals": output_traffic_signals,
    }.items()

    group = GroupAction(
        [
            PushRosNamespace(namespace),
            PushRosNamespace("classification"),
            IncludeLaunchDescription(include, launch_arguments=arguments),
        ]
    )

    return group


def launch_setup(context, *args, **kwargs):
    # Load all camera namespaces
    all_camera_namespaces = LaunchConfiguration("all_camera_namespaces").perform(context)

    # Convert string to list
    all_camera_namespaces = yaml.load(all_camera_namespaces, Loader=yaml.FullLoader)
    if not isinstance(all_camera_namespaces, list):
        print("all_camera_namespaces is not a list")
    if not all((isinstance(v, str) for v in all_camera_namespaces)):
        print("all_camera_namespaces is not a list of strings")

    # Create containers for all cameras
    traffic_light_recognition_containers = [
        create_traffic_light_occlusion_predictor(namespace) for namespace in all_camera_namespaces
    ]
    return traffic_light_recognition_containers


def generate_launch_description():
    return launch.LaunchDescription(
        [
            DeclareLaunchArgument("all_camera_namespaces", description="camera namespace list"),
            OpaqueFunction(function=launch_setup),
        ]
    )

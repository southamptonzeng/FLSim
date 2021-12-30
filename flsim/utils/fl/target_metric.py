#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
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

from enum import Enum

from flsim.utils.fl.stats import RandomVariableStatsTrackerMA, AverageType


class TargetMetricDirection(Enum):
    MIN = "min"
    MAX = "max"


class TargetMetricTracker:
    """
    Tracks the sliding window of eval metric throughout the course of training
    and reports the round if eval metric target is reached
    """

    def __init__(
        self,
        target_value: float,
        window_size: int,
        average_type: AverageType,
        direction: TargetMetricDirection,
    ):
        self._stats = RandomVariableStatsTrackerMA(
            window_size=window_size, mode=average_type
        )
        self.target_value = target_value
        self.window_size = window_size
        self.direction = direction

    def update_and_check_target(
        self,
        current_eval_metric: float,
    ) -> bool:
        """
        Updates the stats tracker with latest eval metric
        Return value:
            True if target metric is reached.
        """
        self._stats.update(current_eval_metric)
        if self._stats.num_samples < self.window_size:
            return False
        return (
            self._stats.mean() > self.target_value
            if self.direction == TargetMetricDirection.MAX
            else self._stats.mean() < self.target_value
        )

    @property
    def mean(self):
        return self._stats.mean()

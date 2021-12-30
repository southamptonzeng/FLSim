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

import abc
from typing import Any, List

import torch


class IFLBatchMetrics(abc.ABC):
    """Each forward run of FL Model (i.e. concrete implementation of IFLModel
    in PyML) will return an IFLBatchMetrics object. This is an encapsulation
    and abstraction around several useful/common metrics such as loss,
    num_examples, predictions, and targets so that IFLMetricsReporter can
    aggregate metrics from any kind of model as long as the model returns
    IFLBatchMetrics.
    """

    @property
    @abc.abstractmethod
    def loss(self) -> torch.Tensor:
        pass

    @property
    @abc.abstractmethod
    def num_examples(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def predictions(self) -> List[Any]:
        pass

    @property
    @abc.abstractmethod
    def targets(self) -> List[Any]:
        pass

    @property
    @abc.abstractmethod
    def model_inputs(self) -> Any:
        pass

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

import numpy as np
import pytest
from flsim.common.pytest_helper import assertEqual
from flsim.utils.async_trainer.async_example_weights import (
    AsyncExampleWeightConfig,
    ExampleWeight,
)
from flsim.utils.tests.helpers.async_weights_test_utils import (  # noqa
    AsyncExampleWeightsTestUtils,
)
from hydra.utils import instantiate


class TestAsyncExampleWeights:
    @pytest.mark.parametrize(
        "example_weight_config, example_weight_class",
        AsyncExampleWeightsTestUtils.EXAMPLE_WEIGHT_TEST_CONFIGS,
    )
    def test_string_conversion(
        self,
        example_weight_config: AsyncExampleWeightConfig,
        example_weight_class: ExampleWeight,
    ):
        """Check that strings are correctly converted to ExampleWeight"""
        obj = instantiate(example_weight_config)
        assertEqual(obj.__class__, example_weight_class)

    @pytest.mark.parametrize(
        "example_weight_config, example_weight_class",
        AsyncExampleWeightsTestUtils.EXAMPLE_WEIGHT_TEST_CONFIGS,
    )
    @pytest.mark.parametrize(
        "avg_num_examples",
        AsyncExampleWeightsTestUtils.AVG_NUMBER_OF_EXAMPLES,
    )
    def test_example_weight_compute(
        self,
        example_weight_config: AsyncExampleWeightConfig,
        example_weight_class: ExampleWeight,
        avg_num_examples: int,
    ):
        """Test that all weight computation works as expected"""
        # generate 10 random integers
        max_num_examples = 10000
        for _ in range(10):
            num_examples = np.random.randint(1, max_num_examples)
            example_weight_config.avg_num_examples = avg_num_examples
            obj = instantiate(example_weight_config)
            assertEqual(
                obj.weight(num_examples),
                AsyncExampleWeightsTestUtils.expected_weight(
                    avg_num_examples=avg_num_examples,
                    num_examples=num_examples,
                    example_weight_class=example_weight_class,
                ),
            )

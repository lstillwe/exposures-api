# coding: utf-8

"""
    Environmental Exposures API

    API for environmental exposure models for NIH Data Translator program

    OpenAPI spec version: 1.0.0
    Contact: stealey@renci.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from __future__ import absolute_import

import os
import sys
import unittest

import exposures_api
from exposures_api.rest import ApiException
from exposures_api.apis.default_api import DefaultApi


class TestDefaultApi(unittest.TestCase):
    """ DefaultApi unit test stubs """

    def setUp(self):
        self.api = exposures_api.apis.default_api.DefaultApi()

    def tearDown(self):
        pass

    def test_exposures_exposure_type_coordinates_get(self):
        """
        Test case for exposures_exposure_type_coordinates_get

        Get exposure location(s) as latitude, longitude coordinates
        """
        pass

    def test_exposures_exposure_type_dates_get(self):
        """
        Test case for exposures_exposure_type_dates_get

        Get exposure start date and end date range for exposure type
        """
        pass

    def test_exposures_exposure_type_scores_get(self):
        """
        Test case for exposures_exposure_type_scores_get

        Get exposure score for a given environmental factor at exposure location(s)
        """
        pass

    def test_exposures_exposure_type_values_get(self):
        """
        Test case for exposures_exposure_type_values_get

        Get exposure value for a given environmental factor at exposure location(s)
        """
        pass

    def test_exposures_get(self):
        """
        Test case for exposures_get

        Get list of exposure types
        """
        pass


if __name__ == '__main__':
    unittest.main()

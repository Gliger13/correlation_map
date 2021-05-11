import pytest

from test_framework.asserts.image.image import check_find_image_rotation_angle
from test_framework.tools.common.data_factory import get_test_data


@pytest.mark.parametrize('test_data', get_test_data(__file__))
def test_find_image_rotation_angle(test_data, test_source_image, test_expected_image):
    check_find_image_rotation_angle(test_source_image, test_expected_image)

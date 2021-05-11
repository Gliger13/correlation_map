import pytest

from test_framework.asserts.image.image import check_rotate_image
from test_framework.tools.common.data_factory import get_test_data


@pytest.mark.parametrize('test_data', get_test_data(__file__))
def test_rotate_image(test_data, test_source_image, test_expected_image):
    check_rotate_image(test_source_image, test_expected_image)

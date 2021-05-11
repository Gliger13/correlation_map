import pytest

from test_framework.asserts.image.image import check_gray_transformation
from test_framework.tools.common.data_factory import get_test_data


@pytest.mark.parametrize('test_data', get_test_data(__file__))
def test_gray_transformation(test_data, test_image, test_gray_image):
    check_gray_transformation(test_image, test_gray_image)

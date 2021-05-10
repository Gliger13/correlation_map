import os

import pytest

from core.image import Image
from test_framework.tools.common.root_path import get_abs_root_path


@pytest.fixture
def test_image(test_data):
    image_url = test_data.get('test_image_path')
    root_path = get_abs_root_path(__file__)
    return Image(os.path.join(root_path, image_url))


@pytest.fixture
def test_gray_image(test_data):
    image_url = test_data.get('test_gray_image_path')
    root_path = get_abs_root_path(__file__)
    return Image(os.path.join(root_path, image_url))

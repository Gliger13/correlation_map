"""Module contains image chooser combo box model"""
from PyQt5.QtWidgets import QComboBox

from core.images.image_container import ImageContainer


class ImageChooserComboBox(QComboBox):
    """Combo box to choose images"""

    def __init__(self):
        super().__init__()
        self.update_items()

    def update_items(self):
        """Update all items in the current chooser combobox

        Update items in the current chooser combobox in alphabetic order with the items from the image container
        """
        current_choice = self.currentText()
        self.clear()
        self.addItems(sorted([image_type.capitalize() for image_type in ImageContainer.get_loaded_image_types()]))
        self.setCurrentText(current_choice)

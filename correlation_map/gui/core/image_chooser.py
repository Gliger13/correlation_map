"""Module contains image chooser combo box model"""
from PyQt5.QtWidgets import QComboBox

from correlation_map.core.models.figures.figure_container import FigureContainer


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
        self.addItems(sorted([image_type.capitalize() for image_type in FigureContainer.get_all_figure_types()]))
        self.setCurrentText(current_choice)

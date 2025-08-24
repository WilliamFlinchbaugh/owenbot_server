from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QGridLayout, QPushButton
)

class DirectionalPad(QWidget):
    """A directional pad widget with 8 directional buttons arranged in a 3x3 grid."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Create the main layout
        layout = QGridLayout(self)
        layout.setSpacing(2)
        
        self.directions = {
            (0, 1): ("N", "↑", (0, 1)),      # North
            (0, 2): ("NE", "↗", (0.7, 0.7)),  # Northeast
            (1, 2): ("E", "→", (1, 0)),      # East
            (2, 2): ("SE", "↘", (0.7, -0.7)), # Southeast
            (2, 1): ("S", "↓", (0, -1)),     # South
            (2, 0): ("SW", "↙", (-0.7, -0.7)), # Southwest
            (1, 0): ("W", "←", (-1, 0)),     # West
            (0, 0): ("NW", "↖", (-0.7, 0.7))   # Northwest
        }
        
        self.direction_map = {x[0]: x[2] for x in self.directions.values()}
        
        # Create buttons for each direction
        self.buttons = {}
        self.current_direction = None
        self.current_coordinates = (0, 0)
        
        for (row, col), (direction, arrow, coords) in self.directions.items():
            button = QPushButton(arrow)
            button.setMinimumSize(60, 60)
            button.setMaximumSize(60, 60)
            
            # Set font for the arrow
            font = QFont()
            font.setPointSize(16)
            button.setFont(font)
            
            # Connect button press and release events
            button.pressed.connect(lambda d=direction, c=coords: self.on_direction_pressed(d, c))
            button.released.connect(self.on_direction_released)
            
            # Store button reference
            self.buttons[direction] = button
            
            # Add button to layout
            layout.addWidget(button, row, col)
        
        # Add empty space in the center (row 1, col 1)
        center_widget = QWidget()
        center_widget.setMinimumSize(60, 60)
        center_widget.setMaximumSize(60, 60)
        center_widget.setStyleSheet("background-color: transparent;")
        layout.addWidget(center_widget, 1, 1)
        
        # Set the layout size constraints
        self.setFixedSize(186, 186)  # 3 * 60 + 2 * 3 spacing
        
    def on_direction_pressed(self, direction, coordinates):
        """Handle direction button press."""
        self.current_direction = direction
        self.current_coordinates = coordinates
        
    def on_direction_released(self):
        """Handle direction button release - return to rest state."""
        self.current_direction = "REST"
        self.current_coordinates = (0, 0)
        
    def dpadPos(self):
        return self.current_coordinates

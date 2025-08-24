from PySide6.QtWidgets import QApplication, QWidget, QStyleFactory, QMainWindow, QGridLayout
from PySide6.QtCore import QPointF, QRectF, QLineF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor
import sys
import math


class Joystick(QWidget):
    
    # joystick_signal = Signal(tuple[float, float])
    
    def __init__(self, parent=None):
        super(Joystick, self).__init__(parent)
        self.setMinimumSize(100, 100)
        self.movingOffset = QPointF(0, 0)
        self.grabCenter = False
        self.__maxDistance = 50
        self.deadzone_angle = 6
        self.cardinal_dirs = [
            (0, 1, 0),
            (90, 0, 1),
            (180, -1, 0),
            (-90, 0, -1),
        ]
    
    def paintEvent(self, event):
        painter = QPainter(self)
        bounds = QRectF(-self.__maxDistance, 
                        -self.__maxDistance, 
                        self.__maxDistance*2, 
                        self.__maxDistance*2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(QColor(0, 0, 255))
        painter.drawEllipse(self._centerEllipse())
    
    def _centerEllipse(self):
        if self.grabCenter:
            return QRectF(-20, -20, 40, 40).translated(self.movingOffset)
        return QRectF(-20, -20, 40, 40).translated(self._center())
    
    def _center(self):
        return QPointF(self.width()/2, self.height()/2)
    
    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), point)
        if limitLine.length() > self.__maxDistance:
            limitLine.setLength(self.__maxDistance)
        return limitLine.p2()
    
    def mousePressEvent(self, ev):
        self.grabCenter = self._centerEllipse().contains(ev.position())
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, event):
        self.grabCenter = False
        self.movingOffset = QPointF(0.0, 0.0)
        self.update()

    def mouseMoveEvent(self, event):
        if self.grabCenter:
            self.movingOffset = self._boundJoystick(event.position())
            self.update()
    
    def joystickPos(self): # returns x, y position
        if not self.grabCenter:
            return 0.0, 0.0
        normVector = QLineF(self._center(), self.movingOffset)
        x, y = normVector.dx()/self.__maxDistance, -normVector.dy()/self.__maxDistance
        magnitude = math.sqrt(x*x + y*y)
        angle = math.degrees(math.atan2(y, x))
        angle = angle + 360 if angle < 0 else angle
        
        # check for deadzones
        for target_deg, target_x, target_y in self.cardinal_dirs:
            # handle wrap-around
            if target_deg == 0:
                if angle <= self.deadzone_angle or angle >= (360 - self.deadzone_angle):
                    return target_x*magnitude, target_y*magnitude
            else:
                if abs(angle - target_deg) <= self.deadzone_angle:
                    return target_x*magnitude, target_y*magnitude
        
        # no deadzone
        return x, y
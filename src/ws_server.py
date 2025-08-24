from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtNetwork import QHostAddress
from PySide6.QtCore import QObject, Signal

class WSServer(QObject):
    client_connected = Signal()
    client_disconnected = Signal()
    message_sent = Signal(str)  # message
    message_received = Signal(str)  # message
    
    def __init__(self, port=9876, parent=None):
        super(WSServer, self).__init__(parent)
        
        self.client = None
        self.server = QWebSocketServer(
            "owenBot Server", 
            QWebSocketServer.SslMode.NonSecureMode, 
            self
        )
        
        self.server.newConnection.connect(self.on_new_connection)
        self.server.listen(QHostAddress('0.0.0.0'), port)
    
    def send_message(self, message: str):
        # don't send if we don't have a client
        if self.client is None:
            return
        
        self.client.sendTextMessage(message)
        self.message_sent.emit(message)
    
    def on_new_connection(self):
        # only handle new connection if we don't have a client right now
        if self.client is not None:
            return
        
        self.client = self.server.nextPendingConnection()
        self.client.textMessageReceived.connect(self.on_message_received)
        self.client.disconnected.connect(self.on_client_disconnected)
        self.server.pauseAccepting()
        self.client_connected.emit()
    
    def on_message_received(self, message):
        self.message_received.emit(message)
    
    def on_client_disconnected(self):
        if self.sender() == self.client:
            self.client_disconnected.emit()
            self.client = None
            self.sender().deleteLater()
            self.server.resumeAccepting()
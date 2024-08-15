import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import cut

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path = None  # Variable to store the file path
        self.pieces = None  # Variable to store the number of pieces
        self.destination_folder = None  # Variable to store the destination folder
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video File Selector')
        self.setFixedSize(400, 200)  # Set a fixed size for the window

        # Set up drag-and-drop
        self.setAcceptDrops(True)

        # Create layout
        layout = QVBoxLayout()

        # Create a label to display the selected file path
        self.file_label = QLabel('No file selected', self)
        self.file_label.setStyleSheet("font-size: 16px; padding: 10px;")  # Style the label
        self.file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.file_label)

        # Create a button to open the file dialog
        self.open_button = QPushButton('Select Video File', self)
        self.open_button.setStyleSheet("font-size: 14px; padding: 10px;")  # Style the button
        self.open_button.clicked.connect(self.openFileDialog)
        layout.addWidget(self.open_button)

        # Create a "Done" button
        self.done_button = QPushButton('Done', self)
        self.done_button.setStyleSheet("font-size: 14px; padding: 10px;")  # Style the button
        self.done_button.clicked.connect(self.confirmExit)
        layout.addWidget(self.done_button)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #a3e4d7;
            }
            QPushButton {
                background-color: #566573;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                color: #333;
            }
        """)

    def openFileDialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        
        if file_path:
            self.file_label.setText(f"Selected file: {file_path}")
            self.file_path = file_path  # Store the file path

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path:
                self.file_label.setText(f"Selected file: {file_path}")
                self.file_path = file_path  # Store the file path

    def confirmExit(self):
        if self.file_path:
            print(f"File path stored: {self.file_path}")
            pieces, ok = QInputDialog.getInt(self, 'Input', 'How many pieces do you want to divide the video into?', min=1)
            if ok:
                self.pieces = pieces
                print(f"Number of pieces: {self.pieces}")
                self.selectDestinationFolder()
            else:
                QMessageBox.warning(self, 'Input Required', 'Please specify the number of pieces.')
        else:
            print("No file selected")
            QMessageBox.warning(self, 'No File Selected', 'Please select a file first.')

    def selectDestinationFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder_path:
            self.destination_folder = folder_path
            print(f"Destination folder: {self.destination_folder}")
            reply = QMessageBox.question(self, 'Confirmation', 'Are you sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                #splitting the video
                cut.split_video(self.file_path,self.pieces,self.destination_folder)
                self.close()  # Close the window
        else:
            QMessageBox.warning(self, 'No Folder Selected', 'Please select a destination folder.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileSelector()
    ex.show()
    sys.exit(app.exec_())

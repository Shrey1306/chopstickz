"""PyQt5-based video editor with LLM-guided editing capabilities."""

import sys
import tempfile
import cv2
import ffmpeg
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QFileDialog,
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class VideoProcessor(QThread):
    """Thread-based video processor with editing operations."""

    update_signal = pyqtSignal(QImage)
    finished = pyqtSignal()

    def __init__(self, video_path: str):
        super().__init__()
        self.original_video_path = video_path
        self.video_path = video_path
        self.video_history = [video_path]
        self.running = True
        self.trim_required = False
        self.start_sec = 0
        self.end_sec = 0

    def run(self):
        while self.running:
            if self.trim_required:
                self.trim_video(self.start_sec, self.end_sec)
                self.trim_required = False
                self.finished.emit()
            self.play_video()

    def trim_video(self, trim_start_sec: float, trim_end_sec: float):
        """Trim video from both ends by specified seconds."""
        probe = ffmpeg.probe(self.video_path)
        total_duration = float(probe["format"]["duration"])

        adjusted_start_sec = trim_start_sec
        adjusted_end_sec = total_duration - trim_end_sec
        duration_to_keep = adjusted_end_sec - adjusted_start_sec

        if duration_to_keep <= 0:
            print("Error: The resulting duration is non-positive after trimming.")
            return

        temp_video_path = tempfile.mktemp(suffix=".mp4")

        try:
            (
                ffmpeg.input(self.video_path, ss=adjusted_start_sec, t=duration_to_keep)
                .output(temp_video_path, c="copy")
                .run(overwrite_output=True)
            )
            self.video_path = temp_video_path
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            stderr = e.stderr.decode() if e.stderr else "Unknown FFmpeg error"
            print(f"Failed to trim video: {stderr}")

    def crop_video(self, scale: float):
        """Crop video to specified aspect ratio scale."""
        probe = ffmpeg.probe(self.video_path)
        video_stream = next(
            (s for s in probe["streams"] if s["codec_type"] == "video"), None
        )
        original_width = int(video_stream["width"])
        original_height = int(video_stream["height"])

        new_width = int(original_height * scale)
        if new_width % 2 != 0:
            new_width -= 1

        x_offset = (original_width - new_width) // 2
        crop_filter = f"{new_width}:{original_height}:{x_offset}:0"
        temp_video_path = tempfile.mktemp(suffix=".mp4")

        try:
            (
                ffmpeg.input(self.video_path)
                .filter("crop", *crop_filter.split(":"))
                .output(temp_video_path, vcodec="libx264", crf=22)
                .overwrite_output()
                .run()
            )
            self.video_path = temp_video_path
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to crop video: {e.stderr.decode('utf-8')}")

    def zoom_video(self, zoom_scale: float):
        """Zoom into video by specified scale factor."""
        probe = ffmpeg.probe(self.video_path)
        video_stream = next(
            (s for s in probe["streams"] if s["codec_type"] == "video"), None
        )
        original_width = int(video_stream["width"])
        original_height = int(video_stream["height"])

        new_width = int(original_width * zoom_scale)
        new_height = int(original_height * zoom_scale)
        new_width += new_width % 2
        new_height += new_height % 2

        x_offset = (original_width - new_width) // 2
        y_offset = (original_height - new_height) // 2
        temp_video_path = tempfile.mktemp(suffix=".mp4")

        try:
            (
                ffmpeg.input(self.video_path)
                .filter("crop", w=new_width, h=new_height, x=x_offset, y=y_offset)
                .output(temp_video_path, vcodec="libx264", crf=22)
                .overwrite_output()
                .run()
            )
            self.video_path = temp_video_path
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to zoom video: {e.stderr.decode('utf-8')}")

    def change_speed(self, speed_factor: float):
        """Change video playback speed."""
        temp_video_path = tempfile.mktemp(suffix=".mp4")

        try:
            (
                ffmpeg.input(self.video_path)
                .filter("setpts", f"{1/speed_factor}*PTS")
                .output(temp_video_path, vcodec="libx264", crf=22)
                .run(overwrite_output=True)
            )
            self.video_path = temp_video_path
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to change video speed: {e.stderr.decode('utf-8')}")

    def fade_in_video(self, duration: int = 2):
        """Apply fade-in effect to video."""
        temp_video_path = tempfile.mktemp(suffix=".mp4")

        try:
            (
                ffmpeg.input(self.video_path)
                .filter("fade", t="in", d=duration)
                .output(temp_video_path, vcodec="libx264", crf=22)
                .run(overwrite_output=True)
            )
            self.video_path = temp_video_path
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to apply fade in effect: {e.stderr.decode('utf-8')}")

    def fade_out_video(self, duration: int = 2):
        """Apply fade-out effect to video."""
        temp_video_path = tempfile.mktemp(suffix=".mp4")
        probe = ffmpeg.probe(self.video_path)
        total_duration = float(probe["format"]["duration"])
        fade_start = total_duration - duration

        try:
            (
                ffmpeg.input(self.video_path)
                .filter("fade", t="out", start_time=fade_start, d=duration)
                .output(temp_video_path, vcodec="libx264", crf=22)
                .run(overwrite_output=True)
            )
            self.video_path = temp_video_path
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to apply fade out effect: {e.stderr.decode('utf-8')}")

    def play_video(self):
        """Play video and emit frames for display."""
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                cap.release()
                cap = cv2.VideoCapture(self.video_path)
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(
                rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888
            )
            scaled = image.scaled(640, 480, Qt.KeepAspectRatio)
            self.update_signal.emit(scaled)
            QThread.msleep(int(1000 / fps))

        cap.release()

    def start_playback(self):
        """Start video playback."""
        self.running = True
        if not self.isRunning():
            self.start()

    def pause_playback(self):
        """Pause video playback."""
        self.running = False
        self.wait()

    def undo_last_action(self):
        """Undo the last editing action."""
        if len(self.video_history) > 1:
            self.video_history.pop()
            self.video_path = self.video_history[-1]
            print("Last action undone.")
        else:
            print("No actions to undo.")


class VideoEditorApp(QWidget):
    """Main video editor application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM Guided Video Editor")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.video_label = QLabel("Video Display Here")
        self.upload_button = QPushButton("Upload Video")
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText(
            'Enter command (e.g., "trim the video by 1 second on each side", "undo")'
        )
        self.command_input.returnPressed.connect(self.process_command)
        self.upload_button.clicked.connect(self.upload_video)

        self.layout.addWidget(self.upload_button)
        self.layout.addWidget(self.video_label)
        self.layout.addWidget(self.command_input)
        self.setLayout(self.layout)

        self.video_processor = VideoProcessor("./stock.mp4")
        self.video_processor.update_signal.connect(self.update_image)
        self.video_processor.finished.connect(self.on_finished_trim)

    def upload_video(self):
        """Open file dialog to upload a video."""
        video_path, _ = QFileDialog.getOpenFileName(
            self, "Select Video", "", "Video Files (*.mp4 *.avi *.mov)"
        )
        if video_path:
            self.video_processor.pause_playback()
            self.video_processor = VideoProcessor(video_path)
            self.video_processor.update_signal.connect(self.update_image)
            self.video_processor.finished.connect(self.on_finished_trim)
            self.video_processor.start_playback()

    def update_image(self, image: QImage):
        """Update the video display with a new frame."""
        self.video_label.setPixmap(
            QPixmap.fromImage(image).scaled(
                self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def process_command(self):
        """Process user command for video editing."""
        command = self.command_input.text().lower()

        if command == "undo":
            self.video_processor.pause_playback()
            self.video_processor.undo_last_action()
            self.video_processor.start_playback()

        elif command == "fade in":
            self.video_processor.pause_playback()
            self.video_processor.fade_in_video(2)
            self.video_processor.start_playback()

        elif command == "fade out":
            self.video_processor.pause_playback()
            self.video_processor.fade_out_video(2)
            self.video_processor.start_playback()

        elif command == "zoom in":
            self.video_processor.pause_playback()
            self.video_processor.zoom_video(0.9)
            self.video_processor.start_playback()

        elif "speed up" in command:
            self._handle_speed_command(command, speedup=True)

        elif "slow down" in command:
            self._handle_speed_command(command, speedup=False)

        elif command.startswith("trim the video by") and command.endswith("seconds on each side"):
            parts = command.split()
            seconds = int(parts[4])
            self.video_processor.pause_playback()
            self.video_processor.start_sec = seconds
            self.video_processor.end_sec = seconds
            self.video_processor.trim_required = True
            self.video_processor.start_playback()

        elif command == "crop to mobile dimensions":
            self.video_processor.pause_playback()
            self.video_processor.crop_video(9 / 16)
            self.video_processor.start_playback()

        else:
            QMessageBox.warning(self, "Error", "Invalid command format. Please try again.")

    def _handle_speed_command(self, command: str, speedup: bool):
        """Handle speed up/down commands."""
        try:
            parts = command.split()
            factor = float(parts[-1])
            self.video_processor.pause_playback()
            if speedup:
                self.video_processor.change_speed(factor)
            else:
                self.video_processor.change_speed(1 / factor)
            self.video_processor.start_playback()
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid speed factor. Please try again.")

    def on_finished_trim(self):
        """Handle trim completion."""
        print("Trimmed")


def main():
    """Run the video editor application."""
    app = QApplication(sys.argv)
    editor = VideoEditorApp()
    editor.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


"""
Entry point for the Isaac AI Agent desktop application.

Usage:
    python -m isaac_agent.desktop
    isaac-agent-desktop  (via console_scripts)
"""

import sys
import signal


def main():
    """Launch the PyQt6 desktop application."""
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QFont

    from isaac_agent.desktop.main_window import MainWindow

    # Allow Ctrl+C to terminate
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setApplicationName("Isaac AI Agent")
    app.setOrganizationName("IsaacAgent")
    app.setApplicationVersion("0.1.0")

    # Set default application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create and show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

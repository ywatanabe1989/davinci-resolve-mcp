"""
Continuous Screenshot Capture for DaVinci Resolve MCP Server.

Provides background screenshot capture for monitoring workflows.
"""

import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from .capture import capture_screenshot, DEFAULT_OUTPUT_DIR


class ContinuousCapture:
    """Continuous screenshot capture for monitoring."""

    def __init__(
        self,
        output_dir: str = DEFAULT_OUTPUT_DIR,
        interval_sec: float = 1.0,
        quality: int = 60,
        monitor_id: int = 0,
        capture_all: bool = False,
    ):
        self.output_dir = Path(output_dir)
        self.interval_sec = interval_sec
        self.quality = quality
        self.monitor_id = monitor_id
        self.capture_all = capture_all

        self.running = False
        self.thread = None
        self.screenshot_count = 0
        self.session_id = None

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def start(self, session_id: str = None):
        """Start continuous capture."""
        if self.running:
            return

        self.running = True
        self.screenshot_count = 0
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")

        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop continuous capture."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def _capture_loop(self):
        """Main capture loop."""
        while self.running:
            start_time = time.time()

            filename = f"{self.session_id}_{self.screenshot_count:04d}.jpg"
            output_path = str(self.output_dir / filename)

            result = capture_screenshot(
                output_path=output_path,
                quality=self.quality,
                monitor_id=self.monitor_id,
                capture_all=self.capture_all,
            )

            if result.get("success"):
                self.screenshot_count += 1

            # Sleep for remaining interval
            elapsed = time.time() - start_time
            sleep_time = max(0.01, self.interval_sec - elapsed)
            time.sleep(sleep_time)

    def get_status(self) -> Dict[str, Any]:
        """Get capture status."""
        return {
            "running": self.running,
            "session_id": self.session_id,
            "screenshot_count": self.screenshot_count,
            "output_dir": str(self.output_dir),
            "interval_sec": self.interval_sec,
        }


# Global instance for MCP tools
_capture_instance: Optional[ContinuousCapture] = None


def start_monitoring(
    output_dir: str = DEFAULT_OUTPUT_DIR,
    interval_sec: float = 1.0,
    quality: int = 60,
    monitor_id: int = 0,
    capture_all: bool = False,
) -> Dict[str, Any]:
    """Start continuous screenshot monitoring."""
    global _capture_instance

    if _capture_instance and _capture_instance.running:
        return {"success": False, "error": "Monitoring already running"}

    _capture_instance = ContinuousCapture(
        output_dir=output_dir,
        interval_sec=interval_sec,
        quality=quality,
        monitor_id=monitor_id,
        capture_all=capture_all,
    )
    _capture_instance.start()

    return {
        "success": True,
        "message": f"Started monitoring (interval: {interval_sec}s)",
        "session_id": _capture_instance.session_id,
        "output_dir": output_dir,
    }


def stop_monitoring() -> Dict[str, Any]:
    """Stop continuous screenshot monitoring."""
    global _capture_instance

    if not _capture_instance or not _capture_instance.running:
        return {"success": False, "error": "Monitoring not running"}

    status = _capture_instance.get_status()
    _capture_instance.stop()
    _capture_instance = None

    return {
        "success": True,
        "message": "Monitoring stopped",
        "screenshots_captured": status["screenshot_count"],
    }


def get_monitoring_status() -> Dict[str, Any]:
    """Get current monitoring status."""
    if not _capture_instance:
        return {"running": False, "message": "No active monitoring session"}

    return _capture_instance.get_status()

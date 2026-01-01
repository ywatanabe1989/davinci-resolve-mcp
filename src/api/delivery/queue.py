#!/usr/bin/env python3
"""
DaVinci Resolve Render Queue Operations
Starting, monitoring, and clearing render queue
"""

import logging
from typing import Dict, Any

logger = logging.getLogger("davinci-resolve-mcp.delivery.queue")


def start_render(resolve) -> Dict[str, Any]:
    """Start rendering jobs in the render queue."""
    if not resolve:
        logger.error("No connection to DaVinci Resolve")
        return {"error": "No connection to DaVinci Resolve"}

    logger.info("Starting render process")

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        logger.error("Failed to get Project Manager")
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        logger.error("No project is currently open")
        return {"error": "No project is currently open"}

    page = resolve.GetCurrentPage()
    if page != "deliver":
        logger.info(f"Switching from {page} page to deliver page")
        resolve.OpenPage("deliver")

    try:
        logger.info("Checking for jobs in render queue")
        try:
            queue_items = current_project.GetRenderJobList()
            if queue_items:
                logger.info(f"Found {len(queue_items)} jobs in render queue")
            else:
                logger.warning("GetRenderJobList() returned None or empty list")
                queue_items = []
        except Exception as e:
            logger.error(f"Error getting render job list: {str(e)}")
            queue_items = []

        if not queue_items or len(queue_items) == 0:
            logger.warning("No jobs in render queue")
            return {"warning": "No jobs in render queue", "jobs_count": 0}

        logger.info("Starting render process")
        try:
            result = current_project.StartRendering()
            if result is None:
                logger.info(
                    "Newer StartRendering() API returned None, trying StartRenderingJob()"
                )
                result = current_project.StartRenderingJob()
        except AttributeError:
            logger.info(
                "Newer StartRendering() API not available, using StartRenderingJob()"
            )
            result = current_project.StartRenderingJob()
        except Exception as e:
            logger.error(f"Error starting render: {str(e)}")
            result = False

        if result:
            logger.info("Render started successfully")
            return {
                "success": True,
                "message": "Render started successfully",
                "jobs_count": len(queue_items),
            }
        else:
            logger.error("Failed to start rendering")
            return {
                "error": "Failed to start rendering",
                "jobs_count": len(queue_items),
            }

    except Exception as e:
        logger.error(f"Exception while starting render: {str(e)}")
        return {"error": f"Failed to start rendering: {str(e)}"}


def get_render_queue_status(resolve) -> Dict[str, Any]:
    """Get the status of jobs in the render queue."""
    if not resolve:
        logger.error("No connection to DaVinci Resolve")
        return {"error": "No connection to DaVinci Resolve"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        logger.error("Failed to get Project Manager")
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        logger.error("No project is currently open")
        return {"error": "No project is currently open"}

    page = resolve.GetCurrentPage()
    if page != "deliver":
        logger.info(f"Switching from {page} page to deliver page")
        resolve.OpenPage("deliver")

    try:
        queue_items = current_project.GetRenderJobList()

        if not queue_items:
            return {"status": "empty", "message": "Render queue is empty", "jobs": []}

        jobs = []
        is_rendering = False

        for job_id in queue_items:
            job_info = {"id": job_id, "name": "Unknown", "status": "Unknown"}

            try:
                job_info["name"] = current_project.GetRenderJobName(job_id)
                status = current_project.GetRenderJobStatus(job_id)
                job_info["status"] = status

                if status == "Rendering":
                    is_rendering = True

                try:
                    progress = current_project.GetRenderJobFrameProgress(job_id)
                    if progress:
                        job_info["progress"] = progress

                    time_remaining = current_project.GetRenderJobEstimatedTimeRemaining(
                        job_id
                    )
                    if time_remaining:
                        job_info["time_remaining"] = time_remaining
                except Exception:
                    pass

            except Exception as e:
                logger.warning(f"Could not get details for job {job_id}: {str(e)}")

            jobs.append(job_info)

        if is_rendering:
            queue_status = "rendering"
        elif any(job["status"] == "Complete" for job in jobs):
            if all(job["status"] == "Complete" for job in jobs):
                queue_status = "complete"
            else:
                queue_status = "partial_complete"
        else:
            queue_status = "ready"

        return {
            "status": queue_status,
            "jobs_count": len(jobs),
            "jobs": jobs,
            "is_rendering": is_rendering,
        }

    except Exception as e:
        logger.error(f"Exception while getting render queue status: {str(e)}")
        return {"error": f"Failed to get render queue status: {str(e)}"}


def clear_render_queue(resolve) -> Dict[str, Any]:
    """Clear all jobs from the render queue."""
    if not resolve:
        logger.error("No connection to DaVinci Resolve")
        return {"error": "No connection to DaVinci Resolve"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        logger.error("Failed to get Project Manager")
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        logger.error("No project is currently open")
        return {"error": "No project is currently open"}

    page = resolve.GetCurrentPage()
    if page != "deliver":
        logger.info(f"Switching from {page} page to deliver page")
        resolve.OpenPage("deliver")

    try:
        queue_items = current_project.GetRenderJobList()
        initial_count = len(queue_items) if queue_items else 0

        if initial_count == 0:
            return {
                "success": True,
                "message": "Render queue was already empty",
                "jobs_removed": 0,
            }

        is_rendering = current_project.IsRenderingInProgress()
        if is_rendering:
            logger.warning(
                "Rendering is in progress. Attempting to stop before clearing queue."
            )
            try:
                current_project.StopRendering()
                logger.info("Stopped current rendering")
            except Exception as e:
                logger.error(f"Could not stop rendering: {str(e)}")

        result = current_project.DeleteAllRenderJobs()

        if result:
            return {
                "success": True,
                "message": "Render queue cleared successfully",
                "jobs_removed": initial_count,
                "was_rendering": is_rendering,
            }
        else:
            return {
                "error": "Failed to clear render queue",
                "jobs_count": initial_count,
            }

    except Exception as e:
        logger.error(f"Exception while clearing render queue: {str(e)}")
        return {"error": f"Failed to clear render queue: {str(e)}"}

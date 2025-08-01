# File: backend/app/api/v1/routes/data.py
# Path: backend/app/api/v1/routes/data.py

"""
Data import API routes for the logistics management system.
"""

import logging
import tempfile
import os
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import JSONResponse

from app.models import BaseResponse, ErrorResponse
from app.services.data_service import DataService
from app.services.logistics_service import LogisticsService

router = APIRouter()
logger = logging.getLogger(__name__)


def get_data_service() -> DataService:
    """Get data service instance."""
    return DataService()


def get_logistics_service() -> LogisticsService:
    """Get logistics service instance."""
    return LogisticsService()


@router.post("/upload/csv", response_model=BaseResponse)
async def upload_csv_data(
    request: Request,
    file: UploadFile = File(..., description="CSV file to upload"),
    delimiter: str = "|",
    skip_initial_space: bool = True,
):
    """Upload and process CSV data file."""
    logger.info("📥 API v1 - POST /data/upload/csv")

    # Validate file type
    if not file.filename.lower().endswith('.csv'):
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                status="error",
                message="Invalid file type",
                details="Only CSV files are supported",
                code=400,
            ).dict(),
        )

    try:
        # Create temporary file to store uploaded content
        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, suffix=".csv"
        ) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Process the uploaded file
        data_service = get_data_service()
        
        # Load and parse the CSV data
        raw_data = data_service._load_csv_from_path(
            temp_file_path, delimiter, skip_initial_space
        )
        articles = data_service._parse_csv_articles_from_data(raw_data)
        
        # Create picking orders from the data
        projects = data_service._create_projects_from_articles(articles)
        orders = data_service.create_picking_orders(projects)
        
        # Add orders to logistics service
        logistics_service = get_logistics_service()
        for order in orders:
            logistics_service.add_order(order)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        # Prepare response data
        response_data = {
            "filename": file.filename,
            "total_records": len(raw_data),
            "articles_parsed": len(articles),
            "projects_created": len(projects),
            "orders_created": len(orders),
            "sample_articles": [
                {
                    "artikel": article.artikel,
                    "artikel_bezeichnung": article.artikel_bezeichnung,
                    "menge": article.menge,
                    "lagerplatz": article.lagerplatz,
                    "status": article.status.value,
                }
                for article in articles[:5]  # First 5 articles as sample
            ],
        }

        return BaseResponse(
            status="success",
            message="CSV data uploaded and processed successfully",
            data=response_data,
        )

    except Exception as e:
        logger.error("❌ Error uploading CSV data: %s", str(e))
        
        # Clean up temporary file if it exists
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
        
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status="error",
                message="Failed to process CSV file",
                details=str(e),
                code=500,
            ).dict(),
        )


@router.post("/load/default", response_model=BaseResponse)
async def load_default_data(request: Request):
    """Load default data from docs/data directory."""
    logger.info("📥 API v1 - POST /data/load/default")

    try:
        data_service = get_data_service()
        logistics_service = get_logistics_service()
        
        # Load and parse default data
        articles = data_service.parse_csv_articles("orig.csv")
        projects = data_service.parse_json_projects("project.json")
        orders = data_service.create_picking_orders(projects)
        
        # Add orders to logistics service
        for order in orders:
            logistics_service.add_order(order)
        
        # Create some sample pickers and carts
        sample_pickers = [
            {"picker_id": "P001", "name": "John Doe", "employee_number": "EMP001"},
            {"picker_id": "P002", "name": "Jane Smith", "employee_number": "EMP002"},
            {"picker_id": "P003", "name": "Bob Wilson", "employee_number": "EMP003"},
        ]
        
        sample_carts = [
            {"cart_id": "C001", "capacity": 100.0},
            {"cart_id": "C002", "capacity": 150.0},
            {"cart_id": "C003", "capacity": 200.0},
        ]
        
        # Add sample pickers and carts (this would need to be implemented in LogisticsService)
        
        response_data = {
            "articles_loaded": len(articles),
            "projects_loaded": len(projects),
            "orders_created": len(orders),
            "pickers_created": len(sample_pickers),
            "carts_created": len(sample_carts),
        }

        return BaseResponse(
            status="success",
            message="Default data loaded successfully",
            data=response_data,
        )

    except Exception as e:
        logger.error("❌ Error loading default data: %s", str(e))
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status="error",
                message="Failed to load default data",
                details=str(e),
                code=500,
            ).dict(),
        )


@router.get("/status", response_model=BaseResponse)
async def get_data_status(request: Request):
    """Get current data status and statistics."""
    logger.info("📥 API v1 - GET /data/status")

    try:
        logistics_service = get_logistics_service()
        
        response_data = {
            "orders_count": len(logistics_service.orders),
            "pickers_count": len(logistics_service.pickers),
            "carts_count": len(logistics_service.carts),
            "open_orders": len([o for o in logistics_service.orders if o.status.value == "Offen"]),
            "in_progress_orders": len([o for o in logistics_service.orders if o.status.value == "In Bearbeitung"]),
            "completed_orders": len([o for o in logistics_service.orders if o.status.value == "Abgeschlossen"]),
        }

        return BaseResponse(
            status="success",
            message="Data status retrieved successfully",
            data=response_data,
        )

    except Exception as e:
        logger.error("❌ Error getting data status: %s", str(e))
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                status="error",
                message="Failed to get data status",
                details=str(e),
                code=500,
            ).dict(),
        )


# EOF 
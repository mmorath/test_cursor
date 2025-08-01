# Backend API v1 Routes Documentation

## Overview

This document describes the REST API endpoints for the Logistics Management System backend. The API follows RESTful conventions and provides comprehensive functionality for managing picking orders, pickers, material carts, and system statistics.

**Base URL**: `/api/v1`

**Content-Type**: `application/json`

## Authentication

Currently, the API does not require authentication. In a production environment, this should be implemented using JWT tokens or API keys.

## Response Format

All API responses follow a standardized format:

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "details": "Detailed error information",
  "code": 400
}
```

## API Endpoints

### 1. Orders Management (`/orders`)

The orders endpoints handle picking order lifecycle management, from creation to completion.

#### GET `/orders`
Retrieve all orders with optional filtering and pagination.

**Query Parameters:**
- `status_filter` (optional): Filter orders by status (`OFFEN`, `IN_BEARBEITUNG`, `ABGESCHLOSSEN`)
- `page` (default: 1): Page number for pagination
- `size` (default: 10, max: 100): Number of items per page

**Response:**
```json
{
  "status": "success",
  "message": "Orders retrieved successfully",
  "data": {
    "orders": [
      {
        "order_id": "ORD001",
        "project_number": "054536",
        "status": "OFFEN",
        "priority": "HIGH",
        "assigned_picker": "P001",
        "created_at": "2024-01-15T10:30:00Z",
        "completion_percentage": 75.0,
        "total_articles": 10,
        "completed_articles": 7,
        "total_weight": 150.5,
        "is_complete": false
      }
    ],
    "pagination": {
      "page": 1,
      "size": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

#### GET `/orders/{order_id}`
Retrieve a specific order by ID.

**Path Parameters:**
- `order_id`: Unique identifier of the order

**Response:**
```json
{
  "status": "success",
  "message": "Order retrieved successfully",
  "data": {
    "order_id": "ORD001",
    "project_number": "054536",
    "status": "OFFEN",
    "priority": "HIGH",
    "assigned_picker": "P001",
    "created_at": "2024-01-15T10:30:00Z",
    "completion_percentage": 75.0,
    "total_articles": 10,
    "completed_articles": 7,
    "total_weight": 150.5,
    "is_complete": false
  }
}
```

#### POST `/orders/{order_id}/assign`
Assign an order to a picker.

**Path Parameters:**
- `order_id`: Unique identifier of the order

**Query Parameters:**
- `picker_id`: ID of the picker to assign the order to

**Response:**
```json
{
  "status": "success",
  "message": "Order ORD001 assigned to picker P001",
  "data": {
    "order_id": "ORD001",
    "picker_id": "P001"
  }
}
```

#### POST `/orders/{order_id}/pick`
Record the picking of an article within an order.

**Path Parameters:**
- `order_id`: Unique identifier of the order

**Query Parameters:**
- `article_id`: ID of the article being picked
- `quantity`: Quantity of the article being picked
- `picker_id`: ID of the picker performing the action

**Response:**
```json
{
  "status": "success",
  "message": "Picked 5 of article ART001",
  "data": {
    "order_id": "ORD001",
    "article_id": "ART001",
    "quantity": 5,
    "picker_id": "P001"
  }
}
```

#### POST `/orders/{order_id}/complete`
Mark an order as completed.

**Path Parameters:**
- `order_id`: Unique identifier of the order

**Response:**
```json
{
  "status": "success",
  "message": "Order ORD001 completed",
  "data": {
    "order_id": "ORD001"
  }
}
```

### 2. Pickers Management (`/pickers`)

The pickers endpoints manage warehouse personnel who perform picking operations.

#### GET `/pickers`
Retrieve all pickers in the system.

**Response:**
```json
{
  "status": "success",
  "message": "Pickers retrieved successfully",
  "data": {
    "pickers": [
      {
        "picker_id": "P001",
        "name": "John Doe",
        "employee_number": "EMP001",
        "is_active": true,
        "current_order": "ORD001"
      }
    ]
  }
}
```

#### POST `/pickers`
Create a new picker.

**Request Body:**
```json
{
  "name": "Jane Smith",
  "employee_number": "EMP002"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Picker created successfully",
  "data": {
    "picker_id": "P002"
  }
}
```

### 3. Carts Management (`/carts`)

The carts endpoints manage material carts used for collecting picked items.

#### GET `/carts`
Retrieve all material carts.

**Response:**
```json
{
  "status": "success",
  "message": "Carts retrieved successfully",
  "data": {
    "carts": [
      {
        "cart_id": "C001",
        "capacity": 100.0,
        "current_weight": 45.5,
        "is_available": true,
        "assigned_picker": "P001"
      }
    ]
  }
}
```

#### POST `/carts`
Create a new material cart.

**Request Body:**
```json
{
  "capacity": 150.0
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Cart created successfully",
  "data": {
    "cart_id": "C002"
  }
}
```

### 4. Statistics (`/statistics`)

The statistics endpoints provide system-wide metrics and overview data.

#### GET `/statistics/overview`
Get comprehensive system overview statistics.

**Response:**
```json
{
  "status": "success",
  "message": "System overview retrieved successfully",
  "data": {
    "total_orders": 25,
    "open_orders": 10,
    "completed_orders": 15,
    "total_pickers": 8,
    "active_pickers": 6,
    "total_carts": 12,
    "available_carts": 8,
    "total_articles": 150,
    "picked_articles": 120,
    "system_efficiency": 85.5
  }
}
```

### 5. Data Management (`/data`)

The data endpoints handle data import, loading, and status monitoring.

#### POST `/data/upload/csv`
Upload and process a CSV file (like `orig.csv`).

**Request:**
- `file`: CSV file to upload (multipart/form-data)
- `delimiter` (optional, default: "|"): CSV delimiter
- `skip_initial_space` (optional, default: true): Skip initial spaces

**Response:**
```json
{
  "status": "success",
  "message": "CSV data uploaded and processed successfully",
  "data": {
    "filename": "orig.csv",
    "total_records": 65,
    "articles_parsed": 65,
    "projects_created": 1,
    "orders_created": 1,
    "sample_articles": [
      {
        "artikel": "388303408",
        "artikel_bezeichnung": "SPANNPRATZE GS18NIMOCR36 FLZN",
        "menge": 3,
        "lagerplatz": "23IZ022A",
        "status": "Offen"
      }
    ]
  }
}
```

#### POST `/data/load/default`
Load default data from the `docs/data` directory.

**Response:**
```json
{
  "status": "success",
  "message": "Default data loaded successfully",
  "data": {
    "articles_loaded": 65,
    "projects_loaded": 1,
    "orders_created": 1,
    "pickers_created": 3,
    "carts_created": 3
  }
}
```

#### GET `/data/status`
Get current data status and statistics.

**Response:**
```json
{
  "status": "success",
  "message": "Data status retrieved successfully",
  "data": {
    "orders_count": 1,
    "pickers_count": 3,
    "carts_count": 3,
    "open_orders": 1,
    "in_progress_orders": 0,
    "completed_orders": 0
  }
}
```

## Data Models

### Order Status Enum
- `OFFEN`: Order is open and ready for processing
- `IN_BEARBEITUNG`: Order is currently being processed
- `ABGESCHLOSSEN`: Order has been completed

### Priority Levels
- `LOW`: Low priority orders
- `MEDIUM`: Medium priority orders
- `HIGH`: High priority orders

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting to prevent abuse.

## Logging

All API requests are logged with the following information:
- Request method and path
- Request parameters
- Response status
- Error details (if applicable)

## Testing

The API includes comprehensive test coverage:
- Unit tests for individual endpoints
- Integration tests for complete workflows
- API contract tests

Run tests using:
```bash
cd backend
make test
```

## Development

To run the API locally:

```bash
cd backend
make run-backend
```

The API will be available at `http://localhost:8000/api/v1`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Versioning

This is API version 1. Future versions will maintain backward compatibility or provide migration paths for breaking changes. 
# Logistics Management System

A comprehensive warehouse management and picking system with FastAPI backend and NiceGUI frontend.

## 🏗️ Architecture

This application follows a modern microservices architecture with:

- **Backend**: FastAPI REST API with proper versioning (`/api/v1/`)
- **Frontend**: NiceGUI web interface with real-time updates
- **Communication**: HTTP/JSON API between frontend and backend
- **Data**: CSV and JSON data sources with Pydantic validation

## 📁 Project Structure

```
logistics-system/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/         # API version 1
│   │   │       ├── routes/ # API endpoints
│   │   │       └── models/ # Response models
│   │   ├── models/         # Pydantic data models
│   │   └── services/       # Business logic
│   ├── config.py           # Configuration management
│   ├── main.py            # FastAPI application
│   └── requirements.txt   # Backend dependencies
├── frontend/               # NiceGUI frontend application
│   ├── main.py            # Frontend application
│   ├── config.py          # Frontend configuration
│   └── requirements.txt   # Frontend dependencies
├── docs/
│   └── data/              # Data files
│       ├── orig.csv       # CSV data source
│       └── project.json   # JSON data source
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

This project follows the Python environment specification (`docs/codex/spec.env.python.md`) with dedicated virtual environments for each service and pip-tools for dependency management.

#### Option 1: Automated Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd logistics-system
   ```

2. **Set up backend environment**
   ```bash
   cd backend
   ./setup_venv.sh
   ```

3. **Set up frontend environment**
   ```bash
   cd ../frontend
   ./setup_venv.sh
   ```

#### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd logistics-system
   ```

2. **Set up backend**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install pip-tools
   pip-compile requirements.in
   pip install -r requirements.txt
   ```

3. **Set up frontend**
   ```bash
   cd ../frontend
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install pip-tools
   pip-compile requirements.in
   pip install -r requirements.txt
   ```

#### Dependency Management

- **requirements.in**: Source of truth for dependencies (unpinned)
- **requirements.txt**: Auto-generated with pinned versions
- **Update dependencies**: `make update-requirements`
- **Compile requirements**: `make compile-requirements`

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The API will be available at:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

2. **Start the frontend**
   ```bash
   cd frontend
   source .venv/bin/activate
   python main.py
   ```

   The frontend will be available at:
   - Web Interface: http://localhost:3000

## 📊 Features

### Backend API Features

- **RESTful API** with proper versioning (`/api/v1/`)
- **Standardized responses** with consistent format
- **Data validation** using Pydantic models
- **Error handling** with proper HTTP status codes
- **CORS support** for frontend communication
- **Comprehensive logging** with structured output
- **Health checks** and system monitoring

### Frontend Features

- **Modern UI** with NiceGUI framework
- **Real-time updates** from backend API
- **Responsive design** for different screen sizes
- **Interactive dashboards** with statistics
- **Order management** with filtering and pagination
- **Picker and cart management**
- **Route optimization** visualization

### Core Functionality

- **Order Management**: Create, assign, and track picking orders
- **Picker Management**: Manage warehouse pickers and assignments
- **Cart Management**: Track material carts and utilization
- **Article Picking**: Record picking activities and progress
- **Route Optimization**: Calculate optimal picking routes
- **Statistics & Reporting**: Real-time system overview and metrics

## 🔧 Configuration

### Backend Configuration

The backend uses environment variables and `.env` files:

```bash
# Backend settings
APP_NAME="Logistics Management System"
APP_VERSION="1.0.0"
HOST="0.0.0.0"
PORT=8000
DEBUG=false

# Data settings
DATA_DIR="../docs/data"
CSV_FILE="orig.csv"
JSON_FILE="project.json"

# CORS settings
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend Configuration

```bash
# Frontend settings
APP_NAME="Logistics Management System"
HOST="127.0.0.1"
PORT=3000
DEBUG=true

# API settings
API_BASE_URL="http://localhost:8000"
API_TIMEOUT=30
```

## 📡 API Endpoints

### Orders Management

- `GET /api/v1/orders` - List all orders with pagination
- `GET /api/v1/orders/{order_id}` - Get specific order details
- `POST /api/v1/orders/{order_id}/assign` - Assign order to picker
- `POST /api/v1/orders/{order_id}/pick` - Record article picking
- `POST /api/v1/orders/{order_id}/complete` - Complete order

### Pickers Management

- `GET /api/v1/pickers` - List all pickers
- `POST /api/v1/pickers` - Create new picker
- `PUT /api/v1/pickers/{picker_id}` - Update picker
- `DELETE /api/v1/pickers/{picker_id}` - Deactivate picker

### Carts Management

- `GET /api/v1/carts` - List all carts
- `POST /api/v1/carts` - Create new cart
- `PUT /api/v1/carts/{cart_id}` - Update cart
- `POST /api/v1/carts/{cart_id}/assign` - Assign cart to picker

### Statistics

- `GET /api/v1/statistics/overview` - System overview statistics
- `GET /api/v1/statistics/orders` - Order statistics
- `GET /api/v1/statistics/pickers` - Picker performance statistics

## 🧪 Testing

### Backend Testing

```bash
cd backend
source venv/bin/activate
pytest --cov=app --cov-report=html
```

### Frontend Testing

```bash
cd frontend
source venv/bin/activate
pytest --cov=app --cov-report=html
```

### API Testing

```bash
# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/orders
```

## 📈 Data Flow

1. **Data Loading**: CSV and JSON files are loaded and validated
2. **Order Creation**: Projects are converted to picking orders
3. **Assignment**: Orders are assigned to available pickers
4. **Picking Process**: Articles are picked and recorded
5. **Completion**: Orders are marked as complete
6. **Reporting**: Statistics are calculated and displayed

## 🔒 Security

- **Input validation** using Pydantic models
- **CORS protection** for cross-origin requests
- **Error handling** without exposing sensitive information
- **Logging** for audit trails and debugging

## 🚀 Deployment

### Production Deployment

1. **Backend Deployment**
   ```bash
   # Using Gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

2. **Frontend Deployment**
   ```bash
   # Using production server
   python main.py --host 0.0.0.0 --port 3000
   ```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 📝 Development

### Code Quality

The project follows strict code quality standards:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **Pytest** for testing

### Adding New Features

1. **Backend**: Add models, services, and API endpoints
2. **Frontend**: Add UI components and event handlers
3. **Testing**: Add unit and integration tests
4. **Documentation**: Update API docs and README

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the codex specifications in `docs/codex/`

## 🔄 Version History

- **v1.0.0**: Initial release with basic functionality
- **v1.1.0**: Added route optimization and statistics
- **v1.2.0**: Enhanced UI and real-time updates

---

**Built with ❤️ using FastAPI and NiceGUI**

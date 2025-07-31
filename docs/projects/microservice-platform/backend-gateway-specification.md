# 🌐 API Gateway Specification

---
title: API Gateway
category: microservice
status: active
last_updated: 2024-01-15
---

## 📋 Service Overview

The API Gateway serves as the central entry point for all client requests to the microservice platform. It handles authentication, routing, rate limiting, and provides a unified API interface for frontend applications and external clients.

## 🏗️ Architecture

### Service Responsibilities
- **Request Routing:** Route requests to appropriate microservices
- **Authentication:** Validate JWT tokens and handle authentication
- **Rate Limiting:** Prevent API abuse and ensure fair usage
- **Request/Response Transformation:** Modify requests and responses as needed
- **Logging & Monitoring:** Centralized request logging and metrics
- **CORS Handling:** Cross-origin resource sharing configuration
- **Load Balancing:** Distribute requests across service instances

### Technology Stack
- **Framework:** FastAPI + Kong Gateway
- **Authentication:** JWT token validation
- **Rate Limiting:** Redis-based rate limiting
- **Monitoring:** Prometheus metrics + Grafana dashboards
- **Load Balancing:** Kong load balancer
- **Caching:** Redis for response caching

## 🔌 API Endpoints

### Gateway Configuration

#### GET `/health`
**Purpose:** Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "user-service": "healthy",
    "order-service": "healthy",
    "inventory-service": "healthy"
  }
}
```

#### GET `/metrics`
**Purpose:** Prometheus metrics endpoint

**Response:**
```
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/api/v1/users",status="200"} 1234
http_requests_total{method="POST",endpoint="/api/v1/orders",status="201"} 567
```

### Service Routing

#### User Service Routes
```
/api/v1/users/* → user-service:8001
/api/v1/auth/* → user-service:8001
/api/v1/roles/* → user-service:8001
```

#### Order Service Routes
```
/api/v1/orders/* → order-service:8002
/api/v1/order-items/* → order-service:8002
```

#### Inventory Service Routes
```
/api/v1/inventory/* → inventory-service:8003
/api/v1/products/* → inventory-service:8003
```

#### Payment Service Routes
```
/api/v1/payments/* → payment-service:8004
/api/v1/transactions/* → payment-service:8004
```

#### Notification Service Routes
```
/api/v1/notifications/* → notification-service:8005
/api/v1/email/* → notification-service:8005
```

## 🔐 Security Configuration

### Authentication Middleware
```python
class AuthMiddleware:
    """JWT token validation middleware."""
    
    async def __call__(self, request: Request, call_next):
        # Skip authentication for public endpoints
        if self.is_public_endpoint(request.url.path):
            return await call_next(request)
        
        # Extract and validate JWT token
        token = self.extract_token(request)
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        
        # Validate token with user service
        user = await self.validate_token(token)
        request.state.user = user
        
        return await call_next(request)
```

### Rate Limiting Configuration
```python
class RateLimiter:
    """Redis-based rate limiting."""
    
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.limits = {
            "authenticated": {"requests": 1000, "window": 3600},  # 1000 req/hour
            "unauthenticated": {"requests": 100, "window": 3600},  # 100 req/hour
            "api_key": {"requests": 10000, "window": 3600},  # 10000 req/hour
        }
    
    async def check_rate_limit(self, client_id: str, limit_type: str):
        """Check if request is within rate limits."""
        key = f"rate_limit:{client_id}:{limit_type}"
        limit = self.limits[limit_type]
        
        current = await self.redis.incr(key)
        if current == 1:
            await self.redis.expire(key, limit["window"])
        
        if current > limit["requests"]:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
```

## 📊 Request/Response Transformation

### Request Transformation
```python
class RequestTransformer:
    """Transform incoming requests."""
    
    async def transform_request(self, request: Request):
        # Add correlation ID for tracing
        correlation_id = str(uuid.uuid4())
        request.headers["X-Correlation-ID"] = correlation_id
        
        # Add user context
        if hasattr(request.state, "user"):
            request.headers["X-User-ID"] = str(request.state.user.id)
            request.headers["X-User-Roles"] = ",".join(request.state.user.roles)
        
        # Log request
        await self.log_request(request)
        
        return request
```

### Response Transformation
```python
class ResponseTransformer:
    """Transform outgoing responses."""
    
    async def transform_response(self, response: Response):
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response
```

## 🔄 Load Balancing

### Service Discovery
```python
class ServiceRegistry:
    """Service discovery and health checking."""
    
    def __init__(self):
        self.services = {
            "user-service": ["user-service-1:8001", "user-service-2:8001"],
            "order-service": ["order-service-1:8002", "order-service-2:8002"],
            "inventory-service": ["inventory-service-1:8003", "inventory-service-2:8003"],
        }
        self.health_checks = {}
    
    async def get_healthy_instances(self, service_name: str) -> List[str]:
        """Get healthy service instances."""
        instances = self.services.get(service_name, [])
        healthy_instances = []
        
        for instance in instances:
            if await self.is_healthy(instance):
                healthy_instances.append(instance)
        
        return healthy_instances
    
    async def is_healthy(self, instance: str) -> bool:
        """Check if service instance is healthy."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://{instance}/health", timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False
```

### Load Balancing Strategy
```python
class LoadBalancer:
    """Round-robin load balancer with health checking."""
    
    def __init__(self, service_registry: ServiceRegistry):
        self.registry = service_registry
        self.current_index = {}
    
    async def get_next_instance(self, service_name: str) -> str:
        """Get next healthy service instance."""
        instances = await self.registry.get_healthy_instances(service_name)
        
        if not instances:
            raise HTTPException(status_code=503, detail="Service unavailable")
        
        # Round-robin selection
        if service_name not in self.current_index:
            self.current_index[service_name] = 0
        
        instance = instances[self.current_index[service_name]]
        self.current_index[service_name] = (self.current_index[service_name] + 1) % len(instances)
        
        return instance
```

## 📈 Monitoring & Observability

### Metrics Collection
```python
class MetricsCollector:
    """Collect and expose metrics."""
    
    def __init__(self):
        self.request_counter = Counter(
            "http_requests_total",
            "Total number of HTTP requests",
            ["method", "endpoint", "status", "service"]
        )
        self.request_duration = Histogram(
            "http_request_duration_seconds",
            "HTTP request duration in seconds",
            ["method", "endpoint", "service"]
        )
        self.active_connections = Gauge(
            "http_active_connections",
            "Number of active HTTP connections"
        )
    
    async def record_request(self, method: str, endpoint: str, status: int, service: str, duration: float):
        """Record request metrics."""
        self.request_counter.labels(method=method, endpoint=endpoint, status=status, service=service).inc()
        self.request_duration.labels(method=method, endpoint=endpoint, service=service).observe(duration)
```

### Logging Configuration
```python
class RequestLogger:
    """Structured request logging."""
    
    async def log_request(self, request: Request, response: Response, duration: float):
        """Log request details."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "duration_ms": duration * 1000,
            "user_id": getattr(request.state, "user_id", None),
            "correlation_id": request.headers.get("X-Correlation-ID"),
            "user_agent": request.headers.get("User-Agent"),
            "ip_address": request.client.host,
        }
        
        logger.info("API Gateway Request", extra=log_data)
```

## 🚀 Deployment

### Docker Configuration
```yaml
# docker-compose.yml
api-gateway:
  image: microservice-platform/api-gateway:latest
  environment:
    - REDIS_URL=redis://redis:6379
    - USER_SERVICE_URL=http://user-service:8001
    - ORDER_SERVICE_URL=http://order-service:8002
    - INVENTORY_SERVICE_URL=http://inventory-service:8003
    - PAYMENT_SERVICE_URL=http://payment-service:8004
    - NOTIFICATION_SERVICE_URL=http://notification-service:8005
    - JWT_SECRET=${JWT_SECRET}
    - LOG_LEVEL=INFO
  ports:
    - "8000:8000"
  depends_on:
    - redis
    - user-service
    - order-service
    - inventory-service
    - payment-service
    - notification-service
```

### Kubernetes Configuration
```yaml
# k8s/api-gateway.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: api-gateway
        image: microservice-platform/api-gateway:latest
        ports:
        - containerPort: 8000
        env:
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: api-gateway-secrets
              key: jwt-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
spec:
  selector:
    app: api-gateway
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 🧪 Testing Strategy

### Unit Tests
- **Middleware Testing:** Authentication and rate limiting
- **Routing Testing:** Request routing logic
- **Transformation Testing:** Request/response transformation
- **Load Balancing Testing:** Load balancer algorithms

### Integration Tests
- **Service Communication:** End-to-end service routing
- **Authentication Flow:** Complete authentication process
- **Rate Limiting:** Rate limiting behavior under load
- **Health Checks:** Service health monitoring

### Performance Tests
- **Load Testing:** High-throughput request handling
- **Latency Testing:** Response time under various loads
- **Concurrent Users:** Multiple simultaneous users
- **Failover Testing:** Service failure scenarios

## 📚 Documentation

### API Documentation
- **OpenAPI/Swagger:** Auto-generated API documentation
- **Service Routes:** Complete routing table
- **Authentication:** Authentication flow documentation
- **Rate Limits:** Rate limiting policies

### Operational Documentation
- **Deployment Guide:** Production deployment instructions
- **Monitoring Guide:** Metrics and alerting setup
- **Troubleshooting:** Common issues and solutions
- **Security Guide:** Security configuration and best practices

## 🔗 Dependencies

### Internal Services
- **User Service:** Authentication and user validation
- **All Microservices:** Request routing and load balancing
- **Redis:** Rate limiting and caching
- **Monitoring Stack:** Metrics collection and alerting

### External Services
- **Load Balancer:** External load balancing (if needed)
- **CDN:** Static asset delivery
- **SSL Certificate:** TLS termination and certificate management

---

**The API Gateway provides a secure, scalable, and observable entry point to the microservice platform, ensuring reliable communication between clients and services.** 
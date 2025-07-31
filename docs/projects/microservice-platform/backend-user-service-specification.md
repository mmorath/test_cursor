# 🔐 User Service Specification

---
title: User Service
category: microservice
status: active
last_updated: 2024-01-15
---

## 📋 Service Overview

The User Service is responsible for user management, authentication, and authorization across the microservice platform. It provides centralized user identity management and integrates with other services through APIs and events.

## 🏗️ Architecture

### Service Boundaries
- **User Management:** CRUD operations for user accounts
- **Authentication:** JWT token generation and validation
- **Authorization:** Role-based access control (RBAC)
- **Profile Management:** User preferences and settings
- **Session Management:** User session tracking and management

### Technology Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL (primary), Redis (caching)
- **Authentication:** JWT + OAuth 2.0
- **Message Queue:** RabbitMQ for events
- **Monitoring:** Prometheus + Grafana

## 🔌 API Endpoints

### Authentication Endpoints

#### POST `/auth/login`
**Purpose:** User authentication and token generation

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "remember_me": "boolean"
}
```

**Response:**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "username": "string",
    "email": "string",
    "roles": ["string"],
    "permissions": ["string"]
  }
}
```

#### POST `/auth/refresh`
**Purpose:** Refresh access token using refresh token

**Request Body:**
```json
{
  "refresh_token": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### POST `/auth/logout`
**Purpose:** Invalidate user session

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

### User Management Endpoints

#### GET `/users`
**Purpose:** List users with pagination and filtering

**Query Parameters:**
- `page`: Page number (default: 1)
- `size`: Page size (default: 20, max: 100)
- `search`: Search term for username/email
- `role`: Filter by role
- `status`: Filter by status (active, inactive, suspended)

**Response:**
```json
{
  "users": [
    {
      "id": "uuid",
      "username": "string",
      "email": "string",
      "first_name": "string",
      "last_name": "string",
      "roles": ["string"],
      "status": "string",
      "created_at": "datetime",
      "last_login": "datetime"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 100,
    "pages": 5
  }
}
```

#### POST `/users`
**Purpose:** Create new user account

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "roles": ["string"],
  "send_welcome_email": "boolean"
}
```

**Response:**
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "roles": ["string"],
  "status": "active",
  "created_at": "datetime"
}
```

#### GET `/users/{user_id}`
**Purpose:** Get user details by ID

**Response:**
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "roles": ["string"],
  "permissions": ["string"],
  "status": "string",
  "profile": {
    "avatar_url": "string",
    "phone": "string",
    "timezone": "string",
    "language": "string"
  },
  "created_at": "datetime",
  "updated_at": "datetime",
  "last_login": "datetime"
}
```

#### PUT `/users/{user_id}`
**Purpose:** Update user information

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "roles": ["string"],
  "profile": {
    "phone": "string",
    "timezone": "string",
    "language": "string"
  }
}
```

#### DELETE `/users/{user_id}`
**Purpose:** Deactivate user account

**Response:**
```json
{
  "message": "User deactivated successfully"
}
```

### Role Management Endpoints

#### GET `/roles`
**Purpose:** List all available roles

**Response:**
```json
{
  "roles": [
    {
      "id": "uuid",
      "name": "string",
      "description": "string",
      "permissions": ["string"],
      "created_at": "datetime"
    }
  ]
}
```

#### POST `/roles`
**Purpose:** Create new role

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "permissions": ["string"]
}
```

## 📊 Data Models

### User Model
```python
class User(BaseModel):
    id: UUID
    username: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    roles: List[str]
    status: UserStatus
    profile: UserProfile
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    failed_login_attempts: int
    locked_until: Optional[datetime]
```

### UserProfile Model
```python
class UserProfile(BaseModel):
    avatar_url: Optional[str]
    phone: Optional[str]
    timezone: str = "UTC"
    language: str = "en"
    preferences: Dict[str, Any]
```

### Role Model
```python
class Role(BaseModel):
    id: UUID
    name: str
    description: str
    permissions: List[str]
    created_at: datetime
    updated_at: datetime
```

## 🔄 Event Communication

### Published Events

#### `user.created`
**Triggered when:** New user account is created

**Event Payload:**
```json
{
  "event_type": "user.created",
  "user_id": "uuid",
  "username": "string",
  "email": "string",
  "roles": ["string"],
  "timestamp": "datetime"
}
```

#### `user.updated`
**Triggered when:** User information is updated

**Event Payload:**
```json
{
  "event_type": "user.updated",
  "user_id": "uuid",
  "changes": {
    "email": "string",
    "roles": ["string"],
    "status": "string"
  },
  "timestamp": "datetime"
}
```

#### `user.deactivated`
**Triggered when:** User account is deactivated

**Event Payload:**
```json
{
  "event_type": "user.deactivated",
  "user_id": "uuid",
  "timestamp": "datetime"
}
```

#### `user.login`
**Triggered when:** User successfully logs in

**Event Payload:**
```json
{
  "event_type": "user.login",
  "user_id": "uuid",
  "ip_address": "string",
  "user_agent": "string",
  "timestamp": "datetime"
}
```

### Consumed Events

#### `order.created`
**Purpose:** Update user's order history

**Handler:** `update_user_order_history()`

#### `payment.processed`
**Purpose:** Update user's payment history

**Handler:** `update_user_payment_history()`

## 🔐 Security

### Authentication
- **JWT Tokens:** Access tokens with 1-hour expiration
- **Refresh Tokens:** Long-lived tokens for token renewal
- **Password Policy:** Minimum 8 characters, complexity requirements
- **Rate Limiting:** 5 failed login attempts per 15 minutes
- **Account Lockout:** 30-minute lockout after 5 failed attempts

### Authorization
- **RBAC:** Role-based access control
- **Permission Granularity:** Fine-grained permissions per endpoint
- **Token Validation:** Centralized token validation service
- **Session Management:** Secure session handling

### Data Protection
- **Password Hashing:** bcrypt with salt rounds
- **Data Encryption:** Sensitive data encrypted at rest
- **Audit Logging:** Complete audit trail for all operations
- **Data Masking:** Sensitive data masked in logs

## 📈 Performance & Scalability

### Caching Strategy
- **User Profiles:** Redis cache with 1-hour TTL
- **Role Permissions:** Redis cache with 24-hour TTL
- **Session Data:** Redis cache with session TTL
- **Database Queries:** Query result caching for frequently accessed data

### Database Optimization
- **Indexes:** Optimized indexes on username, email, status
- **Connection Pooling:** PgBouncer for connection management
- **Read Replicas:** Read-only replicas for query distribution
- **Partitioning:** User data partitioned by creation date

### Monitoring Metrics
- **Response Time:** < 100ms for 95% of requests
- **Error Rate:** < 0.1% error rate
- **Throughput:** 1000+ requests per second
- **Database Connections:** < 80% connection pool utilization

## 🚀 Deployment

### Container Configuration
```yaml
# docker-compose.yml
user-service:
  image: microservice-platform/user-service:latest
  environment:
    - DATABASE_URL=postgresql://user:pass@db:5432/users
    - REDIS_URL=redis://redis:6379
    - RABBITMQ_URL=amqp://rabbitmq:5672
    - JWT_SECRET=${JWT_SECRET}
    - LOG_LEVEL=INFO
  ports:
    - "8001:8000"
  depends_on:
    - postgres
    - redis
    - rabbitmq
```

### Kubernetes Deployment
```yaml
# k8s/user-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: microservice-platform/user-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: user-service-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## 🧪 Testing Strategy

### Unit Tests
- **Service Layer:** Business logic testing
- **Repository Layer:** Data access testing
- **Authentication:** JWT token validation testing
- **Authorization:** Permission checking testing

### Integration Tests
- **API Endpoints:** End-to-end API testing
- **Database Integration:** Database operation testing
- **Event Publishing:** Event communication testing
- **External Services:** Third-party service integration

### Performance Tests
- **Load Testing:** 1000+ concurrent users
- **Stress Testing:** System behavior under high load
- **Database Performance:** Query performance testing
- **Memory Usage:** Memory leak detection

## 📚 Documentation

### API Documentation
- **OpenAPI/Swagger:** Auto-generated API documentation
- **Postman Collection:** Pre-configured API requests
- **Code Examples:** SDK examples in multiple languages

### Developer Guides
- **Setup Guide:** Local development environment
- **Deployment Guide:** Production deployment instructions
- **Troubleshooting:** Common issues and solutions
- **Best Practices:** Development guidelines

## 🔗 Dependencies

### Internal Services
- **Notification Service:** Send welcome emails and notifications
- **Audit Service:** Log user actions for compliance
- **Analytics Service:** Track user behavior and metrics

### External Services
- **Email Service:** Send transactional emails
- **SMS Service:** Send verification codes
- **File Storage:** Store user avatars and documents

---

**The User Service provides the foundation for user identity and access management across the microservice platform, ensuring secure and scalable user operations.**
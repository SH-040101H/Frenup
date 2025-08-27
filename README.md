# IR FitMark - Advanced Fitness Tracking & AI Scoring Platform

A production-ready monorepo for a comprehensive fitness tracking platform with AI-powered assessment and scoring capabilities.

## 🏗️ Architecture

### Applications
- **API** - FastAPI backend with SQLModel + Alembic, Uvicorn, Pydantic v2, OpenAPI
- **Web** - Next.js 15 frontend with TypeScript, shadcn/ui, Tailwind, server actions, Zod
- **Admin** - Next.js 15 admin dashboard for uploads, reports, exceptions, QR bulk generation
- **Worker** - Python service for scheduled AI scoring and report generation

### Packages
- **@pkg/shared** - TypeScript shared types, constants, and utilities
- **pyshared** - Python shared rules, configurations, and checks
- **db** - SQLModel models + Alembic migrations for PostgreSQL

### Infrastructure
- **PostgreSQL** - Primary database
- **MinIO** - S3-compatible object storage
- **Keycloak** - Authentication and authorization
- **Redis** - Caching and Celery broker
- **Docker Compose** - Local development environment

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.12+
- pnpm 8+
- uv (Python package manager)
- Docker & Docker Compose

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ir-fitmark
   ```

2. **Install dependencies**
   ```bash
   # Install Node.js dependencies
   pnpm install
   
   # Install Python dependencies
   uv pip install -e packages/pyshared
   uv pip install -e packages/db
   uv pip install -e apps/api
   uv pip install -e apps/worker
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start infrastructure services**
   ```bash
   docker-compose up -d postgres minio keycloak redis
   ```

5. **Run database migrations**
   ```bash
   cd packages/db
   alembic upgrade head
   ```

6. **Start development servers**
   ```bash
   # Terminal 1: API
   cd apps/api
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2: Web
   cd apps/web
   pnpm dev
   
   # Terminal 3: Admin
   cd apps/admin
   pnpm dev
   
   # Terminal 4: Worker
   cd apps/worker
   celery -A app.main worker --loglevel=info
   ```

## 📋 Environment Variables

### Core Configuration
```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ir_fitmark
POSTGRES_DB=ir_fitmark
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# MinIO (S3-compatible storage)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=ir-fitmark

# Keycloak (Authentication)
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=ir-fitmark
KEYCLOAK_CLIENT_ID=ir-fitmark-client
KEYCLOAK_CLIENT_SECRET=your-client-secret

# Security
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production

# AI/ML Services
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Redis
REDIS_URL=redis://localhost:6379
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Application-Specific Variables
```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
API_WORKERS=1

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_KEYCLOAK_URL=http://localhost:8080

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

## 🗄️ Database Setup

### First Migration

1. **Initialize Alembic** (if not already done)
   ```bash
   cd packages/db
   alembic init src/db/migrations
   ```

2. **Create initial migration**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

3. **Apply migration**
   ```bash
   alembic upgrade head
   ```

### Database Schema

The database includes the following main tables:
- `users` - User accounts and profiles
- `workouts` - Workout sessions and exercises
- `exercises` - Exercise library
- `sets` - Individual exercise sets
- `assessments` - Fitness assessments
- `assessment_results` - AI-scored assessment results
- `file_uploads` - File storage metadata
- `qr_codes` - QR code generation and tracking

## 🏃‍♂️ Development Workflow

### Code Quality

The project uses pre-commit hooks for code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Available Scripts

```bash
# Root level (pnpm)
pnpm dev          # Start all development servers
pnpm build        # Build all applications
pnpm lint         # Lint all TypeScript code
pnpm test         # Run all tests
pnpm clean        # Clean build artifacts

# Python applications
uv pip install -e .  # Install in development mode
uv pip install -r requirements-dev.txt  # Install dev dependencies
```

### Testing

```bash
# TypeScript tests
pnpm test

# Python tests
pytest apps/api/tests/
pytest apps/worker/tests/
pytest packages/pyshared/tests/
pytest packages/db/tests/
```

## 🐳 Docker Development

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# Start specific services
docker-compose up -d postgres minio keycloak

# View logs
docker-compose logs -f api

# Stop all services
docker-compose down
```

### Service Ports

- **API**: http://localhost:8000
- **Web**: http://localhost:3000
- **Admin**: http://localhost:3001
- **PostgreSQL**: localhost:5432
- **MinIO**: http://localhost:9000 (API), http://localhost:9001 (Console)
- **Keycloak**: http://localhost:8080
- **Redis**: localhost:6379

## 📦 Package Structure

```
ir-fitmark/
├── apps/
│   ├── api/                 # FastAPI backend
│   ├── web/                 # Next.js frontend
│   ├── admin/               # Next.js admin dashboard
│   └── worker/              # Celery worker service
├── packages/
│   ├── shared/              # TypeScript shared package
│   ├── pyshared/            # Python shared package
│   └── db/                  # Database models and migrations
├── .github/
│   └── workflows/           # GitHub Actions CI/CD
├── docker-compose.yml       # Local development environment
├── package.json             # Root package.json (pnpm workspace)
├── turbo.json              # Turbo build configuration
└── README.md               # This file
```

## 🔧 Configuration

### Turbo Configuration
The monorepo uses Turbo for build orchestration with the following pipeline:
- `build` - Builds all applications and packages
- `dev` - Starts development servers
- `lint` - Runs linting across all packages
- `test` - Runs tests
- `clean` - Cleans build artifacts

### Pre-commit Hooks
- **Python**: black, isort, ruff
- **TypeScript**: eslint, prettier
- **General**: trailing whitespace, file size checks

## 🚀 Deployment

### Production Build

```bash
# Build all applications
pnpm build

# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

### Environment-Specific Configurations

- **Development**: Uses local services and hot reloading
- **Staging**: Uses staging environment variables
- **Production**: Uses production environment with proper security settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style and conventions
- Write tests for new features
- Update documentation as needed
- Use conventional commit messages
- Ensure all CI checks pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in each package
- Review the API documentation at http://localhost:8000/docs

## 🔗 Links

- **API Documentation**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:3001
- **MinIO Console**: http://localhost:9001
- **Keycloak Admin**: http://localhost:8080

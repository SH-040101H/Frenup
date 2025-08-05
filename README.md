# Authentication App

A complete authentication system built with React frontend and Express.js backend, featuring user registration, login, logout, and protected routes.

## Features

- ✅ User registration with email and password
- ✅ Secure password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ Protected routes and middleware
- ✅ Form validation on frontend and backend
- ✅ Persistent login state
- ✅ Responsive design
- ✅ MongoDB database integration

## Tech Stack

### Backend
- **Express.js** - Web framework
- **MongoDB** with **Mongoose** - Database
- **bcryptjs** - Password hashing
- **jsonwebtoken** - JWT token generation
- **express-validator** - Input validation
- **cors** - Cross-origin resource sharing

### Frontend
- **React** - Frontend framework
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client
- **Context API** - State management

## Project Structure

```
/
├── backend/
│   ├── config/
│   │   └── database.js
│   ├── middleware/
│   │   └── auth.js
│   ├── models/
│   │   └── User.js
│   ├── routes/
│   │   └── auth.js
│   ├── .env
│   ├── package.json
│   └── server.js
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.js
    │   │   ├── Home.js
    │   │   ├── LoginForm.js
    │   │   ├── Navbar.js
    │   │   ├── ProtectedRoute.js
    │   │   └── SignupForm.js
    │   ├── contexts/
    │   │   └── AuthContext.js
    │   ├── App.js
    │   ├── index.js
    │   └── index.css
    └── package.json
```

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- MongoDB (local installation or MongoDB Atlas)
- npm or yarn

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd auth-app

# Install backend dependencies
cd backend
npm install

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Environment Configuration

Create a `.env` file in the backend directory:

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/auth_app
JWT_SECRET=your_jwt_secret_key_change_this_in_production
NODE_ENV=development
```

**Important:** Change the `JWT_SECRET` to a secure random string in production.

### 3. Database Setup

Make sure MongoDB is running on your system:

```bash
# If using local MongoDB
mongod

# Or use MongoDB Atlas cloud service
# Update MONGODB_URI in .env with your Atlas connection string
```

### 4. Running the Application

#### Start the Backend Server

```bash
cd backend
npm run dev  # Development mode with nodemon
# or
npm start    # Production mode
```

The backend server will run on `http://localhost:5000`

#### Start the Frontend Development Server

```bash
cd frontend
npm start
```

The frontend will run on `http://localhost:3000`

## API Endpoints

### Authentication Routes

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| POST | `/api/auth/signup` | Register new user | Public |
| POST | `/api/auth/login` | Login user | Public |
| POST | `/api/auth/logout` | Logout user | Private |
| GET | `/api/auth/me` | Get current user | Private |

### Request/Response Examples

#### Signup
```bash
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Protected Routes
```bash
GET /api/auth/me
Authorization: Bearer <jwt_token>
```

## Frontend Routes

| Route | Component | Description | Protection |
|-------|-----------|-------------|------------|
| `/` | Home | Landing page | Public |
| `/login` | LoginForm | User login | Public |
| `/signup` | SignupForm | User registration | Public |
| `/dashboard` | Dashboard | User dashboard | Protected |

## Usage

1. **Register**: Visit `/signup` to create a new account
2. **Login**: Visit `/login` to authenticate
3. **Dashboard**: Access `/dashboard` (redirects to login if not authenticated)
4. **Logout**: Click logout button in navigation

## Security Features

- **Password Hashing**: Uses bcryptjs with salt rounds
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Server-side validation with express-validator
- **Protected Routes**: Middleware-based route protection
- **CORS Configuration**: Proper cross-origin setup
- **Error Handling**: Comprehensive error responses

## Development

### Backend Development
```bash
cd backend
npm run dev  # Uses nodemon for auto-restart
```

### Frontend Development
```bash
cd frontend
npm start  # React development server with hot reload
```

## Production Deployment

### Backend
1. Set `NODE_ENV=production` in environment
2. Use a secure `JWT_SECRET`
3. Configure MongoDB Atlas or production database
4. Set up proper CORS origins

### Frontend
```bash
cd frontend
npm run build  # Creates optimized production build
```

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running
   - Check connection string in `.env`

2. **JWT Token Issues**
   - Verify `JWT_SECRET` is set
   - Check token format in Authorization header

3. **CORS Errors**
   - Verify frontend URL in CORS configuration
   - Check proxy setting in frontend package.json

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 

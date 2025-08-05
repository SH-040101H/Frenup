# Frenup - Full-Stack Social Platform

A modern full-stack web application built with React and Node.js that enables users to connect, share, and engage with their network.

## 🚀 Features

- **Beautiful UI**: Modern, responsive design with Tailwind CSS
- **Real-time Interactions**: Create and share posts instantly
- **User Management**: Profile creation and management
- **Dashboard**: Comprehensive user dashboard with statistics
- **RESTful API**: Well-structured backend API with Express.js
- **Cross-platform**: Works on desktop and mobile devices

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client for API calls

### Backend
- **Node.js** - JavaScript runtime
- **Express.js** - Web application framework
- **CORS** - Cross-origin resource sharing
- **Helmet** - Security middleware
- **Morgan** - HTTP request logger
- **Rate Limiting** - API protection

## 📁 Project Structure

```
frenup/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # Utility functions
│   │   ├── App.jsx          # Main App component
│   │   └── main.jsx         # Entry point
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── backend/                 # Node.js backend API
│   ├── routes/              # API route handlers
│   ├── middleware/          # Custom middleware
│   ├── models/              # Data models (for future DB integration)
│   ├── config/              # Configuration files
│   ├── server.js            # Main server file
│   └── package.json         # Backend dependencies
└── package.json             # Root workspace configuration
```

## 🚦 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Clone the repository** (or you're already in the project directory)
   ```bash
   git clone <repository-url>
   cd frenup
   ```

2. **Install dependencies for all packages**
   ```bash
   npm run install:all
   ```

3. **Start the development servers**
   ```bash
   npm run dev
   ```

This will start both the frontend (http://localhost:3000) and backend (http://localhost:5000) servers concurrently.

### Individual Server Commands

- **Frontend only**: `npm run frontend:dev`
- **Backend only**: `npm run backend:dev`
- **Build frontend**: `npm run frontend:build`

## 🔗 API Endpoints

### Posts
- `GET /api/posts` - Get all posts
- `POST /api/posts` - Create a new post
- `GET /api/posts/:id` - Get a specific post
- `PUT /api/posts/:id/like` - Like a post
- `DELETE /api/posts/:id` - Delete a post

### Users
- `GET /api/users` - Get all users
- `GET /api/users/:id` - Get user by ID
- `GET /api/users/username/:username` - Get user by username
- `POST /api/users` - Create a new user
- `PUT /api/users/:id` - Update user profile

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user

### Health Check
- `GET /api/health` - API health status

## 🎨 Design System

The application uses a consistent design system with:
- **Primary Color**: Blue (#0ea5e9)
- **Typography**: Inter font family
- **Spacing**: Tailwind's standard spacing scale
- **Components**: Reusable button and card styles

## 📱 Pages

- **Home** (`/`) - Landing page with hero section and features
- **About** (`/about`) - Company information and values
- **Dashboard** (`/dashboard`) - User dashboard with posts and statistics
- **Contact** (`/contact`) - Contact form and information

## 🔮 Future Enhancements

- Database integration (MongoDB/PostgreSQL)
- User authentication with JWT
- Real-time messaging with WebSockets
- Image upload and management
- Advanced user profiles
- Search and filtering
- Mobile app with React Native

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the API health endpoint: http://localhost:5000/api/health
2. Review the console logs in both frontend and backend
3. Ensure all dependencies are installed correctly

---

**Happy coding! 🎉** 

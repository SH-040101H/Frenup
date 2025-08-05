const express = require('express')
const router = express.Router()

// @route   POST /api/auth/login
// @desc    Login user
// @access  Public
router.post('/login', (req, res) => {
  try {
    const { email, password } = req.body

    // Validation
    if (!email || !password) {
      return res.status(400).json({
        success: false,
        message: 'Email and password are required'
      })
    }

    // In a real app, you would validate against database and hash passwords
    // This is just a demo response
    if (email === 'demo@frenup.com' && password === 'demo123') {
      res.json({
        success: true,
        message: 'Login successful',
        data: {
          user: {
            id: 1,
            email: 'demo@frenup.com',
            name: 'Demo User',
            username: 'demouser'
          },
          token: 'demo-jwt-token-12345'
        }
      })
    } else {
      res.status(401).json({
        success: false,
        message: 'Invalid credentials'
      })
    }
  } catch (error) {
    console.error('Error during login:', error)
    res.status(500).json({
      success: false,
      message: 'Login failed'
    })
  }
})

// @route   POST /api/auth/register
// @desc    Register new user
// @access  Public
router.post('/register', (req, res) => {
  try {
    const { email, password, name, username } = req.body

    // Validation
    if (!email || !password || !name || !username) {
      return res.status(400).json({
        success: false,
        message: 'All fields are required'
      })
    }

    if (password.length < 6) {
      return res.status(400).json({
        success: false,
        message: 'Password must be at least 6 characters'
      })
    }

    // In a real app, you would hash the password and save to database
    // This is just a demo response
    res.status(201).json({
      success: true,
      message: 'Registration successful',
      data: {
        user: {
          id: Date.now(),
          email: email,
          name: name,
          username: username
        },
        token: 'demo-jwt-token-' + Date.now()
      }
    })
  } catch (error) {
    console.error('Error during registration:', error)
    res.status(500).json({
      success: false,
      message: 'Registration failed'
    })
  }
})

// @route   GET /api/auth/me
// @desc    Get current user
// @access  Private (requires token)
router.get('/me', (req, res) => {
  try {
    // In a real app, you would verify the JWT token
    // This is just a demo response
    res.json({
      success: true,
      data: {
        id: 1,
        email: 'demo@frenup.com',
        name: 'Demo User',
        username: 'demouser'
      }
    })
  } catch (error) {
    console.error('Error fetching user:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to fetch user'
    })
  }
})

module.exports = router
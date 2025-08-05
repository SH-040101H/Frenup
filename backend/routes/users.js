const express = require('express')
const router = express.Router()

// Sample users data (in a real app, this would come from a database)
let users = [
  {
    id: 1,
    username: 'johndoe',
    email: 'john@example.com',
    name: 'John Doe',
    avatar: null,
    bio: 'Software developer passionate about creating amazing user experiences.',
    joinedAt: '2024-01-15',
    stats: {
      posts: 15,
      followers: 127,
      following: 89
    }
  },
  {
    id: 2,
    username: 'janesmith',
    email: 'jane@example.com',
    name: 'Jane Smith',
    avatar: null,
    bio: 'Designer and entrepreneur. Love creating beautiful interfaces.',
    joinedAt: '2024-02-10',
    stats: {
      posts: 23,
      followers: 256,
      following: 134
    }
  },
  {
    id: 3,
    username: 'mikejohnson',
    email: 'mike@example.com',
    name: 'Mike Johnson',
    avatar: null,
    bio: 'Tech enthusiast and community builder.',
    joinedAt: '2024-03-05',
    stats: {
      posts: 8,
      followers: 67,
      following: 92
    }
  }
]

// @route   GET /api/users
// @desc    Get all users
// @access  Public
router.get('/', (req, res) => {
  try {
    // Remove sensitive information
    const publicUsers = users.map(user => ({
      id: user.id,
      username: user.username,
      name: user.name,
      avatar: user.avatar,
      bio: user.bio,
      joinedAt: user.joinedAt,
      stats: user.stats
    }))

    res.json({
      success: true,
      count: publicUsers.length,
      data: publicUsers
    })
  } catch (error) {
    console.error('Error fetching users:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to fetch users'
    })
  }
})

// @route   GET /api/users/:id
// @desc    Get user by ID
// @access  Public
router.get('/:id', (req, res) => {
  try {
    const userId = parseInt(req.params.id)
    const user = users.find(u => u.id === userId)

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    // Remove sensitive information
    const publicUser = {
      id: user.id,
      username: user.username,
      name: user.name,
      avatar: user.avatar,
      bio: user.bio,
      joinedAt: user.joinedAt,
      stats: user.stats
    }

    res.json({
      success: true,
      data: publicUser
    })
  } catch (error) {
    console.error('Error fetching user:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to fetch user'
    })
  }
})

// @route   GET /api/users/username/:username
// @desc    Get user by username
// @access  Public
router.get('/username/:username', (req, res) => {
  try {
    const username = req.params.username.toLowerCase()
    const user = users.find(u => u.username.toLowerCase() === username)

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    // Remove sensitive information
    const publicUser = {
      id: user.id,
      username: user.username,
      name: user.name,
      avatar: user.avatar,
      bio: user.bio,
      joinedAt: user.joinedAt,
      stats: user.stats
    }

    res.json({
      success: true,
      data: publicUser
    })
  } catch (error) {
    console.error('Error fetching user:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to fetch user'
    })
  }
})

// @route   POST /api/users
// @desc    Create new user
// @access  Public
router.post('/', (req, res) => {
  try {
    const { username, email, name, bio = '' } = req.body

    // Validation
    if (!username || !email || !name) {
      return res.status(400).json({
        success: false,
        message: 'Username, email, and name are required'
      })
    }

    // Check if username already exists
    const existingUsername = users.find(u => u.username.toLowerCase() === username.toLowerCase())
    if (existingUsername) {
      return res.status(400).json({
        success: false,
        message: 'Username already exists'
      })
    }

    // Check if email already exists
    const existingEmail = users.find(u => u.email.toLowerCase() === email.toLowerCase())
    if (existingEmail) {
      return res.status(400).json({
        success: false,
        message: 'Email already exists'
      })
    }

    // Create new user
    const newUser = {
      id: users.length + 1,
      username: username.trim().toLowerCase(),
      email: email.trim().toLowerCase(),
      name: name.trim(),
      avatar: null,
      bio: bio.trim(),
      joinedAt: new Date().toISOString().split('T')[0],
      stats: {
        posts: 0,
        followers: 0,
        following: 0
      }
    }

    users.push(newUser)

    // Return user without sensitive information
    const publicUser = {
      id: newUser.id,
      username: newUser.username,
      name: newUser.name,
      avatar: newUser.avatar,
      bio: newUser.bio,
      joinedAt: newUser.joinedAt,
      stats: newUser.stats
    }

    res.status(201).json({
      success: true,
      message: 'User created successfully',
      data: publicUser
    })
  } catch (error) {
    console.error('Error creating user:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to create user'
    })
  }
})

// @route   PUT /api/users/:id
// @desc    Update user profile
// @access  Public (in real app, this would require authentication)
router.put('/:id', (req, res) => {
  try {
    const userId = parseInt(req.params.id)
    const userIndex = users.findIndex(u => u.id === userId)

    if (userIndex === -1) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    const { name, bio } = req.body
    const user = users[userIndex]

    // Update only provided fields
    if (name) user.name = name.trim()
    if (bio !== undefined) user.bio = bio.trim()

    // Return updated user without sensitive information
    const publicUser = {
      id: user.id,
      username: user.username,
      name: user.name,
      avatar: user.avatar,
      bio: user.bio,
      joinedAt: user.joinedAt,
      stats: user.stats
    }

    res.json({
      success: true,
      message: 'User updated successfully',
      data: publicUser
    })
  } catch (error) {
    console.error('Error updating user:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to update user'
    })
  }
})

module.exports = router
const express = require('express')
const router = express.Router()

// Sample posts data (in a real app, this would come from a database)
let posts = [
  {
    id: 1,
    author: 'John Doe',
    content: 'Welcome to Frenup! This is my first post.',
    likes: 5,
    comments: 2,
    timestamp: '2 hours ago',
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
  },
  {
    id: 2,
    author: 'Jane Smith',
    content: 'Loving the new dashboard interface! So clean and modern.',
    likes: 12,
    comments: 4,
    timestamp: '4 hours ago',
    createdAt: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString()
  },
  {
    id: 3,
    author: 'Mike Johnson',
    content: 'Just connected with some amazing people here. The community is fantastic!',
    likes: 8,
    comments: 1,
    timestamp: '1 day ago',
    createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
  }
]

// @route   GET /api/posts
// @desc    Get all posts
// @access  Public
router.get('/', (req, res) => {
  try {
    // Sort posts by creation date (newest first)
    const sortedPosts = posts.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
    
    res.json({
      success: true,
      count: sortedPosts.length,
      data: sortedPosts
    })
  } catch (error) {
    console.error('Error fetching posts:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to fetch posts'
    })
  }
})

// @route   POST /api/posts
// @desc    Create a new post
// @access  Public (in real app, this would require authentication)
router.post('/', (req, res) => {
  try {
    const { content, author = 'Anonymous User' } = req.body

    // Validation
    if (!content || content.trim().length === 0) {
      return res.status(400).json({
        success: false,
        message: 'Post content is required'
      })
    }

    if (content.length > 500) {
      return res.status(400).json({
        success: false,
        message: 'Post content cannot exceed 500 characters'
      })
    }

    // Create new post
    const newPost = {
      id: posts.length + 1,
      author: author.trim(),
      content: content.trim(),
      likes: 0,
      comments: 0,
      timestamp: 'Just now',
      createdAt: new Date().toISOString()
    }

    posts.unshift(newPost) // Add to beginning of array

    res.status(201).json({
      success: true,
      message: 'Post created successfully',
      data: newPost
    })
  } catch (error) {
    console.error('Error creating post:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to create post'
    })
  }
})

// @route   GET /api/posts/:id
// @desc    Get a single post by ID
// @access  Public
router.get('/:id', (req, res) => {
  try {
    const postId = parseInt(req.params.id)
    const post = posts.find(p => p.id === postId)

    if (!post) {
      return res.status(404).json({
        success: false,
        message: 'Post not found'
      })
    }

    res.json({
      success: true,
      data: post
    })
  } catch (error) {
    console.error('Error fetching post:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to fetch post'
    })
  }
})

// @route   PUT /api/posts/:id/like
// @desc    Like a post
// @access  Public
router.put('/:id/like', (req, res) => {
  try {
    const postId = parseInt(req.params.id)
    const post = posts.find(p => p.id === postId)

    if (!post) {
      return res.status(404).json({
        success: false,
        message: 'Post not found'
      })
    }

    post.likes += 1

    res.json({
      success: true,
      message: 'Post liked successfully',
      data: post
    })
  } catch (error) {
    console.error('Error liking post:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to like post'
    })
  }
})

// @route   DELETE /api/posts/:id
// @desc    Delete a post
// @access  Public (in real app, this would require authentication and authorization)
router.delete('/:id', (req, res) => {
  try {
    const postId = parseInt(req.params.id)
    const postIndex = posts.findIndex(p => p.id === postId)

    if (postIndex === -1) {
      return res.status(404).json({
        success: false,
        message: 'Post not found'
      })
    }

    const deletedPost = posts.splice(postIndex, 1)[0]

    res.json({
      success: true,
      message: 'Post deleted successfully',
      data: deletedPost
    })
  } catch (error) {
    console.error('Error deleting post:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to delete post'
    })
  }
})

module.exports = router
import { useState, useEffect } from 'react'
import { Plus, Users, MessageCircle, Heart, Share2 } from 'lucide-react'
import axios from 'axios'

const Dashboard = () => {
  const [posts, setPosts] = useState([])
  const [newPost, setNewPost] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPosts()
  }, [])

  const fetchPosts = async () => {
    try {
      const response = await axios.get('/api/posts')
      setPosts(response.data)
    } catch (error) {
      console.error('Error fetching posts:', error)
      // Set some demo data for development
      setPosts([
        { id: 1, author: 'John Doe', content: 'Welcome to Frenup! This is my first post.', likes: 5, comments: 2, timestamp: '2 hours ago' },
        { id: 2, author: 'Jane Smith', content: 'Loving the new dashboard interface! So clean and modern.', likes: 12, comments: 4, timestamp: '4 hours ago' },
        { id: 3, author: 'Mike Johnson', content: 'Just connected with some amazing people here. The community is fantastic!', likes: 8, comments: 1, timestamp: '1 day ago' }
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleCreatePost = async () => {
    if (!newPost.trim()) return

    try {
      const response = await axios.post('/api/posts', { content: newPost })
      setPosts([response.data, ...posts])
      setNewPost('')
    } catch (error) {
      console.error('Error creating post:', error)
      // Demo behavior for development
      const demoPost = {
        id: Date.now(),
        author: 'You',
        content: newPost,
        likes: 0,
        comments: 0,
        timestamp: 'Just now'
      }
      setPosts([demoPost, ...posts])
      setNewPost('')
    }
  }

  if (loading) {
    return (
      <div className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded mb-4"></div>
            <div className="h-32 bg-gray-200 rounded mb-8"></div>
            <div className="space-y-4">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-24 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">Stay connected with your network</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Users className="h-8 w-8 text-primary-500" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">127</div>
                <div className="text-gray-600">Friends</div>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <MessageCircle className="h-8 w-8 text-primary-500" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">1.2K</div>
                <div className="text-gray-600">Messages</div>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Heart className="h-8 w-8 text-primary-500" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">89</div>
                <div className="text-gray-600">Likes Received</div>
              </div>
            </div>
          </div>
        </div>

        {/* Create Post */}
        <div className="card mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">What's on your mind?</h2>
          <div className="space-y-4">
            <textarea
              value={newPost}
              onChange={(e) => setNewPost(e.target.value)}
              placeholder="Share your thoughts..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              rows="3"
            />
            <div className="flex justify-end">
              <button
                onClick={handleCreatePost}
                disabled={!newPost.trim()}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center"
              >
                <Plus className="h-4 w-4 mr-2" />
                Post
              </button>
            </div>
          </div>
        </div>

        {/* Posts Feed */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold text-gray-900">Recent Posts</h2>
          {posts.map((post) => (
            <div key={post.id} className="card">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 bg-primary-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium">
                      {post.author.charAt(0).toUpperCase()}
                    </span>
                  </div>
                </div>
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="font-medium text-gray-900">{post.author}</h3>
                    <span className="text-gray-500 text-sm">{post.timestamp}</span>
                  </div>
                  <p className="text-gray-700 mb-4">{post.content}</p>
                  <div className="flex items-center space-x-6 text-gray-500">
                    <button className="flex items-center space-x-1 hover:text-red-500 transition-colors">
                      <Heart className="h-4 w-4" />
                      <span>{post.likes}</span>
                    </button>
                    <button className="flex items-center space-x-1 hover:text-blue-500 transition-colors">
                      <MessageCircle className="h-4 w-4" />
                      <span>{post.comments}</span>
                    </button>
                    <button className="flex items-center space-x-1 hover:text-green-500 transition-colors">
                      <Share2 className="h-4 w-4" />
                      <span>Share</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
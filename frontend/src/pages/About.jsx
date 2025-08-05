import { Target, Heart, Zap } from 'lucide-react'

const About = () => {
  const values = [
    {
      icon: <Target className="h-8 w-8 text-primary-500" />,
      title: "Innovation",
      description: "We constantly push the boundaries of what's possible in social networking."
    },
    {
      icon: <Heart className="h-8 w-8 text-primary-500" />,
      title: "Community",
      description: "Building meaningful connections and fostering genuine relationships."
    },
    {
      icon: <Zap className="h-8 w-8 text-primary-500" />,
      title: "Performance",
      description: "Lightning-fast, reliable platform that works when you need it most."
    }
  ]

  return (
    <div className="py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            About Frenup
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            We're on a mission to revolutionize how people connect and share experiences 
            in the digital age.
          </p>
        </div>

        {/* Story Section */}
        <div className="grid lg:grid-cols-2 gap-12 items-center mb-20">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Story</h2>
            <p className="text-gray-600 mb-4">
              Founded in 2024, Frenup emerged from a simple idea: social networking should be 
              intuitive, meaningful, and focused on genuine human connections. We believe that 
              technology should bring people together, not drive them apart.
            </p>
            <p className="text-gray-600 mb-4">
              Our team of passionate developers and designers work tirelessly to create an 
              experience that feels natural and engaging. We're not just building a platform; 
              we're crafting the future of digital relationships.
            </p>
            <p className="text-gray-600">
              Today, Frenup serves thousands of users worldwide, helping them connect, share, 
              and grow their networks in ways that matter.
            </p>
          </div>
          <div className="bg-gradient-to-br from-primary-100 to-primary-50 rounded-2xl p-8 text-center">
            <div className="text-6xl font-bold text-primary-500 mb-2">2024</div>
            <div className="text-gray-600 mb-4">Year Founded</div>
            <div className="text-4xl font-bold text-primary-500 mb-2">10K+</div>
            <div className="text-gray-600 mb-4">Happy Users</div>
            <div className="text-4xl font-bold text-primary-500 mb-2">24/7</div>
            <div className="text-gray-600">Support Available</div>
          </div>
        </div>

        {/* Values Section */}
        <div className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Values</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              The principles that guide everything we do and every decision we make.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {values.map((value, index) => (
              <div key={index} className="card text-center">
                <div className="flex justify-center mb-4">
                  {value.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {value.title}
                </h3>
                <p className="text-gray-600">
                  {value.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Mission Section */}
        <div className="bg-primary-50 rounded-2xl p-8 md:p-12 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Mission</h2>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto">
            To create a social platform that prioritizes authentic connections, meaningful 
            conversations, and positive interactions. We're building a space where people 
            can truly be themselves and form lasting relationships.
          </p>
        </div>
      </div>
    </div>
  )
}

export default About
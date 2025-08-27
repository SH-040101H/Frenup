import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Activity, 
  BarChart3, 
  QrCode, 
  Shield, 
  Zap, 
  Target,
  Users,
  Trophy,
  ArrowRight
} from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm dark:bg-gray-900/80">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Activity className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                IR FitMark
              </h1>
              <Badge variant="secondary">SIH 2024</Badge>
            </div>
            <nav className="hidden md:flex items-center space-x-6">
              <Link href="/login" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                Login
              </Link>
              <Link href="/register">
                <Button>Get Started</Button>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-5xl font-bold text-gray-900 dark:text-white mb-6">
              AI-Powered Fitness
              <span className="text-blue-600"> Assessment</span> Platform
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
              Revolutionary fitness assessment using computer vision and machine learning. 
              Get real-time feedback, detailed reports, and personalized recommendations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/register">
                <Button size="lg" className="w-full sm:w-auto">
                  Start Your Assessment
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/demo">
                <Button variant="outline" size="lg" className="w-full sm:w-auto">
                  Watch Demo
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Cutting-Edge Features
            </h3>
            <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Built for the Smart India Hackathon with production-ready architecture
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="border-2 hover:border-blue-200 transition-colors">
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4">
                  <Zap className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
                <CardTitle>Real-time AI Analysis</CardTitle>
                <CardDescription>
                  Computer vision powered assessment with instant feedback and scoring
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="text-sm text-gray-600 dark:text-gray-300 space-y-2">
                  <li>• Push-up form analysis</li>
                  <li>• Sit-up counting</li>
                  <li>• Running gait analysis</li>
                  <li>• Flexibility measurement</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-200 transition-colors">
              <CardHeader>
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mb-4">
                  <BarChart3 className="h-6 w-6 text-green-600 dark:text-green-400" />
                </div>
                <CardTitle>Detailed Reports</CardTitle>
                <CardDescription>
                  Comprehensive analytics and progress tracking with PDF generation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="text-sm text-gray-600 dark:text-gray-300 space-y-2">
                  <li>• Weekly/Monthly reports</li>
                  <li>• Progress visualization</li>
                  <li>• Performance trends</li>
                  <li>• Downloadable PDFs</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-200 transition-colors">
              <CardHeader>
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center mb-4">
                  <QrCode className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                </div>
                <CardTitle>QR Code System</CardTitle>
                <CardDescription>
                  Seamless assessment initiation with QR code scanning
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="text-sm text-gray-600 dark:text-gray-300 space-y-2">
                  <li>• Bulk QR generation</li>
                  <li>• Secure authentication</li>
                  <li>• Usage tracking</li>
                  <li>• Expiration management</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-200 transition-colors">
              <CardHeader>
                <div className="w-12 h-12 bg-red-100 dark:bg-red-900 rounded-lg flex items-center justify-center mb-4">
                  <Shield className="h-6 w-6 text-red-600 dark:text-red-400" />
                </div>
                <CardTitle>Enterprise Security</CardTitle>
                <CardDescription>
                  Production-grade security with Keycloak authentication
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="text-sm text-gray-600 dark:text-gray-300 space-y-2">
                  <li>• JWT authentication</li>
                  <li>• Role-based access</li>
                  <li>• Secure file storage</li>
                  <li>• Audit logging</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-200 transition-colors">
              <CardHeader>
                <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900 rounded-lg flex items-center justify-center mb-4">
                  <Users className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
                </div>
                <CardTitle>Multi-Role Support</CardTitle>
                <CardDescription>
                  Designed for students, instructors, and administrators
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="text-sm text-gray-600 dark:text-gray-300 space-y-2">
                  <li>• Student assessments</li>
                  <li>• Instructor monitoring</li>
                  <li>• Admin dashboard</li>
                  <li>• Bulk operations</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-200 transition-colors">
              <CardHeader>
                <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900 rounded-lg flex items-center justify-center mb-4">
                  <Target className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
                </div>
                <CardTitle>Personalized Goals</CardTitle>
                <CardDescription>
                  AI-driven recommendations and goal setting
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="text-sm text-gray-600 dark:text-gray-300 space-y-2">
                  <li>• Smart recommendations</li>
                  <li>• Progress tracking</li>
                  <li>• Achievement badges</li>
                  <li>• Custom workout plans</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Production-Ready Architecture
            </h3>
            <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Built with modern technologies and best practices for scalability and reliability
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Trophy className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              </div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Frontend</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Activity className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Backend</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                FastAPI, SQLModel, Alembic, Uvicorn
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="h-8 w-8 text-purple-600 dark:text-purple-400" />
              </div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Infrastructure</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Docker, PostgreSQL, MinIO, Keycloak
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-red-100 dark:bg-red-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Zap className="h-8 w-8 text-red-600 dark:text-red-400" />
              </div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">DevOps</h4>
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Turbo, pnpm, GitHub Actions, Pre-commit
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600 dark:bg-blue-800">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Ready to Transform Fitness Assessment?
          </h3>
          <p className="text-blue-100 text-lg mb-8 max-w-2xl mx-auto">
            Join the future of AI-powered fitness evaluation. Start your journey today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                Get Started Now
              </Button>
            </Link>
            <Link href="/contact">
              <Button size="lg" variant="outline" className="w-full sm:w-auto border-white text-white hover:bg-white hover:text-blue-600">
                Contact Team
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-900 border-t">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Activity className="h-6 w-6 text-blue-600" />
              <span className="font-semibold text-gray-900 dark:text-white">IR FitMark</span>
              <Badge variant="outline">v1.0.0</Badge>
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-300">
              © 2024 IR FitMark Team. Built for Smart India Hackathon.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
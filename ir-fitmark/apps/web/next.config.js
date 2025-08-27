/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    // Type checking is handled by turbo
    ignoreBuildErrors: false,
  },
  eslint: {
    // Linting is handled by turbo
    ignoreDuringBuilds: false,
  },
  images: {
    domains: [
      'localhost',
      '127.0.0.1',
      'ir-fitmark.s3.amazonaws.com',
      'storage.googleapis.com',
    ],
  },
  experimental: {
    // Enable experimental features
    serverComponentsExternalPackages: ['@pkg/shared'],
  },
  // Environment variables to expose to the client
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'IR FitMark',
  },
}

module.exports = nextConfig
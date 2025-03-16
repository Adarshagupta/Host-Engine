import type { NextPage } from 'next'
import Head from 'next/head'
import Link from 'next/link'

const Home: NextPage = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>Host Engine - Vercel Clone</title>
        <meta name="description" content="A Vercel-inspired platform for deploying web applications" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Host Engine</h1>
          <p className="text-xl text-gray-600 mb-8">
            A Vercel-inspired platform for deploying web applications directly from Git repositories
          </p>
          
          <div className="flex justify-center space-x-4">
            <Link href="/login" className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition">
              Login
            </Link>
            <Link href="/register" className="px-6 py-3 bg-white text-primary-600 border border-primary-600 rounded-md hover:bg-gray-50 transition">
              Register
            </Link>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Easy Deployment</h2>
            <p className="text-gray-600">
              Connect your GitHub repository and deploy with a single click. Automatic deployments on every push.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Custom Domains</h2>
            <p className="text-gray-600">
              Connect your custom domains to your projects with automatic SSL certificates.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Team Collaboration</h2>
            <p className="text-gray-600">
              Invite team members to collaborate on your projects with fine-grained permissions.
            </p>
          </div>
        </div>
      </main>

      <footer className="bg-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>© 2023 Host Engine. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export default Home 
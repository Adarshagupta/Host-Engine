import Link from 'next/link';
import Head from 'next/head';

export default function Custom500() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <Head>
        <title>500 - Server Error | Host Engine</title>
      </Head>
      
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <h1 className="text-9xl font-bold text-red-600 mb-4">500</h1>
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Server Error</h2>
        <p className="text-gray-600 mb-8">
          Sorry, something went wrong on our servers. We're working to fix the issue.
        </p>
        <Link href="/" className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition inline-block">
          Return to Home
        </Link>
      </div>
    </div>
  );
} 
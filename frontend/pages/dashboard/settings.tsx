import { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useAuth } from '../../context/AuthContext';

const Settings = () => {
  const { user, loading, isAuthenticated } = useAuth();
  const router = useRouter();
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [loading, isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setMessage({ type: '', text: '' });

    try {
      // In a real app, you would save these settings to the backend
      // await api.put('/users/me/settings', { emailNotifications, darkMode });
      
      // For demo, just simulate a successful save
      setTimeout(() => {
        setMessage({ 
          type: 'success', 
          text: 'Settings saved successfully!' 
        });
        setIsSaving(false);
      }, 1000);
    } catch (error: any) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to save settings' 
      });
      setIsSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex justify-center items-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>Settings - Host Engine</title>
      </Head>

      <main className="py-10">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Application Settings</h1>

          {message.text && (
            <div 
              className={`mb-6 p-4 border-l-4 ${
                message.type === 'success' 
                  ? 'bg-green-50 border-green-400 text-green-700' 
                  : 'bg-red-50 border-red-400 text-red-700'
              }`}
            >
              {message.text}
            </div>
          )}

          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <form onSubmit={handleSubmit} className="p-6 space-y-6">
              <div>
                <h2 className="text-lg font-medium text-gray-900 mb-4">Notifications</h2>
                
                <div className="flex items-center">
                  <input
                    id="emailNotifications"
                    type="checkbox"
                    checked={emailNotifications}
                    onChange={(e) => setEmailNotifications(e.target.checked)}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label htmlFor="emailNotifications" className="ml-3 block text-sm font-medium text-gray-700">
                    Receive email notifications
                  </label>
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  We'll send you updates about your deployments and other important events.
                </p>
              </div>

              <div className="pt-6 border-t border-gray-200">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Display</h2>
                
                <div className="flex items-center">
                  <input
                    id="darkMode"
                    type="checkbox"
                    checked={darkMode}
                    onChange={(e) => setDarkMode(e.target.checked)}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label htmlFor="darkMode" className="ml-3 block text-sm font-medium text-gray-700">
                    Dark mode
                  </label>
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  Use dark theme for the application interface.
                </p>
              </div>

              <div className="pt-6 border-t border-gray-200">
                <button
                  type="submit"
                  disabled={isSaving}
                  className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
                >
                  {isSaving ? 'Saving...' : 'Save settings'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Settings; 
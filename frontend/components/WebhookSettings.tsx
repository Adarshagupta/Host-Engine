import { useState, useEffect } from 'react';
import api from '../utils/api';

interface WebhookSettingsProps {
  projectId: string;
  initialWebhookSecret: string | null;
  onUpdate?: (webhookSecret: string | null) => void;
}

const WebhookSettings = ({ projectId, initialWebhookSecret, onUpdate }: WebhookSettingsProps) => {
  const [webhookSecret, setWebhookSecret] = useState<string>(initialWebhookSecret || '');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [githubWebhookUrl, setGithubWebhookUrl] = useState('');
  const [gitlabWebhookUrl, setGitlabWebhookUrl] = useState('');

  useEffect(() => {
    // Update webhook URLs when component mounts
    const baseUrl = window.location.origin;
    setGithubWebhookUrl(`${baseUrl}/api/webhooks/github`);
    setGitlabWebhookUrl(`${baseUrl}/api/webhooks/gitlab`);
  }, []);

  useEffect(() => {
    // Update the component state if the prop changes
    if (initialWebhookSecret !== null) {
      setWebhookSecret(initialWebhookSecret);
    }
  }, [initialWebhookSecret]);

  const generateSecret = () => {
    setIsGenerating(true);
    setError('');
    setSuccess('');

    // Generate a random string of 32 characters
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    const charactersLength = characters.length;
    
    for (let i = 0; i < 32; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    
    setWebhookSecret(result);
    setIsGenerating(false);
  };

  const saveWebhookSecret = async () => {
    try {
      setIsSaving(true);
      setError('');
      setSuccess('');

      await api.patch(`/projects/${projectId}`, {
        webhook_secret: webhookSecret || null
      });

      setSuccess('Webhook secret saved successfully');
      
      if (onUpdate) {
        onUpdate(webhookSecret || null);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save webhook secret');
    } finally {
      setIsSaving(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(
      () => {
        setSuccess('Copied to clipboard');
        setTimeout(() => setSuccess(''), 3000);
      },
      () => {
        setError('Failed to copy to clipboard');
      }
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Webhook Settings</h2>
        <p className="text-sm text-gray-600 mb-4">
          Configure webhooks to automatically deploy your project when code is pushed to your repository.
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {success && (
        <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-green-700">{success}</p>
            </div>
          </div>
        </div>
      )}

      <div className="bg-white overflow-hidden shadow rounded-lg divide-y divide-gray-200">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Webhook Secret</h3>
          <p className="mt-1 text-sm text-gray-500">
            A secret token used to verify webhook requests from your Git provider.
          </p>
        </div>
        <div className="px-4 py-5 sm:p-6">
          <div className="flex flex-col space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
              <div className="flex-grow">
                <input
                  type="text"
                  value={webhookSecret}
                  onChange={(e) => setWebhookSecret(e.target.value)}
                  placeholder="Webhook secret (leave empty to disable)"
                  className="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                />
              </div>
              <div className="flex space-x-2">
                <button
                  type="button"
                  onClick={generateSecret}
                  disabled={isGenerating}
                  className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  {isGenerating ? 'Generating...' : 'Generate'}
                </button>
                <button
                  type="button"
                  onClick={saveWebhookSecret}
                  disabled={isSaving}
                  className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  {isSaving ? 'Saving...' : 'Save'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white overflow-hidden shadow rounded-lg divide-y divide-gray-200">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Webhook URLs</h3>
          <p className="mt-1 text-sm text-gray-500">
            Configure your Git provider to send webhook events to these URLs.
          </p>
        </div>
        <div className="px-4 py-5 sm:p-6">
          <div className="space-y-4">
            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="block text-sm font-medium text-gray-700">GitHub Webhook URL</label>
                <button
                  onClick={() => copyToClipboard(githubWebhookUrl)}
                  className="text-primary-600 hover:text-primary-500 text-sm"
                >
                  Copy
                </button>
              </div>
              <div className="mt-1 flex rounded-md shadow-sm">
                <input
                  type="text"
                  readOnly
                  value={githubWebhookUrl}
                  className="flex-1 min-w-0 block w-full px-3 py-2 rounded-md text-sm text-gray-900 bg-gray-50 border border-gray-300"
                />
              </div>
              <p className="mt-1 text-xs text-gray-500">Content type: application/json</p>
            </div>
            
            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="block text-sm font-medium text-gray-700">GitLab Webhook URL</label>
                <button
                  onClick={() => copyToClipboard(gitlabWebhookUrl)}
                  className="text-primary-600 hover:text-primary-500 text-sm"
                >
                  Copy
                </button>
              </div>
              <div className="mt-1 flex rounded-md shadow-sm">
                <input
                  type="text"
                  readOnly
                  value={gitlabWebhookUrl}
                  className="flex-1 min-w-0 block w-full px-3 py-2 rounded-md text-sm text-gray-900 bg-gray-50 border border-gray-300"
                />
              </div>
              <p className="mt-1 text-xs text-gray-500">Trigger: Push events</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Setup Instructions</h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-semibold text-gray-900">GitHub</h4>
              <ol className="mt-2 text-sm text-gray-600 list-decimal pl-5 space-y-1">
                <li>Go to your GitHub repository</li>
                <li>Click on Settings &gt; Webhooks &gt; Add webhook</li>
                <li>Enter the GitHub Webhook URL</li>
                <li>Set content type to "application/json"</li>
                <li>Enter your webhook secret</li>
                <li>Select "Just the push event"</li>
                <li>Click "Add webhook"</li>
              </ol>
            </div>
            
            <div>
              <h4 className="text-sm font-semibold text-gray-900">GitLab</h4>
              <ol className="mt-2 text-sm text-gray-600 list-decimal pl-5 space-y-1">
                <li>Go to your GitLab repository</li>
                <li>Click on Settings &gt; Webhooks</li>
                <li>Enter the GitLab Webhook URL</li>
                <li>Leave the Secret Token field empty</li>
                <li>Select "Push events" trigger</li>
                <li>Click "Add webhook"</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WebhookSettings; 
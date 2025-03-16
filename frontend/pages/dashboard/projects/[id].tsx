import { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { useAuth } from '../../../context/AuthContext';
import api from '../../../utils/api';
import DomainManagement from '../../../components/DomainManagement';
import EnvironmentVariables from '../../../components/EnvironmentVariables';
import DeploymentLogs from '../../../components/DeploymentLogs';
import WebhookSettings from '../../../components/WebhookSettings';

interface Project {
  id: string;
  name: string;
  description: string;
  repository_url: string;
  branch: string;
  build_command: string;
  output_directory: string;
  created_at: string;
  environment_variables: Record<string, string>;
  webhook_secret: string | null;
}

interface Deployment {
  id: string;
  status: string;
  created_at: string;
  deployment_url: string;
  commit_hash: string;
  commit_message: string;
}

const ProjectDetail = () => {
  const [project, setProject] = useState<Project | null>(null);
  const [deployments, setDeployments] = useState<Deployment[]>([]);
  const [loading, setLoading] = useState(true);
  const [deployLoading, setDeployLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('deployments');
  const [selectedDeployment, setSelectedDeployment] = useState<string | null>(null);
  const router = useRouter();
  const { id } = router.query;
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    if (id) {
      fetchProject();
      fetchDeployments();
    }
  }, [id, isAuthenticated, router]);

  const fetchProject = async () => {
    try {
      const response = await api.get(`/projects/${id}`);
      setProject(response.data);
    } catch (error) {
      console.error('Failed to fetch project:', error);
      setError('Failed to load project details');
    } finally {
      setLoading(false);
    }
  };

  const fetchDeployments = async () => {
    try {
      const response = await api.get(`/deployments?project_id=${id}`);
      setDeployments(response.data);
      
      // Set the first deployment as selected if available and none is selected
      if (response.data.length > 0 && !selectedDeployment) {
        setSelectedDeployment(response.data[0].id);
      }
    } catch (error) {
      console.error('Failed to fetch deployments:', error);
    }
  };

  const handleDeploy = async () => {
    if (!project) return;

    try {
      setDeployLoading(true);
      setError('');

      await api.post('/deployments', {
        project_id: project.id,
      });

      // Refresh deployments after a short delay
      setTimeout(() => {
        fetchDeployments();
        setDeployLoading(false);
      }, 1000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start deployment');
      setDeployLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'ready':
        return 'bg-green-100 text-green-800';
      case 'building':
      case 'queued':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading project details...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>{project?.name || 'Project'} - Host Engine</title>
      </Head>

      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <div className="flex items-center">
            <Link href="/dashboard" className="mr-4 text-gray-500 hover:text-gray-700">
              &larr; Back
            </Link>
            <h1 className="text-3xl font-bold text-gray-900">{project?.name}</h1>
          </div>
          <button
            onClick={handleDeploy}
            disabled={deployLoading}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            {deployLoading ? 'Deploying...' : 'Deploy Now'}
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="px-4 py-3 mb-6 bg-red-50 border-l-4 border-red-400 text-red-700">
            {error}
          </div>
        )}

        <div className="px-4 sm:px-0">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Project Information</h3>
            </div>
            <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
              <dl className="sm:divide-y sm:divide-gray-200">
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Project name</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{project?.name}</dd>
                </div>
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Description</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{project?.description || 'No description'}</dd>
                </div>
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Repository</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{project?.repository_url}</dd>
                </div>
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Branch</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{project?.branch}</dd>
                </div>
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Build command</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{project?.build_command || 'No build command'}</dd>
                </div>
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Output directory</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{project?.output_directory}</dd>
                </div>
              </dl>
            </div>
          </div>

          <div className="mb-6 border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('deployments')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'deployments'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Deployments
              </button>
              <button
                onClick={() => setActiveTab('env-vars')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'env-vars'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Environment Variables
              </button>
              <button
                onClick={() => setActiveTab('domains')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'domains'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Domains
              </button>
              <button
                onClick={() => setActiveTab('webhooks')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'webhooks'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Webhooks
              </button>
              {selectedDeployment && (
                <button
                  onClick={() => setActiveTab('logs')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'logs'
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Logs
                </button>
              )}
            </nav>
          </div>

          <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
            {activeTab === 'deployments' && (
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Deployments</h2>
                {deployments.length === 0 ? (
                  <p className="text-gray-500">No deployments yet. Click "Deploy Now" to create your first deployment.</p>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Status
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Commit
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Created At
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Actions
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {deployments.map((deployment) => (
                          <tr key={deployment.id} className={selectedDeployment === deployment.id ? 'bg-gray-50' : ''}>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadgeClass(deployment.status)}`}>
                                {deployment.status}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">
                                {deployment.commit_hash ? deployment.commit_hash.substring(0, 7) : 'N/A'}
                              </div>
                              <div className="text-sm text-gray-500">
                                {deployment.commit_message ? deployment.commit_message.split('\n')[0] : ''}
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {formatDate(deployment.created_at)}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                              <button
                                onClick={() => {
                                  setSelectedDeployment(deployment.id);
                                  setActiveTab('logs');
                                }}
                                className="text-primary-600 hover:text-primary-900 mr-4"
                              >
                                View Logs
                              </button>
                              {deployment.deployment_url && (
                                <a
                                  href={deployment.deployment_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-primary-600 hover:text-primary-900"
                                >
                                  Visit
                                </a>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'env-vars' && project && (
              <EnvironmentVariables 
                projectId={project.id} 
                initialEnvVars={project.environment_variables || {}} 
                onUpdate={(envVars) => {
                  if (project) {
                    setProject({
                      ...project,
                      environment_variables: envVars
                    });
                  }
                }}
              />
            )}

            {activeTab === 'domains' && project && (
              <DomainManagement projectId={project.id} />
            )}

            {activeTab === 'webhooks' && project && (
              <WebhookSettings 
                projectId={project.id} 
                initialWebhookSecret={project.webhook_secret}
                onUpdate={(webhookSecret) => {
                  if (project) {
                    setProject({
                      ...project,
                      webhook_secret: webhookSecret
                    });
                  }
                }}
              />
            )}

            {activeTab === 'logs' && selectedDeployment && (
              <DeploymentLogs deploymentId={selectedDeployment} />
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default ProjectDetail; 
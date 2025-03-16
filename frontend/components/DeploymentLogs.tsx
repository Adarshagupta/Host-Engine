import { useState, useEffect } from 'react';
import api from '../utils/api';

interface DeploymentLogsProps {
  deploymentId: string;
}

const DeploymentLogs: React.FC<DeploymentLogsProps> = ({ deploymentId }) => {
  const [logs, setLogs] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deployment, setDeployment] = useState<any>(null);
  const [autoRefresh, setAutoRefresh] = useState(false);

  useEffect(() => {
    fetchDeployment();
    
    // Auto-refresh logs for in-progress deployments
    let interval: NodeJS.Timeout | null = null;
    
    if (autoRefresh) {
      interval = setInterval(fetchDeployment, 3000);
    }
    
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [deploymentId, autoRefresh]);

  const fetchDeployment = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/deployments/${deploymentId}`);
      setDeployment(response.data);
      
      // Set logs from deployment data
      let logContent = '';
      
      if (response.data.build_logs) {
        logContent += "=== BUILD LOGS ===\n";
        logContent += response.data.build_logs;
        logContent += "\n\n";
      }
      
      if (response.data.error_message) {
        logContent += "=== ERROR ===\n";
        logContent += response.data.error_message;
      }
      
      setLogs(logContent || 'No logs available.');
      
      // Auto-refresh only for ongoing deployments
      if (response.data.status === 'queued' || response.data.status === 'building') {
        setAutoRefresh(true);
      } else {
        setAutoRefresh(false);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch deployment logs');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
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

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900">Deployment Logs</h2>
        {deployment && (
          <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(deployment.status)}`}>
            {deployment.status.toUpperCase()}
          </span>
        )}
      </div>
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}
      
      {loading && !logs ? (
        <div className="text-gray-500">Loading logs...</div>
      ) : (
        <div className="bg-gray-800 text-gray-100 p-4 rounded-md">
          <pre className="whitespace-pre-wrap break-words overflow-auto max-h-96">
            {logs}
          </pre>
        </div>
      )}
      
      <div className="flex justify-end">
        <button
          type="button"
          onClick={fetchDeployment}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          Refresh Logs
        </button>
      </div>
    </div>
  );
};

export default DeploymentLogs; 
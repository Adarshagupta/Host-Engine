import { useState, useEffect } from 'react';
import api from '../utils/api';

interface EnvironmentVariablesProps {
  projectId: string;
  initialEnvVars?: Record<string, string>;
  onUpdate?: (envVars: Record<string, string>) => void;
}

const EnvironmentVariables: React.FC<EnvironmentVariablesProps> = ({ 
  projectId, 
  initialEnvVars = {}, 
  onUpdate 
}) => {
  const [envVars, setEnvVars] = useState<Record<string, string>>(initialEnvVars);
  const [newVarKey, setNewVarKey] = useState('');
  const [newVarValue, setNewVarValue] = useState('');
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (Object.keys(initialEnvVars).length > 0) {
      setEnvVars(initialEnvVars);
    } else {
      fetchProject();
    }
  }, [projectId, initialEnvVars]);

  const fetchProject = async () => {
    try {
      const response = await api.get(`/projects/${projectId}`);
      if (response.data.environment_variables) {
        setEnvVars(response.data.environment_variables);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch project environment variables');
    }
  };

  const handleAddVariable = () => {
    if (!newVarKey.trim()) {
      setError('Variable name is required');
      return;
    }

    setEnvVars((prev) => ({
      ...prev,
      [newVarKey]: newVarValue
    }));

    setNewVarKey('');
    setNewVarValue('');
  };

  const handleRemoveVariable = (key: string) => {
    const updatedVars = { ...envVars };
    delete updatedVars[key];
    setEnvVars(updatedVars);
  };

  const handleSaveChanges = async () => {
    try {
      setSaving(true);
      setError('');

      const response = await api.put(`/projects/${projectId}`, {
        environment_variables: envVars
      });

      if (onUpdate) {
        onUpdate(envVars);
      }
      
      setSaving(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save environment variables');
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-900">Environment Variables</h2>
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      <div>
        <div className="flex space-x-4 mb-4">
          <input
            type="text"
            placeholder="KEY"
            value={newVarKey}
            onChange={(e) => setNewVarKey(e.target.value)}
            className="flex-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
          />
          <input
            type="text"
            placeholder="VALUE"
            value={newVarValue}
            onChange={(e) => setNewVarValue(e.target.value)}
            className="flex-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
          />
          <button
            type="button"
            onClick={handleAddVariable}
            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Add
          </button>
        </div>

        {Object.keys(envVars).length === 0 ? (
          <p className="text-gray-500">No environment variables defined.</p>
        ) : (
          <div className="mt-4 border border-gray-200 rounded-md overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Key
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Value
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {Object.entries(envVars).map(([key, value]) => (
                  <tr key={key}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {key}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {value}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleRemoveVariable(key)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="mt-6">
          <button
            type="button"
            onClick={handleSaveChanges}
            disabled={saving}
            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default EnvironmentVariables; 
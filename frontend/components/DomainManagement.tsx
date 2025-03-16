import { useState, useEffect } from 'react';
import api from '../utils/api';

interface Domain {
  id: string;
  name: string;
  verified: boolean;
  created_at: string;
}

interface DomainManagementProps {
  projectId: string;
}

const DomainManagement: React.FC<DomainManagementProps> = ({ projectId }) => {
  const [domains, setDomains] = useState<Domain[]>([]);
  const [newDomain, setNewDomain] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [addingDomain, setAddingDomain] = useState(false);

  useEffect(() => {
    fetchDomains();
  }, [projectId]);

  const fetchDomains = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/domains?project_id=${projectId}`);
      setDomains(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch domains');
    } finally {
      setLoading(false);
    }
  };

  const handleAddDomain = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newDomain.trim()) {
      setError('Domain name is required');
      return;
    }

    try {
      setAddingDomain(true);
      setError('');
      
      await api.post('/domains', {
        name: newDomain,
        project_id: projectId
      });
      
      setNewDomain('');
      await fetchDomains();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add domain');
    } finally {
      setAddingDomain(false);
    }
  };

  const handleVerifyDomain = async (domainId: string) => {
    try {
      await api.post(`/domains/${domainId}/verify`);
      await fetchDomains();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to verify domain');
    }
  };

  const handleDeleteDomain = async (domainId: string) => {
    if (!window.confirm('Are you sure you want to delete this domain?')) {
      return;
    }
    
    try {
      await api.delete(`/domains/${domainId}`);
      await fetchDomains();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete domain');
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-900">Custom Domains</h2>
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}
      
      <form onSubmit={handleAddDomain} className="flex space-x-4">
        <input
          type="text"
          value={newDomain}
          onChange={(e) => setNewDomain(e.target.value)}
          placeholder="example.com"
          className="flex-grow p-2 border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
          disabled={addingDomain}
        />
        <button
          type="submit"
          disabled={addingDomain}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
        >
          {addingDomain ? 'Adding...' : 'Add Domain'}
        </button>
      </form>
      
      {loading ? (
        <div className="text-gray-500">Loading domains...</div>
      ) : domains.length === 0 ? (
        <div className="text-gray-500">No domains added yet.</div>
      ) : (
        <div className="mt-4 border border-gray-200 rounded-md overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Domain
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {domains.map((domain) => (
                <tr key={domain.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {domain.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {domain.verified ? (
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Verified
                      </span>
                    ) : (
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                        Pending Verification
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    {!domain.verified && (
                      <button
                        onClick={() => handleVerifyDomain(domain.id)}
                        className="text-primary-600 hover:text-primary-900 mr-4"
                      >
                        Verify
                      </button>
                    )}
                    <button
                      onClick={() => handleDeleteDomain(domain.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default DomainManagement; 
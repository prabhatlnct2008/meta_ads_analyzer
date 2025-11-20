'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { Loading } from '@/components/ui/Loading';
import { api, getErrorMessage } from '@/lib/api';
import type { Campaign, MetaAdAccount } from '@/lib/types';
import toast from 'react-hot-toast';

export default function CampaignsPage() {
  const [accounts, setAccounts] = useState<MetaAdAccount[]>([]);
  const [selectedAccount, setSelectedAccount] = useState<MetaAdAccount | null>(null);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [datePreset, setDatePreset] = useState('last_7d');

  useEffect(() => {
    loadAccounts();
  }, []);

  useEffect(() => {
    if (selectedAccount) {
      loadCampaigns();
    }
  }, [selectedAccount, datePreset]);

  const loadAccounts = async () => {
    try {
      const response = await api.getMetaAccounts();
      setAccounts(response.accounts);
      if (response.accounts.length > 0) {
        setSelectedAccount(response.accounts[0]);
      } else {
        setLoading(false);
      }
    } catch (error) {
      toast.error(getErrorMessage(error));
      setLoading(false);
    }
  };

  const loadCampaigns = async () => {
    if (!selectedAccount) return;

    setLoading(true);
    try {
      const response = await api.getCampaigns(selectedAccount.id, datePreset);
      setCampaigns(response.campaigns);
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loading size="lg" text="Loading campaigns..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Campaigns</h1>
        <select
          value={datePreset}
          onChange={(e) => setDatePreset(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="last_7d">Last 7 Days</option>
          <option value="last_30d">Last 30 Days</option>
          <option value="this_month">This Month</option>
        </select>
      </div>

      <Card padding={false}>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Campaign</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Spend</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Conversions</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">CPA</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">ROAS</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">CTR</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {campaigns.map((campaign) => (
                <tr key={campaign.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="font-medium text-gray-900">{campaign.name}</div>
                    <div className="text-sm text-gray-500">{campaign.objective}</div>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        campaign.status === 'ACTIVE'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {campaign.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-gray-900">
                    ${campaign.spend.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-gray-900">
                    {campaign.conversions.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-gray-900">
                    ${campaign.cpa.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 text-right text-sm">
                    <span
                      className={`font-semibold ${
                        campaign.roas >= 2 ? 'text-green-600' : 'text-orange-600'
                      }`}
                    >
                      {campaign.roas.toFixed(2)}x
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right text-sm text-gray-900">
                    {campaign.ctr.toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {campaigns.length === 0 && !loading && (
        <div className="text-center py-12">
          <p className="text-gray-500">No campaigns found for the selected period.</p>
        </div>
      )}
    </div>
  );
}

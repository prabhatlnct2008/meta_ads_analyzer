'use client';

import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Loading } from '@/components/ui/Loading';
import { api, getErrorMessage } from '@/lib/api';
import type { OverviewMetrics, MetaAdAccount } from '@/lib/types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import toast from 'react-hot-toast';

export default function DashboardPage() {
  const [accounts, setAccounts] = useState<MetaAdAccount[]>([]);
  const [selectedAccount, setSelectedAccount] = useState<MetaAdAccount | null>(null);
  const [overview, setOverview] = useState<OverviewMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [datePreset, setDatePreset] = useState('last_7d');

  useEffect(() => {
    loadAccounts();
  }, []);

  useEffect(() => {
    if (selectedAccount) {
      loadOverview();
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

  const loadOverview = async () => {
    if (!selectedAccount) return;

    setLoading(true);
    try {
      const response = await api.getOverview(selectedAccount.id, datePreset);
      setOverview(response.overview);
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const handleConnectAccount = async () => {
    try {
      const response = await api.getMetaConnectUrl();
      window.location.href = response.oauth_url;
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loading size="lg" text="Loading dashboard..." />
      </div>
    );
  }

  if (accounts.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full">
        <Card className="max-w-md text-center">
          <CardHeader>
            <CardTitle>Connect Your Facebook Ads</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-6">
              Get started by connecting your Meta Ads account to see your performance data.
            </p>
            <button
              onClick={handleConnectAccount}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Connect Facebook Ads Account
            </button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
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

      {overview && (
        <>
          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">Total Spend</div>
                <div className="text-3xl font-bold text-gray-900">${overview.spend.toLocaleString()}</div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">Conversions</div>
                <div className="text-3xl font-bold text-gray-900">{overview.conversions.toLocaleString()}</div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">CPA</div>
                <div className="text-3xl font-bold text-gray-900">${overview.cpa.toFixed(2)}</div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">ROAS</div>
                <div className={`text-3xl font-bold ${overview.roas >= 2 ? 'text-green-600' : 'text-orange-600'}`}>
                  {overview.roas.toFixed(2)}x
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Additional Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">Impressions</div>
                <div className="text-2xl font-bold text-gray-900">{overview.impressions.toLocaleString()}</div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">Clicks</div>
                <div className="text-2xl font-bold text-gray-900">{overview.clicks.toLocaleString()}</div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-sm text-gray-600 mb-1">CTR</div>
                <div className="text-2xl font-bold text-gray-900">{overview.ctr.toFixed(2)}%</div>
              </CardContent>
            </Card>
          </div>

          {/* Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Performance Over Time</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={overview.daily_data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip />
                    <Legend />
                    <Line yAxisId="left" type="monotone" dataKey="spend" stroke="#3b82f6" name="Spend ($)" />
                    <Line yAxisId="right" type="monotone" dataKey="conversions" stroke="#10b981" name="Conversions" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}

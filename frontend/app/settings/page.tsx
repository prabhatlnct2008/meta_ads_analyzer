'use client';

import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Loading } from '@/components/ui/Loading';
import { api, getErrorMessage } from '@/lib/api';
import type { MetaAdAccount, User } from '@/lib/types';
import toast from 'react-hot-toast';

export default function SettingsPage() {
  const [user, setUser] = useState<User | null>(null);
  const [accounts, setAccounts] = useState<MetaAdAccount[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [userResponse, accountsResponse] = await Promise.all([
        api.getCurrentUser(),
        api.getMetaAccounts(),
      ]);
      setUser(userResponse.user);
      setAccounts(accountsResponse.accounts);
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

  const handleDisconnect = async (connectionId: string) => {
    if (!confirm('Are you sure you want to disconnect this account?')) return;

    try {
      await api.disconnectMeta(connectionId);
      toast.success('Account disconnected successfully');
      loadData();
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const handleRefreshAccount = async (accountId: string) => {
    try {
      await api.refreshMetaAccount(accountId);
      toast.success('Account refreshed successfully');
      loadData();
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loading size="lg" text="Loading settings..." />
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      <h1 className="text-3xl font-bold text-gray-900">Settings</h1>

      {/* Profile Section */}
      <Card>
        <CardHeader>
          <CardTitle>Profile</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <div className="text-gray-900">{user?.email}</div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Member Since</label>
              <div className="text-gray-900">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Connected Accounts */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Connected Meta Ad Accounts</CardTitle>
            <Button onClick={handleConnectAccount} size="sm">
              Connect New Account
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {accounts.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p className="mb-4">No accounts connected yet.</p>
              <Button onClick={handleConnectAccount}>Connect Your First Account</Button>
            </div>
          ) : (
            <div className="space-y-4">
              {accounts.map((account) => (
                <div
                  key={account.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                >
                  <div>
                    <div className="font-medium text-gray-900">{account.name}</div>
                    <div className="text-sm text-gray-500">
                      {account.account_id} • {account.currency}
                    </div>
                    <div className="text-xs text-gray-400 mt-1">
                      Last updated: {new Date(account.updated_at).toLocaleString()}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleRefreshAccount(account.id)}
                    >
                      Refresh
                    </Button>
                    <Button
                      size="sm"
                      variant="danger"
                      onClick={() => handleDisconnect(account.meta_connection_id)}
                    >
                      Disconnect
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* About */}
      <Card>
        <CardHeader>
          <CardTitle>About</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm text-gray-600">
            <p>Meta Ads Analyzer - AI-powered Facebook Ads analytics</p>
            <p>Version 1.0.0</p>
            <p>&copy; 2024 Meta Ads Analyzer. All rights reserved.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

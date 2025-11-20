'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import type { MetaAdAccount } from '@/lib/types';
import { Button } from '@/components/ui/Button';

interface TopBarProps {
  selectedAccount: MetaAdAccount | null;
  onAccountChange: (account: MetaAdAccount) => void;
}

export function TopBar({ selectedAccount, onAccountChange }: TopBarProps) {
  const router = useRouter();
  const [accounts, setAccounts] = useState<MetaAdAccount[]>([]);
  const [showAccountMenu, setShowAccountMenu] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);

  useEffect(() => {
    loadAccounts();
  }, []);

  const loadAccounts = async () => {
    try {
      const response = await api.getMetaAccounts();
      setAccounts(response.accounts);
      if (response.accounts.length > 0 && !selectedAccount) {
        onAccountChange(response.accounts[0]);
      }
    } catch (error) {
      console.error('Error loading accounts:', error);
    }
  };

  const handleLogout = () => {
    api.clearToken();
    router.push('/login');
  };

  const handleConnectAccount = async () => {
    try {
      const response = await api.getMetaConnectUrl();
      window.location.href = response.oauth_url;
    } catch (error) {
      console.error('Error getting OAuth URL:', error);
    }
  };

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
      <div className="relative">
        {accounts.length > 0 ? (
          <>
            <button
              onClick={() => setShowAccountMenu(!showAccountMenu)}
              className="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors flex items-center space-x-2"
            >
              <span className="font-medium">{selectedAccount?.name || 'Select Account'}</span>
              <span>▼</span>
            </button>

            {showAccountMenu && (
              <div className="absolute top-full mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 z-10">
                {accounts.map((account) => (
                  <button
                    key={account.id}
                    onClick={() => {
                      onAccountChange(account);
                      setShowAccountMenu(false);
                    }}
                    className="w-full px-4 py-3 text-left hover:bg-gray-50 first:rounded-t-lg last:rounded-b-lg"
                  >
                    <div className="font-medium">{account.name}</div>
                    <div className="text-sm text-gray-500">{account.account_id}</div>
                  </button>
                ))}
              </div>
            )}
          </>
        ) : (
          <Button onClick={handleConnectAccount} size="sm">
            Connect Facebook Ads
          </Button>
        )}
      </div>

      <div className="relative">
        <button
          onClick={() => setShowUserMenu(!showUserMenu)}
          className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold hover:bg-blue-700 transition-colors"
        >
          U
        </button>

        {showUserMenu && (
          <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10">
            <button
              onClick={() => {
                router.push('/settings');
                setShowUserMenu(false);
              }}
              className="w-full px-4 py-3 text-left hover:bg-gray-50 rounded-t-lg"
            >
              Settings
            </button>
            <button
              onClick={handleLogout}
              className="w-full px-4 py-3 text-left hover:bg-gray-50 rounded-b-lg text-red-600"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

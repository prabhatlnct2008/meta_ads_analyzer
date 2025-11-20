'use client';

import { useState } from 'react';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { TopBar } from '@/components/dashboard/TopBar';
import type { MetaAdAccount } from '@/lib/types';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [selectedAccount, setSelectedAccount] = useState<MetaAdAccount | null>(null);

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar
          selectedAccount={selectedAccount}
          onAccountChange={setSelectedAccount}
        />
        <main className="flex-1 overflow-y-auto p-6">
          {/* Pass selectedAccount to children via context or props */}
          {children}
        </main>
      </div>
    </div>
  );
}

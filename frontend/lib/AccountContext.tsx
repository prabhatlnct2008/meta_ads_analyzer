'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import type { MetaAdAccount } from './types';

interface AccountContextType {
  selectedAccount: MetaAdAccount | null;
  setSelectedAccount: (account: MetaAdAccount | null) => void;
}

const AccountContext = createContext<AccountContextType | undefined>(undefined);

export function AccountProvider({ children }: { children: ReactNode }) {
  const [selectedAccount, setSelectedAccount] = useState<MetaAdAccount | null>(null);

  return (
    <AccountContext.Provider value={{ selectedAccount, setSelectedAccount }}>
      {children}
    </AccountContext.Provider>
  );
}

export function useAccount() {
  const context = useContext(AccountContext);
  if (context === undefined) {
    throw new Error('useAccount must be used within an AccountProvider');
  }
  return context;
}

// User types
export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  message: string;
}

// Meta Account types
export interface MetaAdAccount {
  id: string;
  user_id: string;
  meta_connection_id: string;
  account_id: string;
  name: string;
  currency: string;
  status: string;
  created_at: string;
  updated_at: string;
}

// Analytics types
export interface OverviewMetrics {
  spend: number;
  impressions: number;
  clicks: number;
  conversions: number;
  revenue: number;
  ctr: number;
  cpc: number;
  cpa: number;
  roas: number;
  daily_data: DailyData[];
}

export interface DailyData {
  date: string;
  spend: number;
  impressions: number;
  clicks: number;
  conversions: number;
  revenue: number;
}

export interface Campaign {
  id: string;
  name: string;
  status: string;
  objective: string;
  spend: number;
  impressions: number;
  clicks: number;
  conversions: number;
  revenue: number;
  ctr: number;
  cpc: number;
  cpa: number;
  roas: number;
}

// Chat types
export interface ChatConversation {
  id: string;
  user_id: string;
  meta_ad_account_id?: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages?: ChatMessage[];
}

export interface ChatMessage {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  metadata?: any;
  created_at: string;
}

// API Response types
export interface ApiError {
  error: string;
}

export interface OverviewResponse {
  account_id: string;
  account_name: string;
  date_preset: string;
  overview: OverviewMetrics;
}

export interface CampaignsResponse {
  account_id: string;
  account_name: string;
  date_preset: string;
  campaigns: Campaign[];
}

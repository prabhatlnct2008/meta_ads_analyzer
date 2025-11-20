import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  AuthResponse,
  User,
  MetaAdAccount,
  OverviewResponse,
  CampaignsResponse,
  ChatConversation,
  ChatMessage,
  ApiError
} from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add token to requests if available
    this.client.interceptors.request.use((config) => {
      const token = this.getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  setToken(token: string) {
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  clearToken() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  // Auth endpoints
  async signup(email: string, password: string): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/api/auth/signup', {
      email,
      password,
    });
    return response.data;
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/api/auth/login', {
      email,
      password,
    });
    return response.data;
  }

  async logout(): Promise<void> {
    await this.client.post('/api/auth/logout');
    this.clearToken();
  }

  async getCurrentUser(): Promise<{ user: User }> {
    const response = await this.client.get<{ user: User }>('/api/auth/me');
    return response.data;
  }

  // Meta endpoints
  async getMetaConnectUrl(): Promise<{ oauth_url: string }> {
    const response = await this.client.get<{ oauth_url: string }>('/api/meta/connect');
    return response.data;
  }

  async getMetaAccounts(): Promise<{ accounts: MetaAdAccount[] }> {
    const response = await this.client.get<{ accounts: MetaAdAccount[] }>('/api/meta/accounts');
    return response.data;
  }

  async refreshMetaAccount(accountId: string): Promise<{ account: MetaAdAccount }> {
    const response = await this.client.post<{ account: MetaAdAccount }>(
      `/api/meta/accounts/${accountId}/refresh`
    );
    return response.data;
  }

  async disconnectMeta(connectionId: string): Promise<void> {
    await this.client.delete(`/api/meta/disconnect/${connectionId}`);
  }

  // Analytics endpoints
  async getOverview(accountId: string, datePreset: string = 'last_7d'): Promise<OverviewResponse> {
    const response = await this.client.get<OverviewResponse>('/api/analytics/overview', {
      params: { account_id: accountId, date_preset: datePreset },
    });
    return response.data;
  }

  async getCampaigns(accountId: string, datePreset: string = 'last_7d'): Promise<CampaignsResponse> {
    const response = await this.client.get<CampaignsResponse>('/api/analytics/campaigns', {
      params: { account_id: accountId, date_preset: datePreset },
    });
    return response.data;
  }

  async getCampaignDetail(campaignId: string, accountId: string, datePreset: string = 'last_7d') {
    const response = await this.client.get(`/api/analytics/campaigns/${campaignId}`, {
      params: { account_id: accountId, date_preset: datePreset },
    });
    return response.data;
  }

  // Chat endpoints
  async getConversations(): Promise<{ conversations: ChatConversation[] }> {
    const response = await this.client.get<{ conversations: ChatConversation[] }>('/api/chat/conversations');
    return response.data;
  }

  async createConversation(accountId: string, title?: string): Promise<{ conversation: ChatConversation }> {
    const response = await this.client.post<{ conversation: ChatConversation }>('/api/chat/conversations', {
      account_id: accountId,
      title,
    });
    return response.data;
  }

  async getMessages(conversationId: string): Promise<{ conversation: ChatConversation }> {
    const response = await this.client.get<{ conversation: ChatConversation }>(
      `/api/chat/conversations/${conversationId}/messages`
    );
    return response.data;
  }

  async sendMessage(
    conversationId: string,
    message: string,
    datePreset: string = 'last_7d'
  ): Promise<{ user_message: ChatMessage; assistant_message: ChatMessage }> {
    const response = await this.client.post(
      `/api/chat/conversations/${conversationId}/messages`,
      { message, date_preset: datePreset }
    );
    return response.data;
  }

  async deleteConversation(conversationId: string): Promise<void> {
    await this.client.delete(`/api/chat/conversations/${conversationId}`);
  }
}

export const api = new ApiClient();

// Helper to handle API errors
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;
    return axiosError.response?.data?.error || 'An error occurred';
  }
  return 'An unexpected error occurred';
}

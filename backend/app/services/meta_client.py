import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class MetaClient:
    """Client for interacting with Meta Marketing API"""

    BASE_URL = "https://graph.facebook.com/v19.0"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    def _make_request(self, endpoint: str, params: Optional[Dict] = None, method: str = 'GET'):
        """Make request to Meta API"""
        url = f"{self.BASE_URL}/{endpoint}"

        if params is None:
            params = {}

        params['access_token'] = self.access_token

        try:
            if method == 'GET':
                response = requests.get(url, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, params=params, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Meta API request error: {e}")
            raise

    def get_user_accounts(self) -> List[Dict]:
        """Get ad accounts for the authenticated user"""
        try:
            data = self._make_request('me/adaccounts', {
                'fields': 'id,account_id,name,currency,account_status,business,timezone_name'
            })
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching user accounts: {e}")
            raise

    def get_account_insights(self, account_id: str, date_preset: str = 'last_7d',
                            fields: Optional[List[str]] = None) -> Dict:
        """Get insights for an ad account"""
        if fields is None:
            fields = [
                'spend', 'impressions', 'clicks', 'ctr', 'cpc', 'cpp', 'cpm',
                'actions', 'conversions', 'cost_per_action_type',
                'action_values', 'purchase_roas'
            ]

        try:
            params = {
                'fields': ','.join(fields),
                'date_preset': date_preset,
                'level': 'account',
                'time_increment': 1
            }

            data = self._make_request(f'{account_id}/insights', params)
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching account insights: {e}")
            raise

    def get_account_insights_range(self, account_id: str, since: str, until: str,
                                   fields: Optional[List[str]] = None) -> Dict:
        """Get insights for an ad account with custom date range"""
        if fields is None:
            fields = [
                'spend', 'impressions', 'clicks', 'ctr', 'cpc', 'cpp', 'cpm',
                'actions', 'conversions', 'cost_per_action_type',
                'action_values', 'purchase_roas'
            ]

        try:
            params = {
                'fields': ','.join(fields),
                'time_range': f'{{"since":"{since}","until":"{until}"}}',
                'level': 'account',
                'time_increment': 1
            }

            data = self._make_request(f'{account_id}/insights', params)
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching account insights: {e}")
            raise

    def get_campaigns(self, account_id: str, fields: Optional[List[str]] = None,
                     limit: int = 100) -> List[Dict]:
        """Get campaigns for an ad account"""
        if fields is None:
            fields = [
                'id', 'name', 'status', 'objective', 'effective_status',
                'created_time', 'updated_time', 'daily_budget', 'lifetime_budget'
            ]

        try:
            params = {
                'fields': ','.join(fields),
                'limit': limit
            }

            data = self._make_request(f'{account_id}/campaigns', params)
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching campaigns: {e}")
            raise

    def get_campaign_insights(self, campaign_id: str, date_preset: str = 'last_7d',
                             fields: Optional[List[str]] = None) -> List[Dict]:
        """Get insights for a specific campaign"""
        if fields is None:
            fields = [
                'spend', 'impressions', 'clicks', 'ctr', 'cpc', 'cpm',
                'actions', 'conversions', 'cost_per_action_type',
                'action_values', 'purchase_roas'
            ]

        try:
            params = {
                'fields': ','.join(fields),
                'date_preset': date_preset,
                'level': 'campaign'
            }

            data = self._make_request(f'{campaign_id}/insights', params)
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching campaign insights: {e}")
            raise

    def get_campaign_insights_range(self, campaign_id: str, since: str, until: str,
                                   fields: Optional[List[str]] = None) -> List[Dict]:
        """Get campaign insights with custom date range"""
        if fields is None:
            fields = [
                'spend', 'impressions', 'clicks', 'ctr', 'cpc', 'cpm',
                'actions', 'conversions', 'cost_per_action_type',
                'action_values', 'purchase_roas'
            ]

        try:
            params = {
                'fields': ','.join(fields),
                'time_range': f'{{"since":"{since}","until":"{until}"}}',
                'level': 'campaign'
            }

            data = self._make_request(f'{campaign_id}/insights', params)
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching campaign insights: {e}")
            raise

    def get_adsets(self, campaign_id: str, fields: Optional[List[str]] = None) -> List[Dict]:
        """Get ad sets for a campaign"""
        if fields is None:
            fields = [
                'id', 'name', 'status', 'effective_status', 'daily_budget',
                'lifetime_budget', 'created_time', 'updated_time'
            ]

        try:
            params = {
                'fields': ','.join(fields),
                'limit': 100
            }

            data = self._make_request(f'{campaign_id}/adsets', params)
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching ad sets: {e}")
            raise

    def get_ads(self, adset_id: str, fields: Optional[List[str]] = None) -> List[Dict]:
        """Get ads for an ad set"""
        if fields is None:
            fields = [
                'id', 'name', 'status', 'effective_status',
                'created_time', 'updated_time'
            ]

        try:
            params = {
                'fields': ','.join(fields),
                'limit': 100
            }

            data = self._make_request(f'{adset_id}/ads', params)
            return data.get('data', [])
        except Exception as e:
            print(f"Error fetching ads: {e}")
            raise

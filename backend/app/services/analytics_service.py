from datetime import datetime, timedelta
from typing import Dict, List, Optional
from app.services.meta_client import MetaClient

class AnalyticsService:
    """Service for processing and aggregating Meta ads analytics"""

    def __init__(self, meta_client: MetaClient):
        self.meta_client = meta_client

    @staticmethod
    def get_date_range(preset: str) -> tuple:
        """Convert date preset to (since, until) strings"""
        today = datetime.now().date()

        if preset == 'last_7d':
            since = (today - timedelta(days=7)).strftime('%Y-%m-%d')
            until = today.strftime('%Y-%m-%d')
        elif preset == 'last_30d':
            since = (today - timedelta(days=30)).strftime('%Y-%m-%d')
            until = today.strftime('%Y-%m-%d')
        elif preset == 'this_month':
            since = today.replace(day=1).strftime('%Y-%m-%d')
            until = today.strftime('%Y-%m-%d')
        else:
            # Default to last 7 days
            since = (today - timedelta(days=7)).strftime('%Y-%m-%d')
            until = today.strftime('%Y-%m-%d')

        return since, until

    @staticmethod
    def extract_action_value(actions: List[Dict], action_type: str) -> float:
        """Extract specific action value from actions array"""
        if not actions:
            return 0.0

        for action in actions:
            if action.get('action_type') == action_type:
                return float(action.get('value', 0))

        return 0.0

    @staticmethod
    def extract_cost_per_action(cost_per_actions: List[Dict], action_type: str) -> float:
        """Extract specific cost per action from array"""
        if not cost_per_actions:
            return 0.0

        for cpa in cost_per_actions:
            if cpa.get('action_type') == action_type:
                return float(cpa.get('value', 0))

        return 0.0

    def get_account_overview(self, account_id: str, date_preset: str = 'last_7d') -> Dict:
        """Get aggregated overview metrics for an account"""
        try:
            insights = self.meta_client.get_account_insights(account_id, date_preset)

            # Aggregate metrics
            total_spend = 0.0
            total_impressions = 0
            total_clicks = 0
            total_conversions = 0.0
            total_revenue = 0.0
            daily_data = []

            for insight in insights:
                spend = float(insight.get('spend', 0))
                impressions = int(insight.get('impressions', 0))
                clicks = int(insight.get('clicks', 0))

                # Extract conversions (purchase events)
                actions = insight.get('actions', [])
                conversions = self.extract_action_value(actions, 'purchase')

                # Extract revenue
                action_values = insight.get('action_values', [])
                revenue = self.extract_action_value(action_values, 'purchase')

                total_spend += spend
                total_impressions += impressions
                total_clicks += clicks
                total_conversions += conversions
                total_revenue += revenue

                # Store daily data
                daily_data.append({
                    'date': insight.get('date_start'),
                    'spend': spend,
                    'impressions': impressions,
                    'clicks': clicks,
                    'conversions': conversions,
                    'revenue': revenue
                })

            # Calculate derived metrics
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
            cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
            roas = (total_revenue / total_spend) if total_spend > 0 else 0

            return {
                'spend': round(total_spend, 2),
                'impressions': total_impressions,
                'clicks': total_clicks,
                'conversions': round(total_conversions, 2),
                'revenue': round(total_revenue, 2),
                'ctr': round(ctr, 2),
                'cpc': round(cpc, 2),
                'cpa': round(cpa, 2),
                'roas': round(roas, 2),
                'daily_data': daily_data
            }

        except Exception as e:
            print(f"Error getting account overview: {e}")
            raise

    def get_campaigns_with_insights(self, account_id: str, date_preset: str = 'last_7d') -> List[Dict]:
        """Get campaigns with their performance metrics"""
        try:
            # Get campaigns
            campaigns = self.meta_client.get_campaigns(account_id)

            campaigns_with_insights = []

            for campaign in campaigns:
                campaign_id = campaign.get('id')

                try:
                    # Get insights for each campaign
                    insights = self.meta_client.get_campaign_insights(campaign_id, date_preset)

                    # Aggregate insights
                    spend = 0.0
                    impressions = 0
                    clicks = 0
                    conversions = 0.0
                    revenue = 0.0

                    for insight in insights:
                        spend += float(insight.get('spend', 0))
                        impressions += int(insight.get('impressions', 0))
                        clicks += int(insight.get('clicks', 0))

                        actions = insight.get('actions', [])
                        conversions += self.extract_action_value(actions, 'purchase')

                        action_values = insight.get('action_values', [])
                        revenue += self.extract_action_value(action_values, 'purchase')

                    # Calculate metrics
                    ctr = (clicks / impressions * 100) if impressions > 0 else 0
                    cpc = (spend / clicks) if clicks > 0 else 0
                    cpa = (spend / conversions) if conversions > 0 else 0
                    roas = (revenue / spend) if spend > 0 else 0

                    campaigns_with_insights.append({
                        'id': campaign_id,
                        'name': campaign.get('name'),
                        'status': campaign.get('status'),
                        'objective': campaign.get('objective'),
                        'spend': round(spend, 2),
                        'impressions': impressions,
                        'clicks': clicks,
                        'conversions': round(conversions, 2),
                        'revenue': round(revenue, 2),
                        'ctr': round(ctr, 2),
                        'cpc': round(cpc, 2),
                        'cpa': round(cpa, 2),
                        'roas': round(roas, 2)
                    })

                except Exception as e:
                    print(f"Error fetching insights for campaign {campaign_id}: {e}")
                    # Add campaign without insights
                    campaigns_with_insights.append({
                        'id': campaign_id,
                        'name': campaign.get('name'),
                        'status': campaign.get('status'),
                        'objective': campaign.get('objective'),
                        'spend': 0,
                        'impressions': 0,
                        'clicks': 0,
                        'conversions': 0,
                        'revenue': 0,
                        'ctr': 0,
                        'cpc': 0,
                        'cpa': 0,
                        'roas': 0
                    })

            return campaigns_with_insights

        except Exception as e:
            print(f"Error getting campaigns with insights: {e}")
            raise

    def get_campaign_detail(self, campaign_id: str, date_preset: str = 'last_7d') -> Dict:
        """Get detailed view of a campaign with adsets and ads"""
        try:
            # Get campaign insights
            campaign_insights = self.meta_client.get_campaign_insights(campaign_id, date_preset)

            # Get adsets
            adsets = self.meta_client.get_adsets(campaign_id)

            # Process adsets
            adsets_data = []
            for adset in adsets:
                adsets_data.append({
                    'id': adset.get('id'),
                    'name': adset.get('name'),
                    'status': adset.get('status'),
                    'daily_budget': adset.get('daily_budget'),
                    'lifetime_budget': adset.get('lifetime_budget')
                })

            return {
                'campaign_id': campaign_id,
                'insights': campaign_insights,
                'adsets': adsets_data
            }

        except Exception as e:
            print(f"Error getting campaign detail: {e}")
            raise

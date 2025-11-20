from typing import Dict
from app.services.meta_client import MetaClient
from app.services.analytics_service import AnalyticsService
from app.services.llm_client import LLMClient

class ChatOrchestrator:
    """Orchestrates chat interactions by fetching data and calling LLM"""

    def __init__(self, meta_client: MetaClient):
        self.meta_client = meta_client
        self.analytics_service = AnalyticsService(meta_client)
        self.llm_client = LLMClient()

    def process_message(self, account_id: str, message: str, date_preset: str = 'last_7d') -> Dict:
        """Process user message and return LLM response with data"""
        try:
            # Fetch analytics data
            # For MVP, always fetch overview and campaigns
            overview = self.analytics_service.get_account_overview(account_id, date_preset)
            campaigns = self.analytics_service.get_campaigns_with_insights(account_id, date_preset)

            # Get LLM analysis
            answer = self.llm_client.analyze_performance(overview, campaigns, message)

            return {
                'answer': answer,
                'data_used': {
                    'overview': overview,
                    'campaigns_count': len(campaigns),
                    'date_preset': date_preset
                }
            }

        except Exception as e:
            print(f"Error in chat orchestrator: {e}")
            raise

    def get_quick_insights(self, account_id: str, date_preset: str = 'last_7d') -> str:
        """Generate quick performance insights"""
        try:
            overview = self.analytics_service.get_account_overview(account_id, date_preset)
            campaigns = self.analytics_service.get_campaigns_with_insights(account_id, date_preset)

            question = "Provide a brief summary of the account performance. Highlight the most important insights and top 3 actionable recommendations."

            answer = self.llm_client.analyze_performance(overview, campaigns, question)
            return answer

        except Exception as e:
            print(f"Error generating quick insights: {e}")
            raise

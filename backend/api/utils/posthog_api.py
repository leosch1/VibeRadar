import os
from dotenv import load_dotenv
import requests
from typing import Any, Dict, Optional

load_dotenv()
API_KEY = os.getenv('POSTHOG_API_KEY')
PROJECT_ID = os.getenv('POSTHOG_PROJECT_ID')

if not API_KEY or not PROJECT_ID:
    raise RuntimeError("Please set POSTHOG_API_KEY and POSTHOG_PROJECT_ID in your .env file")

class PostHogAPI:
    """
    Client for interacting with the PostHog Insights API.

    Example:
        api = PostHogAPI()
        users = api.get_this_weeks_users()
        duration = api.get_avg_session_duration()
    """

    BASE_ENDPOINT_TEMPLATE = 'https://eu.posthog.com/api/projects/{project_id}'

    def __init__(
        self,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None
    ) -> None:
        # Load from env if not provided
        self.api_key = API_KEY
        self.base_url = base_url or self.BASE_ENDPOINT_TEMPLATE.format(project_id=PROJECT_ID)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session = session or requests.Session()

    def get_insight_result(self, insight_id: str) -> Dict[str, Any]:
        """
        Fetch the raw JSON result for a given insight ID.

        Args:
            insight_id: The ID of the insight to fetch.

        Returns:
            Parsed JSON response as a dict.
        """
        url = f"{self.base_url}/insights/{insight_id}/?refresh=force_blocking"
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_this_weeks_users(self) -> Dict[str, int]:
        """
        Get total user count for this week using a predefined insight.

        Returns:
            A dict with the key 'this-weeks-users' and the computed value.
        """
        INSIGHT_ID = "1040318"
        data = self.get_insight_result(INSIGHT_ID).get("result", [])
        total = sum(data[0].get("data", [])) if data else 0
        return {"this-weeks-users": total}

    def get_avg_session_duration(self) -> Dict[str, float]:
        """
        Calculate the average session duration (excluding zero values) using a predefined insight.

        Returns:
            A dict with the key 'session-duration' and the average value.
        """
        INSIGHT_ID = "1040925"
        result = self.get_insight_result(INSIGHT_ID).get("result", [])

        if not result:
            return {"session-duration": 0.0}

        values = result[0].get("data", [])
        non_zero = [v for v in values if v > 0]
        average = sum(values) / len(non_zero) if non_zero else 0.0
        return {"session-duration": average}
    
    def get_top_city(self) -> Dict[str, str]:
        """
        Get the top city based on user activity.

        Returns:
            A dict with the key 'top-city' and the name of the city.
        """
        # get insight ID for top city


        INSIGHT_ID = "1033313"
        data = self.get_insight_result(INSIGHT_ID).get("result", [])

        if not data:
            return {"top-city": "Unknown"}
        top_city = data[0].get("label", "Unknown").replace("::", " / ")
        return {"top-city": top_city}


if __name__ == "__main__":
    api = PostHogAPI()
    print(api.get_this_weeks_users())
    print(api.get_avg_session_duration())

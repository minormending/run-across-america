from typing import Any, Dict, List
from requests import Session, Response



class RunAcrossAmerica:
    BASE_URL: str = "https://runprod.cockpitmobile.com"

    def __init__(self, user_code: str) -> None:
        self.user_code = user_code

        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202",
            "Origin": "ionic://localhost",
            "is-virtual-client": "true",
            "ios-version": "1.0.74",
        }

        self._token: str = None
        self._user_id: str = None

    def _authenticate(self) -> Dict[str, Any]:
        url: str = f"{self.BASE_URL}/authenticate"
        headers: Dict[str, str] = {
            "content-type": "application/json",
        }
        payload: Dict[str, str] = {"email": "", "password": self.user_code}

        resp: Response = self.session.post(url, json=payload, headers=headers)
        return resp.json()

    def __setup_user_details(self) -> None:
        resp: Dict[str, Any] = self._authenticate()
        self._token = resp.get("token")
        self._user_id = resp.get("user", {}).get("id")

    def _bearer_token(self) -> str:
        if not self._token:
            self.__setup_user_details()
        return self._token

    def _get_user_id(self) -> str:
        if not self._user_id:
            self.__setup_user_details()
        return self._user_id

    def teams(self) -> List[Dict[str, Any]]:
        url: str = f"{self.BASE_URL}/users/{self._get_user_id()}/raceteams"
        resp: Response = self.session.get(url)

        j = resp.json()
        return j.get("race_teams", [])

    def goals(self, team_id: str) -> Dict[str, Any]:
        url: str = f"{self.BASE_URL}/raceteams/{team_id}/goals"
        resp: Response = self.session.get(url)

        j = resp.json()
        return j.get("team_goal")

    def members(self, team_id: str) -> List[Dict[str, Any]]:
        url: str = f"{self.BASE_URL}/raceteams/{team_id}/members?limit=1000&offset=0"
        resp: Response = self.session.get(url)
        return resp.json()

    def leaderboard(self, team_id: str) -> List[Dict[str, Any]]:
        url: str = (
            f"{self.BASE_URL}/teams/{team_id}/goalleaderboard?limit=1000&offset=0"
        )
        resp: Response = self.session.get(url)

        j = resp.json()
        return j.get("user_distances")

    def feed(self, team_id: str) -> List[Dict[str, Any]]:
        url: str = f"{self.BASE_URL}/raceteams/{team_id}/feed?limit=1000&offset=0"
        headers: Dict[str, str] = {
            "content-type": "application/json",
        }
        payload: Dict[str, str] = {
            "filters": {
                "feed_type": {
                    "plans": False,
                    "activities": True,
                    "achievements": False,
                },
                "activities": {"all": True, "description_or_selfie_only": None},
            }
        }
        resp: Response = self.session.post(url, json=payload, headers=headers)

        j = resp.json()
        return j.get("runs")

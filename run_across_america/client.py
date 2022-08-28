from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List
from requests import Session, Response

from .models import Goal, Team, Activity


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

    def teams(self) -> Iterator[Team]:
        url: str = f"{self.BASE_URL}/users/{self._get_user_id()}/raceteams"
        resp: Response = self.session.get(url)

        data = resp.json()
        for item in data.get("race_teams", []):
            inner: Dict[str, Any] = item.get("team", {})

            yield Team(
                id=inner.get("id"),
                name=inner.get("name"),
                code=inner.get("code"),
                icon=inner.get("icon"),
                created=datetime.strptime(
                    inner.get("creation_time", ""), "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                member_count=int(item.get("memberCount", "0")),
            )

    def goals(self, team_id: str) -> Goal:
        url: str = f"{self.BASE_URL}/raceteams/{team_id}/goals"
        resp: Response = self.session.get(url)

        data = resp.json().get("team_goal")
        return Goal(
            team_id=data.get("race_team_id"),
            distance=data.get("distance"),
            units=data.get("distance_units"),
            start_date=datetime.strptime(
                data.get("start_date", ""), "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            end_date=datetime.strptime(
                data.get("end_date", ""), "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
        )

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

    def feed(self, team_id: str) -> Iterator[Activity]:
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

        data = resp.json()
        for item in data.get("runs"):
            yield Activity(
                name=item.get("activity_name"),
                type=item.get("activity_type"),
                distance=float(item.get("distance_ran")),
                units=item.get("distance_units"),
                duration=timedelta(milliseconds=int(item.get("run_time"))),
                time_completed=datetime.strptime(
                    item.get("time_completed_at"), "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                user_id=item.get("user_id"),
                user_first_name=item.get("first_name"),
                user_last_name=item.get("last_name"),
                user_icon=item.get("profile_photo_link"),
            )

import argparse
from pydoc import cli
from typing import Any, Dict, List

from run_across_america import RunAcrossAmerica


def filter_team_name(haystack: List[Dict[str, Any]], needle: str) -> Dict[str, Any]:
    for item in haystack:
        name: str = item.get("team", {}).get("name", "")
        if name.lower() == needle:
            return item

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lookup info from `Run Across America`."
    )
    parser.add_argument(
        "user_code",
        help="User invitation code emailed after sign-up.",
    )

    must_specify_one = parser.add_mutually_exclusive_group()
    must_specify_one.add_argument(
        "--teams",
        action="store_true",
        help="Get all available teams for the current user.",
    )
    must_specify_one.add_argument(
        "team_name",
        nargs="?",
        help="Team name, not case sensitive.",
    )

    parser.add_argument(
        "--goals",
        action="store_true",
        help="Get the distance goal for the specified team.",
    )
    parser.add_argument(
        "--members",
        action="store_true",
        help="Get all the members of the specified team.",
    )
    parser.add_argument(
        "--leaderboard",
        action="store_true",
        help="Get all current leaderboard of the specified team.",
    )
    parser.add_argument(
        "--feed",
        action="store_true",
        help="Get the current feed of the specified team.",
    )

    args = parser.parse_args()

    client = RunAcrossAmerica(args.user_code)

    teams: List[Dict[str, Any]] = client.teams()

    if args.teams:
        for team in teams:
            print(team)
        exit(0)

    if not args.team_name:
        print("Must specify a team name!")
        exit(1)

    team_name: str = args.team_name.lower()
    
    team: Dict[str, Any] = filter_team_name(teams, team_name)
    if not team:
        print(f"Error: Unable to find team with name: {args.team_name}")
        print("Available team names are:")
        for team in teams:
            print("\t", team.get("team", {}).get("name"))
        exit(1)

    team_id: str = team.get("team", {}).get("id")

    if args.goals:
        goal: Dict[str, Any] = client.goals(team_id)
        print(goal)

    elif args.members:
        members: List[Dict[str, Any]] = client.members(team_id)
        for member in members:
            print(member)

    elif args.leaderboard:
        leaderboard: List[Dict[str, Any]] = client.leaderboard(team_id)
        for pos, member in enumerate(leaderboard):
            print(f"#{pos + 1}", member)

    elif args.feed:
        feed: List[Dict[str, Any]] = client.feed(team_id)
        for activity in feed:
            print(activity)


if __name__ == "__main__":
    main()

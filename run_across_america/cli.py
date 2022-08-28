import argparse
from typing import Any, Dict, List
from unicodedata import name

from run_across_america import RunAcrossAmerica, Team


def filter_team_name(haystack: List[Team], needle: str) -> Team:
    for team in haystack:
        if team.name.lower() == needle:
            return team


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

    teams: List[Team] = client.teams()

    if args.teams:
        for team in teams:
            print(team)
        exit(0)

    if not args.team_name:
        print("Must specify a team name!")
        exit(1)
    team_name: str = args.team_name.lower()

    team: Dict[str, Any] = next(filter(lambda t: t.name.lower() == team_name, teams))
    if not team:
        print(f"Error: Unable to find team with name: {args.team_name}")
        print("Available team names are:")
        for team in teams:
            print("\t", team.get("team", {}).get("name"))
        exit(1)

    if args.goals:
        goal: Dict[str, Any] = client.goals(team.id)
        print(goal)

    elif args.members:
        members: List[Dict[str, Any]] = client.members(team.id)
        for member in members:
            print(member)

    elif args.leaderboard:
        leaderboard: List[Dict[str, Any]] = client.leaderboard(team.id)
        for pos, member in enumerate(leaderboard):
            print(f"#{pos + 1}", member)

    elif args.feed:
        feed: List[Dict[str, Any]] = client.feed(team.id)
        for activity in feed:
            print(activity)


if __name__ == "__main__":
    main()

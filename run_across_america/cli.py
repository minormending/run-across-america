import argparse
from typing import Any, Dict, List

from run_across_america import RunAcrossAmerica, Team, Activity, Goal, Member
from run_across_america.models import MemberStats


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

    teams: List[Team] = list(client.teams())

    if args.teams:
        for team in teams:
            print(team)
        exit(0)

    if not args.team_name:
        print("Must specify a team name!")
        exit(1)
    team_name: str = args.team_name.lower()

    team: Team = next(filter(lambda t: t.name.lower() == team_name, teams))
    if not team:
        print(f"Error: Unable to find team with name: {args.team_name}")
        print("Available team names are:")
        for team in teams:
            print("\t", team.get("team", {}).get("name"))
        exit(1)

    if args.goals:
        goal: Goal = client.goals(team.id, include_progress=True)
        print(goal)

    elif args.members:
        members: List[Member] = list(client.members(team.id))
        for member in members:
            print(member)

    elif args.leaderboard:
        leaderboard: List[MemberStats] = client.leaderboard(team.id)
        for member in leaderboard:
            print(f"#{member.rank}", member)

    elif args.feed:
        feed: List[Activity] = list(client.feed(team.id))
        for activity in feed:
            print(activity)


if __name__ == "__main__":
    main()

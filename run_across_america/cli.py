import argparse
from pydoc import cli
from typing import Any, Dict, List

from run_across_america import RunAcrossAmerica


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lookup info from `Run Across America`."
    )
    parser.add_argument(
        "user_code",
        help="User invitation code emailed after sign-up.",
    )

    subparsers = parser.add_subparsers(dest="command")

    teams_parser = subparsers.add_parser(
        "teams",
        help="Get all available teams for the current user.",
    )

    team_goals_parser = subparsers.add_parser(
        "goals",
        help="Get the distance goal for the specified team.",
    )
    team_goals_parser.add_argument(
        "team_name",
        help="Team name, not case sensitive.",
    )

    members_parser = subparsers.add_parser(
        "members",
        help="Get all the members of the specified team.",
    )
    members_parser.add_argument(
        "team_name",
        help="Team name, not case sensitive.",
    )

    leaderboard_parser = subparsers.add_parser(
        "leaderboard",
        help="Get all current leaderboard of the specified team.",
    )
    leaderboard_parser.add_argument(
        "team_name",
        help="Team name, not case sensitive.",
    )

    feed_parser = subparsers.add_parser(
        "feed",
        help="Get the current feed of the specified team.",
    )
    feed_parser.add_argument(
        "team_name",
        help="Team name, not case sensitive.",
    )


    args = parser.parse_args()


    client = RunAcrossAmerica(args.user_code)


    def get_team(team_name: str) -> Dict[str, Any]:
        teams: List[Dict[str, Any]] = client.teams()

        def filter_team_name(item: Dict[str, Any], needle: str) -> bool:
            name: str = item.get("team", {}).get("name", "")
            return name.lower() == needle

        team_name: str = team_name.lower()
        team: Dict[str, Any] = next(
            filter(lambda t: filter_team_name(t, team_name), teams)
        )

        if not team:
            print(f"Error: Unable to find team with name: {args.team_name}")
            print("Available team names are:")
            for team in teams:
                print("\t", team.get("team", {}).get("name"))
            return None

        return team

    if args.command == "teams":
        teams: List[Dict[str, Any]] = client.teams()
        for team in teams:
            print(team)

    elif args.command == "goals":
        team: Dict[str, Any] = get_team(args.team_name)
        if not team:
            exit(1)

        team_id: str = team.get("team", {}).get("id")
        goal: Dict[str, Any] = client.goals(team_id)
        print(goal)

    elif args.command == "members":
        team: Dict[str, Any] = get_team(args.team_name)
        if not team:
            exit(1)

        team_id: str = team.get("team", {}).get("id")
        members: List[Dict[str, Any]] = client.members(team_id)
        for member in members:
            print(member)

    elif args.command == "leaderboard":
        team: Dict[str, Any] = get_team(args.team_name)
        if not team:
            exit(1)

        team_id: str = team.get("team", {}).get("id")
        leaderboard: List[Dict[str, Any]] = client.leaderboard(team_id)
        for pos, member in enumerate(leaderboard):
            print(f"#{pos + 1}", member)

    elif args.command == "feed":
        team: Dict[str, Any] = get_team(args.team_name)
        if not team:
            exit(1)

        team_id: str = team.get("team", {}).get("id")
        feed: List[Dict[str, Any]] = client.feed(team_id)
        for activity in feed:
            print(activity)

if __name__ == "__main__":
    main()

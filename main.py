from sys import stderr, exit
from time import sleep
from traceback import format_exc
from argparse import ArgumentParser
from prometheus_client import start_http_server, Gauge

from mattermost import MattermostClient


def fetch_data():
    # TODO - Implement data fetching
    pass


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--port",
        type=int,
        default=9060,
        help="the port to run the Prometheus exporter on",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="log whenever data is scraped",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="how often to fetch data, in seconds",
    )
    parser.add_argument(
        "--mattermost-url",
        type=str,
        default="https://not.slack.hackclub.com",
        help="base URL of the Mattermost instance to monitor",
    )
    parser.add_argument(
        "--username",
        type=str,
        help="username (or email) for Mattermost authentication",
    )
    parser.add_argument(
        "--password",
        type=str,
        help="password for Mattermost authentication",
    )
    parser.add_argument(
        "--token",
        type=str,
        help="personal access token for Mattermost (alternative to username/password)",
    )
    args = parser.parse_args()

    mattermost = MattermostClient(
        url=args.mattermost_url,
    )

    if args.token:
        user = mattermost.log_in_with_token(token=args.token)
    elif args.username and args.password:
        user = mattermost.log_in_with_credentials(
            username=args.username,
            password=args.password,
        )
    else:
        print(
            "Error: Must provide either --token, or both --username and --password",
            file=stderr,
        )
        exit(1)
    print(f"Logged in to {args.mattermost_url} as @{user['username']}", flush=True)

    start_http_server(args.port)
    print(f"Started metrics exporter: http://localhost:{args.port}/metrics", flush=True)

    has_had_success = False
    total_users = Gauge(
        "mattermost_users_total",
        "Total number of users on the Mattermost instance",
        ["hostname"],
    )

    while True:
        try:
            total = mattermost.get_total_users()
            total_users.labels(hostname=mattermost.url.hostname).set(total)
            if args.verbose:
                print(f"Fetched data: {total} total users")
            has_had_success = True
        except Exception as e:
            # Exit the program if the first fetch fails
            if not has_had_success:
                raise e
            print(f"Failed to fetch data: {format_exc()}", file=stderr, flush=True)
        finally:
            sleep(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

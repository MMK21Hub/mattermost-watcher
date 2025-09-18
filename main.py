from sys import stderr
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
        default=5,
        help="how often to fetch data, in seconds",
    )
    parser.add_argument(
        "--mattermost-url",
        type=str,
        default="https://not.slack.hackclub.com",
        help="base URL of the Mattermost instance to monitor",
    )
    parser.add_argument(
        "--mattermost-username",
        type=str,
        help="username (or email) for Mattermost authentication",
        required=True,
    )
    parser.add_argument(
        "--mattermost-password",
        type=str,
        help="password for Mattermost authentication",
        required=True,
    )
    args = parser.parse_args()

    mattermost = MattermostClient(
        username=args.mattermost_username,
        password=args.mattermost_password,
        url=args.mattermost_url,
    )
    user = mattermost.log_in()
    print(f"Logged in to {args.mattermost_url} as @{user['username']}", flush=True)

    start_http_server(args.port)
    print(f"Started metrics exporter: http://localhost:{args.port}/metrics", flush=True)

    has_had_success = False
    # TODO - Set up metrics

    while True:
        try:
            the_data = fetch_data()
            # TODO - Update metrics
            if args.verbose:
                print(f"Successfully fetched data")
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

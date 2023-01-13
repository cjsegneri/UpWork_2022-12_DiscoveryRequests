
from parse_requests import parse_requests
from group_requests import group_requests
from group_secondary_requests import group_secondary_requests
from aggregate_groups import aggregate_groups


def main():
    parse_requests()

    group_requests()

    group_secondary_requests()

    aggregate_groups()

    return 0

if __name__ == "__main__":
    main()

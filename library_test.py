import argparse
import asyncio
import logging

from aiovodafone.api import VodafoneStationApi


def get_arguments() -> tuple[argparse.ArgumentParser, argparse.Namespace]:
    """Get parsed passed in arguments."""
    parser = argparse.ArgumentParser(description="aiovodafone library test")
    parser.add_argument(
        "--router", "-r", type=str, default="192.168.1.1", help="Set router IP address"
    )
    parser.add_argument(
        "--username", "-u", type=str, default="vodafone", help="Set router username"
    )
    parser.add_argument("--password", "-p", type=str, help="Set router password")

    arguments = parser.parse_args()

    return parser, arguments


async def main() -> None:
    """Run main."""
    parser, args = get_arguments()

    if not args.password:
        print("You have to specify a password")
        exit(1)

    print("-" * 20)
    api = VodafoneStationApi(args.router, args.username, args.password)
    logged = False
    try:
        logged = await api.login()
    finally:
        if not logged:
            await api.close()
            exit(1)
    print("Logged:", logged)

    print("-" * 20)
    devices = await api.get_all_devices()
    print("Devices:", devices)
    print("-" * 20)
    data = await api.get_user_data()
    print("Data:", data)
    print("-" * 20)
    print("Logout & close session")
    await api.logout()
    await api.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("charset_normalizer").setLevel(logging.INFO)
    asyncio.run(main())
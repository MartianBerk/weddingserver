from argparse import ArgumentParser

from baked.lib.wedding.webapi import WeddingApi


if __name__ == "__main__":
    parser = ArgumentParser(description="Wedding Web API.")
    parser.add_argument("--host", type=str, required=False, help="Host")
    args = parser.parse_args()

    WeddingApi.run(standalone=True, host=args.host)

import argparse
from synchro.main import Synchro


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Synchronize packages between requirements.txt and pyproject.toml."
        )
    )

    parser.add_argument(
        "--requirements",
        type=str,
        default="requirements.txt",
        help="Path to the requirements.txt file",
    )
    parser.add_argument(
        "--pyproject",
        type=str,
        default="pyproject.toml",
        help="Path to the pyproject.toml file",
    )
    parser.add_argument(
        "--no-backup", action="store_true", help="Skip creating backup files"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run the tool without asking for user confirmation",
    )

    args = parser.parse_args()

    synchronizer = Synchro(args.requirements, args.pyproject)

    synchronizer.run()


if __name__ == "__main__":
    main()

import toml
from typing import Dict, Set
from termcolor import colored
import re


class Synchro:
    """
    A class to synchronize packages between requirements.txt and pyproject.toml files.

    Methods
    -------
    sync_packages():
        Synchronizes the packages between requirements.txt and pyproject.toml.


    Usage
    -----
    >>> from synchro.main import Synchro
    >>> sync = Synchro()
    >>> sync.run()
    
    """

    def __init__(self):
        """
        Initializes the Synchro.
        """
        self.requirements_path = "requirements.txt"
        self.pyproject_path = "pyproject.toml"

    def _colored_output(
        self,
        text: str,
        color: str = "green",
    ):
        """Colored output to the terminal."""
        print(colored(text, color))

    def _parse_pyproject(self) -> Dict[str, str]:
        """
        Parses pyproject.toml and returns a dictionary of packages and their versions.

        Returns
        -------
        Dict[str, str]
            A dictionary of packages and their versions from pyproject.toml.
        """
        with open(self.pyproject_path, "r") as file:
            pyproject_data = toml.load(file)
        return (
            pyproject_data.get("tool", {})
            .get("poetry", {})
            .get("dependencies", {})
        )

    def _parse_requirements(self) -> Dict[str, str]:
        """
        Parses requirements.txt and returns a dictionary of packages and their versions.

        Returns
        -------
        Dict[str, str]
            A dictionary of package specifications from requirements.txt.
        """
        try:
            with open(self.requirements_path, "r") as file:
                lines = file.read().splitlines()
            return {
                re.split("==|>=|<=|>|<", line)[0]: (
                    re.split("==|>=|<=|>|<", line)[1] if "==" in line else "*"
                )
                for line in lines
                if line
            }
        except Exception as error:
            self._colored_output(f"Error: {error}", "red")
            exit()

    def _parse_pyproject(self) -> Dict[str, str]:
        """
        Parses pyproject.toml and returns a dictionary of packages and their versions.

        Returns
        -------
        Dict[str, str]
            A dictionary of packages and their versions from pyproject.toml.
        """
        with open(self.pyproject_path, "r") as file:
            pyproject_data = toml.load(file)
        return (
            pyproject_data.get("tool", {})
            .get("poetry", {})
            .get("dependencies", {})
        )

    def _write_pyproject(self, packages: Dict[str, str]):
        """
        Writes the updated package list to pyproject.toml.

        Parameters
        ----------
        packages : Dict[str, str]
            The dictionary of packages and their versions to write to pyproject.toml.
        """
        with open(self.pyproject_path, "r") as file:
            pyproject_data = toml.load(file)
        pyproject_data["tool"]["poetry"]["dependencies"] = packages
        with open(self.pyproject_path, "w") as file:
            toml.dump(pyproject_data, file)

    def run(self):
        """
        Synchronizes the packages between requirements.txt and pyproject.toml.

        It ensures that both files have the same packages with the same versions.
        If a package is in one file but not the other, it adds the package.
        If a package version differs between the files, it updates the version.
        """
        reqs = self._parse_requirements()
        pyproject_packages = self._parse_pyproject()

        # Synchronize packages
        for package, version in reqs.items():
            if (
                package not in pyproject_packages
                or pyproject_packages[package] != version
            ):
                pyproject_packages[package] = version
                self._colored_output(
                    f"Updated '{package}' to version '{version}'", "green"
                )

        # Write back to pyproject.toml
        self._write_pyproject(pyproject_packages)
        self._colored_output(
            "Packages have been successfully synchronized!", "green"
        )
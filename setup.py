import os

from setuptools import find_packages, setup

with open(os.path.join("version.txt")) as version_file:
    version_from_file = version_file.read().strip()

with open("requirements.txt") as f_required:
    required = f_required.read().splitlines()

with open("test_requirements.txt") as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name="cloudshell-snmp-autoload",
    url="http://www.qualisystems.com/",
    author="QualiSystems",
    author_email="info@qualisystems.com",
    packages=find_packages(),
    install_requires=required,
    test_suite="tests",
    tests_require=required_for_tests,
    python_requires="~=3.7",
    version=version_from_file,
    description="QualiSystems SNMP Autoload Python package",
    long_description="QualiSystems SNMP Autoload Python package",
    include_package_data=True,
)

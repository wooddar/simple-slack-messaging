import sys
import os
from setuptools import setup
from setuptools.command.install import install

VERSION = "0.1.0"

class VerifyVersionCommand(install):
    """
    Custom command to verify that the git tag matches our version

    Copied with shame from the circleCI documentation

    """
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(
    name="simple-slack-messaging",
    version=VERSION,
    packages=["simple_slack", "simple_slack.blocks"],
    url="https://github.com/wooddar/simple-slack-messaging",
    license="MIT",
    author="Hugo Darwood",
    author_email="hugodarwood@gmail.com",
    description="A Package for flexibly creating and sending Slack messages",
    python_requires=">=3.5",
    install_requires=["slackclient==2.1.0"],
    keywords='slack messages block kit api',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)

"""Startup Files which stores A HandleSetup Class."""

from typing import Optional, Tuple, Union

import time
import sys
import os

from bs4 import BeautifulSoup

import requests

from Helper import Utils, NexusLogging, NexusColor, config


class HandleSetup:
    """A class responsible for handling various setup tasks for the Token Joiner tool."""

    @staticmethod
    def fetch_user_agent() -> str:
        """Fetch user agent from the remote source."""
        try:
            response = requests.get(
                "https://nexustools.de/Useragent/useragent",
                timeout=5,
            )
            soup = BeautifulSoup(
                response.text, "html.parser"
            )
            return soup.pre.get_text(strip=True)
        except requests.RequestException as e:
            print(
                f"{NexusLogging.LC} {NexusColor.RED}Failed to fetch user agent: {e}{NexusColor.RESET}"
            )
            sys.exit(
                "Error fetching user agent. Exiting..."
            )

    @staticmethod
    def show_initial_title():
        """Display the initial title with an option to skip the animation."""
        Utils.new_title(
            "Token Joiner discord.gg/V2xcBscnfD ┃ Press S to skip animation"
        )

    @staticmethod
    def setup_headers(discord, user_agent: str, xcontext: tuple = None):
        """Set up headers for the Discord instance."""
        Utils.new_title(
            "Token Joiner discord.gg/V2xcBscnfD ┃ 2.2.3"
        )
        print(
            f"{NexusLogging.LC} {NexusColor.LIGHTBLACK}Building Headers...{NexusColor.RESET}"
        )
        discord.fill_headers(token="", user_agent=user_agent, xcontext=xcontext)
        print(
            f"{NexusLogging.LC} {NexusColor.GREEN}Headers Built!{NexusColor.RESET}"
        )

    @staticmethod
    def handle_proxies(
        utils_instance,
    ) -> Tuple[bool, Optional[str]]:
        """Handle proxy usage based on user input."""
        if utils_instance.load("Input/proxies.txt") != 0:
            use_proxies = (
                input(
                    f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Proxies Found, Use them? (y/n):{NexusColor.NEXUS} "
                )
                .strip()
                .lower()
                == "y"
            )
            if use_proxies:
                print(
                    f"{NexusLogging.LC} {NexusColor.GREEN}Using Proxies{NexusColor.RESET}"
                )
                return True, None
            print(
                f"{NexusLogging.LC} {NexusColor.RED}Defaulting to no proxies.{NexusColor.RESET}"
            )

        return False, None

    @staticmethod
    def get_invite_link() -> str:
        """Get and sanitize the invite link from the user."""
        invite = input(
            f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Invite:{NexusColor.NEXUS} "
        ).strip()
        if ".gg/" in invite:
            return invite.split(".gg/")[1]
        if "invite/" in invite:
            return invite.split("invite/")[1]
        return invite

    @staticmethod
    def validate_invite(invite: str):
        """Validate the Discord invite link."""
        url = f"https://discord.com/api/v9/invites/{invite}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(
                    f"{NexusLogging.LC} {NexusColor.LIGHTBLACK}Invite -> {NexusColor.GREEN}Valid{NexusColor.RESET}"
                )
            elif response.status_code == 429:
                print(
                    f"{NexusLogging.LC} {NexusColor.RED}Rate Limited. Continuing without checking.{NexusColor.RESET}"
                )
            else:
                print(
                    f"{NexusLogging.LC} {NexusColor.LIGHTBLACK}Invite -> {NexusColor.RED}Invalid{NexusColor.RESET}"
                )
                time.sleep(2)
                sys.exit("Invalid invite. Exiting...")
        except requests.RequestException as e:
            print(
                f"{NexusLogging.LC} {NexusColor.RED}Failed to validate invite: {e}{NexusColor.RESET}"
            )
            sys.exit("Error validating invite. Exiting...")

    @staticmethod
    def get_nickname() -> Optional[str]:
        """Prompt the user for a nickname."""
        if (
            input(
                f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Change Nick? (y/n):{NexusColor.NEXUS} "
            )
            .strip()
            .lower()
            == "y"
        ):
            nickname = input(
                f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Nickname:{NexusColor.NEXUS} "
            ).strip()
            print(
                f"{NexusLogging.LC} {NexusColor.LIGHTBLACK}Nickname -> {NexusColor.GREEN}{nickname}{NexusColor.RESET}"
            )
            return nickname
        return None

    @staticmethod
    def get_delay() -> int | None:
        """Prompt the user for joining delay."""
        confirm = input(
            f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Join Delay? (y/n):{NexusColor.NEXUS} "
        ).strip().lower()
        
        if confirm == "y":
            while True:
                delay_input = input(
                    f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Delay (in seconds):{NexusColor.NEXUS} "
                ).strip()
                
                try:
                    delay = int(delay_input)
                    print(
                        f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Delay set to -> {NexusColor.GREEN}{delay}{NexusColor.RESET}"
                    )
                    return delay
                except ValueError:
                    print(
                        f"{NexusLogging.LC}{NexusColor.RED} Invalid input. Please enter a valid integer.{NexusColor.RESET}"
                    )
        return None

    @staticmethod
    def get_vcjoin() -> int:
        
        confirm = input(
            f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Join VC? (y/n):{NexusColor.NEXUS} "
        ).strip().lower()
        
        if confirm == "y":
                channel_id = input(
                    f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Channel ID:{NexusColor.NEXUS} "
                ).strip()
                
                try:
                    channel_id = int(channel_id)
                    print(
                        f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Joining VC -> {NexusColor.GREEN}{channel_id}{NexusColor.RESET}"
                    )
                    return channel_id
                except ValueError:
                    print(
                        f"{NexusLogging.LC}{NexusColor.RED} Invalid input. Please enter a valid channel id.{NexusColor.RESET}"
                    )

    @staticmethod
    def get_image() -> str:
        """
        Prompt the user to input an image URL or file path, 
        then convert the image to a Base64 string.
        """
        while True:
            choice = input(
                f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Enter image source - URL (u) or Path (p): {NexusColor.NEXUS}"
            ).strip().lower()

            if choice == "u":
                image_url = input(
                    f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Enter Image URL: {NexusColor.NEXUS}"
                ).strip()
                
                if not image_url.startswith(("http://", "https://")):
                    print(
                        f"{NexusLogging.LC}{NexusColor.RED} Invalid URL. Please provide a valid URL.{NexusColor.RESET}"
                    )
                    continue

                try:
                    path = Utils.download_image(url=image_url)
                    return Utils.image_to_base64(image_path=path)
                except Exception as e:
                    print(
                        f"{NexusLogging.LC}{NexusColor.RED} Error: {e}{NexusColor.RESET}"
                    )

            elif choice == "p":
                image_path = input(
                    f"{NexusLogging.LC}{NexusColor.LIGHTBLACK} Enter Image Path (Drag & Drop): {NexusColor.NEXUS}"
                ).strip()

                if not os.path.isfile(image_path):
                    print(
                        f"{NexusLogging.LC}{NexusColor.RED} Invalid file path. Please provide a valid path.{NexusColor.RESET}"
                    )
                    continue

                try:
                    return Utils.image_to_base64(image_path=image_path)
                except Exception as e:
                    print(
                        f"{NexusLogging.LC}{NexusColor.RED} Error: {e}{NexusColor.RESET}"
                    )

            else:
                print(
                    f"{NexusLogging.LC}{NexusColor.RED} Invalid input. Please type 'u' for URL or 'p' for Path.{NexusColor.RESET}"
                )

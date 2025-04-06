"""Python file for mass adding Profile Pictures. to tokens."""

import sys
import os
import threading

import tls_client

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from Helper import (
    NexusColor,
    NexusLogging,
    Utils,
    HandleSetup,
    Discord,
    intro,
    fetch_session,
    pink_gradient,
)


class PFPChanger:
    """Class For changing Profile Pictures."""

    def __init__(
        self,
        image: str,
        useragent: str,
        proxy: str | None = None,
    ) -> None:
        """Initializes the PFPChanger class."""
        self.useragent: str = useragent
        self.image: str = image

        self.discord = Discord
        self.session = tls_client.Session(
            random_tls_extension_order=True,
            client_identifier=Discord.extract_version(
                user_agent=self.useragent
            ),
        )

        self.succses: int = 0
        self.failed: int = 0

        if proxy:
            self.session.proxies.update(
                {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}",
                }
            )

    def change_pfp(self, token: str) -> None:
        """Function To change The Profile Picture From a token

        Args:
            token (str): Token to change the Profile Pictures.
        """
        fetch_session(token)
        response = self.session.patch(
            "https://discord.com/api/v9/users/@me",
            headers=self.discord.fill_headers(
                token, self.useragent
            ),
            json={
                "avatar": f"data:image/jpeg;base64,{self.image}"
            },
        )

        if response.status_code == 200:
            self.succses += 1
            NexusLogging.print_status(
                token=token,
                message="PFP Changed",
                color=NexusColor.GREEN,
            )
            return

        if response.status_code == 429:
            self.failed += 1
            NexusLogging.print_status(
                token=token,
                message="Ratelimit (429)",
                color=NexusColor.RED,
            )
            return

        self.failed += 1
        NexusLogging.print_error(
            token=token, message="Error", response=response
        )
        return

    def print_summary(self):
        """Print a summary of the join operation."""
        print(
            f"{NexusLogging.LC} {NexusColor.LIGHTBLACK}"
            f"Succses: {NexusColor.GREEN}{self.succses}{NexusColor.LIGHTBLACK} "
            f"| Failed: {NexusColor.RED}{self.failed}{NexusColor.LIGHTBLACK} "
            f"| Total: {pink_gradient[2]}{self.succses + self.failed}{NexusColor.RESET}"
        )
        input()


def mass_change_pfp() -> None:
    """Function To mass change Profile Pictures."""
    utils = Utils()
    discord = Discord()

    utils.clear()
    utils.new_title(
        "PFP Changer discord.gg/nexustools ┃ 1.0.0"
    )

    useragent = HandleSetup.fetch_user_agent()

    intro()

    HandleSetup.setup_headers(discord, useragent)

    use_proxies, proxy = HandleSetup.handle_proxies(utils)

    image_base64 = HandleSetup.get_image()

    if use_proxies:
        proxy = utils.get_formatted_proxy(
            "Input/proxies.txt"
        )

    pfpchanger = PFPChanger(
        image=image_base64, useragent=useragent, proxy=proxy
    )

    threads = []
    for token in utils.get_tokens(formatting=True):

        thread = threading.Thread(
            target=pfpchanger.change_pfp, args=(token,)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    pfpchanger.print_summary()


if __name__ == "__main__":
    mass_change_pfp()

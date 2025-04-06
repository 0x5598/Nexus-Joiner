"""Python File for Bypassing Rules."""

from typing import Dict, Union

import tls_client

from Helper.Utils.logging import NexusLogging
from Helper.NexusColors.color import NexusColor

class BypassRules:
    """Class for Onboarding Bypass."""

    def __init__(
        self, token: str, guild_id: int,
    ) -> None:
        """Initializes the BypassRules class."""
        self.session = tls_client.Session(
            random_tls_extension_order=True,
            client_identifier="chrome_120",
        )
        self.token: str = token
        self.guild_id: int = guild_id
        self.headers: Dict[str, str] = {
            "authorization": self.token
        }

    def get_data(self) -> Union[tuple[str, list], None]:
        """Fetches rules data."""

        response = self.session.get(
            f"https://discord.com/api/v9/guilds/{self.guild_id}/member-verification?with_guild=false&invite_code=",
            headers=self.headers,
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("version"), data.get(
                "form_fields"
            )

        NexusLogging.print_error(
            token=self.token,
            message="Error",
            response=response
        )
        return None

    def bypass_rules(self) -> None:
        """Main function to bypass rules."""
        version, form_fields = self.get_data()

        response = self.session.put(
            f"https://discord.com/api/v9/guilds/{self.guild_id}/requests/@me",
            headers=self.headers,
            json={
                "version": version,
                "form_fields": form_fields,
            },
        )

        if response.status_code == 201:
            NexusLogging.print_status(
                token=self.token,
                message="Bypassed Rules",
                color=NexusColor.GREEN
            )
        else:
            NexusLogging.print_error(
                token=self.token,
                message="Error",
                response=response
            )

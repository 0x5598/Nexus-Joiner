"""Python File for Bypassing Onboarding."""

from typing import Dict, Tuple, Union
import time
import random

import tls_client

from Helper.Utils.logging import NexusLogging
from Helper.NexusColors.color import NexusColor

class OnboardingBypass:
    """Class for Onboarding Bypass."""

    def __init__(self, token: str, guildid: int) -> None:
        """Initializes the OnboardingBypass class."""
        self.session = tls_client.Session(
            random_tls_extension_order=True,
            client_identifier="chrome_120"
        )
        self.token: str = token
        self.guildid: int = guildid
        self.headers: Dict[str, str] = {
            "authorization": self.token
        }

    def fetch_onboarding_data(
        self,
    ) -> Union[Dict[str, Tuple[str, int, bool]], None]:
        """Fetches onboarding data."""
        response = self.session.get(
            f"https://discord.com/api/v9/guilds/{self.guildid}/onboarding",
            headers=self.headers,
        )

        if response.status_code == 200:
            return response.json()

        NexusLogging.print_error(
            token=self.token,
            message="Error",
            response=response
        )
        return None

    def bypass_onboarding(self) -> None:
        """Main function to bypass onboarding."""
        onboarding_data = self.fetch_onboarding_data()
        if not onboarding_data:
            return

        prompts = onboarding_data.get("prompts", [])
        responses = []
        prompts_seen = {}
        responses_seen = {}
        current_time = int(time.time() * 1000)

        for prompt in prompts:
            prompt_id = prompt.get("id")
            prompts_seen[prompt_id] = current_time

            options = prompt.get("options", [])
            for option in options:
                option_id = option.get("id")
                responses_seen[option_id] = current_time

            if prompt.get("single_select"):
                if prompt.get("required", False) or random.choice([True, False]):
                    selected_option = random.choice(options) if options else None
                    if selected_option:
                        responses.append(selected_option["id"])
            else:
                if not prompt.get("required", False):
                    selected_options = random.sample(
                        options,
                        k=random.randint(0, len(options))
                    )
                    for option in selected_options:
                        responses.append(option["id"])
                else:
                    for option in options:
                        responses.append(option["id"])

        if not responses:
            print("No valid responses constructed for onboarding.")
            return

        response = self.session.post(
            f"https://discord.com/api/v9/guilds/{self.guildid}/onboarding-responses",
            json={
            "onboarding_responses": responses,
            "onboarding_prompts_seen": prompts_seen,
            "onboarding_responses_seen": responses_seen,
        },
            headers=self.headers,
        )

        if response.status_code == 200:
            NexusLogging.print_status(
                token=self.token,
                message="Onboarding Bypassed",
                color=NexusColor.GREEN
            )
        else:
            error_message = response.json()
            NexusLogging.print_error(
                token=self.token,
                message=f"Error: {error_message}",
                response=response
            )

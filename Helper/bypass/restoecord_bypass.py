"""python file which Contains a class To bypass Restorecord"""
from Helper.Utils.logging import NexusLogging
from Helper.NexusColors.color import NexusColor
from Helper.Utils.utils import config


class RestoreCordBypass:
    """Class for Restorecord Bypass"""
    def __init__(
        self,
        token: str,
        guild_id: int,
        client_id: int,
        cfsession,
        proxy: str,
    ):
        """Initializes the RestoreCordBypass class."""
        self.session = cfsession
        self.token: str = token
        self.guild_id: int = guild_id
        self.client_id: int = client_id
        self.proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }

    def bypass(self) -> None:
        """Function To Bypass Restorecord"""
        response = self.session.post(
            "https://discord.com/api/v9/oauth2/authorize",
            params={
                "client_id": self.client_id,
                "response_type": "code",
                "redirect_uri": "https://restorecord.com/api/callback",
                "scope": "identify guilds.join",
                "state": self.guild_id,
            },
            json={"permissions": "0", "authorize": True},
            headers={"authorization": self.token},
            proxies=self.proxies,
        )

        try:
            data = response.json()
            if "location" not in data:
                NexusLogging.print_error(
                    token=self.token,
                    message="Missing 'location' in response data",
                    response=response,
                )
                return False

            answer = data["location"]
            captcha_encounters = 0

            for attempt in range(5):
                attempt_response = self.session.get(
                    answer,
                    allow_redirects=True,
                    proxies=self.proxies,
                )

                if attempt_response.status_code in [307, 200]:
                    NexusLogging.print_status(
                        token=self.token,
                        message="Restorecord Bypassed",
                        color=NexusColor.GREEN,
                    )
                    return True

                if (
                    attempt_response.status_code == 403
                    and "Please complete the captcha to continue"
                    in attempt_response.text
                ):
                    captcha_encounters += 1
                    if config.get("debug"):
                        NexusLogging.print_status(
                            token=self.token,
                            message="Error encountered while attempting to detect Restorecord: Cloudflare",
                            color=NexusColor.RED,
                        )
                    continue

                NexusLogging.print_error(
                    token=self.token,
                    message=f"Unexpected status code {attempt_response.status_code} on attempt {attempt + 1}",
                    response=attempt_response,
                )
                return False

            if captcha_encounters == 5:
                NexusLogging.print_status(
                    token=self.token,
                    message="Error encountered while attempting to detect Restorecord: Cloudflare",
                    color=NexusColor.RED,
                )
                return False

        except Exception as e:
            NexusLogging.print_status(
                token=self.token,
                message=f"Error: {e}",
                color=NexusColor.RED,
            )
            return False

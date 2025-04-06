"Main File to handle Joining and more."

import threading
import time

import tls_client
import cloudscraper
import subprocess

from Helper import (
    Discord,
    Hsolver,
    Utils,
    config,
    fetch_session,
    intro,
    pink_gradient,
    NexusLogging,
    DetectBypass,
    OnboardingBypass,
    BypassRules,
    RestoreCordBypass,
    NexusColor,
    HandleSetup
)


class NexusTokenJoiner:
    """Handles Discord token joining and nickname changing."""

    def __init__(
        self, nickname: str, _proxy: bool, useragent: str
    ) -> None:
        """
        Initializes the NexusTokenJoiner instance.

        Args:
            nickname (str): The nickname to set for the user.
            _proxy (bool): Whether to use proxies for requests.
            useragent (str): The User-Agent string for HTTP headers.
        """
        self.discord: callable = Discord()
        self.hsolver: callable = Hsolver()
        self.utils: callable = Utils()

        self.solver: bool = True
        self._proxy: bool = _proxy

        self.joined: list[str] = []
        self.failed: int = 0

        self.nickname: str = nickname
        self.useragent: str = useragent
        
        self.restorecord_detected = False
        self.client_id = None
        
        self.guild_id = None
        self.session_id: str = None

        self.lock = threading.Lock()

    def change_nick(
        self, guild_id: int, nick: str, token: str
    ) -> None:
        """
        Changes the nickname of a user in a specified Discord guild.

        Args:
            guild_id (int): The ID of the guild where the nickname is to be changed.
            nick (str): The new nickname to set.
            token (str): The Discord token for authentication.
        """
        headers = self.discord.fill_headers(
            token, self.useragent
        )
        session = tls_client.Session(
            random_tls_extension_order=True,
            client_identifier=Discord.extract_version(
                user_agent=self.useragent
            )
        )
        session.headers.update(headers)
        session.cookies.update(
            self.discord.get_cookies(session)
        )

        response = session.patch(
            f"https://discord.com/api/v9/guilds/{guild_id}/members/@me",
            json={"nick": nick},
        )

        if config["debug"]:
            print(f"{NexusColor.LIGHTBLACK}{response.text}")

        if response.status_code == 200:
            NexusLogging.print_status(
                token, "Nickname Changed", NexusColor.GREEN
            )
        elif response.status_code == 429:
            NexusLogging.print_status(
                token, "Ratelimit", NexusColor.RED
            )
        else:
            NexusLogging.print_error(
                token,
                "Error while changing Nickname",
                response,
            )

    def accept_invite(
        self, invite: str, token: str, proxy: str = None
    ) -> None:
        """
        Accepts a Discord server invite and optionally changes the user's nickname.

        Args:
            invite (str): The server invite code.
            token (str): The Discord token for authentication.
            proxy (str, optional): Proxy to use for the request. Defaults to None.
        """
        session = tls_client.Session(
            random_tls_extension_order=True,
            client_identifier=Discord.extract_version(
                user_agent=self.useragent
            )
        )
        try:
            session_id = fetch_session(token)
            if session_id == "Invalid token":
                NexusLogging.print_status(
                    token, "Invalid", NexusColor.RED
                )
                return

            if session_id == "429":
                NexusLogging.print_status(
                    token,
                    "Cant Fetch Session -> 429",
                    NexusColor.RED,
                )
                return

            self.session_id = session_id
            payload = {"session_id": self.session_id}
            session.cookies.update(
                self.discord.get_cookies(session)
            )

            if self._proxy:
                session.proxies.update(
                    {"https": f"http://{proxy}"}
                )

            response = session.post(
                f"https://discord.com/api/v9/invites/{invite}",
                json=payload,
                headers=self.discord.fill_headers(
                    token, self.useragent
                ),
            )

            if config["debug"]:
                print(f"{NexusColor.LIGHTBLACK}session_id={self.session_id}")
                print(f"{NexusColor.LIGHTBLACK}useragent={self.useragent}...")
                print(f"{NexusColor.LIGHTBLACK}headers={response.headers}")

            if response.status_code == 200:
                self._handle_successful_invite(
                    token, response, self.nickname, proxy
                )
            elif response.status_code == 429:
                NexusLogging.print_status(
                    token, "Ratelimit", NexusColor.RED
                )
                with self.lock:
                    self.failed += 1
            elif (
                response.status_code == 401
                and response.json()["message"]
                == "401: Unauthorized"
            ):
                NexusLogging.print_status(
                    token, "Invalid", NexusColor.RED
                )
                with self.lock:
                    self.failed += 1
            elif (
                "You need to verify your account"
                in response.text
            ):
                NexusLogging.print_status(
                    token, "Locked", NexusColor.RED
                )
                with self.lock:
                    self.failed += 1
            elif "captcha_rqdata" in response.text:
                self._handle_captcha(
                    token,
                    response,
                    invite,
                    session,
                    proxy,
                )
            else:
                NexusLogging.print_error(
                    token, "Error while joining", response
                )
                
        except TimeoutError:
            NexusLogging.print_status(token, "Timeout", NexusColor.RED)
            with self.lock:
                self.failed += 1
        except KeyError as e:
            NexusLogging.print_status(token, f"Key Error: {e}", NexusColor.RED)
            with self.lock:
                self.failed += 1
        except Exception as e:
            NexusLogging.print_status(token, f"Error: {e}", NexusColor.RED)
            with self.lock:
                self.failed += 1

    def _handle_successful_invite(
        self, token, response, nickname, proxy
    ):
        """
        Handles the logic for a successful server join.

        Args:
            token (str): The Discord token used for the request.
            response (requests.Response): The response object from the server.
            nickname (str): The nickname to set, if any.
        """
        with self.lock:
            self.joined.append(token)
        NexusLogging.print_status(
            token, "Joined", NexusColor.GREEN
        )
        self.guild_id = response.json()["guild"]["id"]

        cfsess = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "windows",
                "desktop": True,
                "mobile": False,
            }
        )
        detect = DetectBypass(token=token, guildid=self.guild_id, proxy=proxy, cfsession=cfsess)
        
        if nickname:
            self.change_nick(
                guild_id=self.guild_id,
                nick=nickname,
                token=token
            )

        if detect.check_onboarding():
            NexusLogging.print_status(
                token=token,
                message="Detected Onboarding",
                color=NexusColor.LIGHTBLUE,
            )
            OnboardingBypass(
                token=token, guildid=self.guild_id
            ).bypass_onboarding()

        if detect.check_rules():
            NexusLogging.print_status(
                token=token,
                message="Detected Rules",
                color=NexusColor.LIGHTBLUE,
            )
            BypassRules(
                token=token, guild_id=self.guild_id
            ).bypass_rules()
        
        if proxy and config["restorecord_bypass"]:
            if not self.restorecord_detected:
                client_id = detect.check_restorecord()
                if client_id:
                    self.restorecord_detected = True
                    self.client_id = client_id
                else:
                    self.restorecord_detected = True  

            if self.client_id:
                NexusLogging.print_status(
                    token=token,
                    message="Detected Restorecord",
                    color=NexusColor.LIGHTBLUE,
                )
                RestoreCordBypass(
                    token=token,
                    guild_id=self.guild_id,
                    client_id=self.client_id,
                    proxy=proxy,
                    cfsession=cfsess
                ).bypass()

                    
            

    def _handle_captcha(
        self, token, response, invite, session, proxy_
    ):
        """
        Handles captcha challenges during the server joining process.

        Args:
            token (str): The Discord token used for the request.
            response (requests.Response): The response object from the server.
            invite (str): The server invite code.
            session (tls_client.Session): The current TLS session.
            proxy_ (str): Proxy used for the request.
        """
        NexusLogging.print_status(
            token=token,
            message="Hcaptcha",
            color=NexusColor.RED
        )
        if (
            config["captcha_api_key"]
            != "YOUR-CSOLVER-KEY | csolver.xyz" 
            and
            config["captcha_solving"]
        ):
            self._solve_captcha(
                token,
                response,
                invite,
                session,
                proxy_,
            )
        else:
            with self.lock:
                self.failed += 1

    def _solve_captcha(
        self, token, response, invite, session, proxy_
    ):
        """
        Attempts to solve a captcha challenge using an external service.

        Args:
            token (str): The Discord token used for the request.
            response (requests.Response): The response object from the server.
            invite (str): The server invite code.
            session (tls_client.Session): The current TLS session.
            proxy_ (str): Proxy used for the request.
        """
        if self.solver:
            NexusLogging.print_status(
                token=token[:45],
                message="Solving Captcha..",
                color=NexusColor.GREEN
            )
            site_key = response.json()["captcha_sitekey"]
            rqdata = response.json()["captcha_rqdata"]
            rqtoken = response.json()["captcha_rqtoken"]

            try:
                start_time = time.time()
                solution = self.hsolver.get_captcha_key(
                    rqdata=rqdata,
                    site_key=site_key,
                    website_url="https://discord.com/channels/@me",
                    proxy=proxy_,
                    api_key=config["captcha_api_key"],
                )
                if solution:
                    end_time = time.time()
                    NexusLogging.print_status(
                        token=solution,
                        message=f"{NexusColor.GREEN}Solved in {NexusColor.RESET}{end_time - start_time:.2f}s",
                        color=NexusColor.GREEN,
                        length=60
                    )
                    headers = self.discord.fill_headers(
                        token=token, 
                        user_agent=self.useragent,
                        xcaptcha=solution,
                        rqtoken=rqtoken
                    )
                   
                    response = session.post(
                        f"https://discord.com/api/v9/invites/{invite}",
                        json={
                            "session_id": self.session_id
                        },
                        headers=headers
                    )
                    

                    if response.status_code == 200:
                        with self.lock:
                            self.joined.append(token)
                        NexusLogging.print_status(
                            token,
                            "Joined",
                            NexusColor.GREEN,
                        )
                        if self.nickname:
                            guild_id = response.json()[
                                "guild"
                            ]["id"]
                            self.change_nick(
                                guild_id,
                                self.nickname,
                                token,
                            )
                    else:
                        NexusLogging.print_error(
                            token,
                            "Error while joining",
                            response,
                        )
                        with self.lock:
                            self.failed += 1
                else:
                    with self.lock:
                        self.failed += 1
            except (
                ConnectionError,
                TimeoutError,
            ) as conn_error:
                print(
                    f"Connection error occurred: {conn_error}"
                )
                with self.lock:
                    self.failed += 1
            except ValueError as val_error:
                print(
                    f"Value error in response: {val_error}"
                )
                with self.lock:
                    self.failed += 1
            except KeyError as key_error:
                print(
                    f"Key error when accessing response data: {key_error}"
                )
                with self.lock:
                    self.failed += 1
        else:
            with self.lock:
                self.failed += 1

def run_joiner(utils: Utils, invite: str, nickname: str | None, use_proxies: bool, proxy: str | None, useragent: str, delay: int | None, channel_id: int | None):
    """Run the token joiner with the given configuration."""
    threads = []
    nexus = NexusTokenJoiner(nickname=nickname, _proxy=use_proxies, useragent=useragent)
        
    for token in utils.get_tokens(formatting=True):
        if use_proxies:
            proxy = utils.get_formatted_proxy("Input/proxies.txt")
        thread = threading.Thread(target=nexus.accept_invite, args=(invite, token, proxy))
        threads.append(thread)
        thread.start()
        if delay:
            time.sleep(delay)

    for thread in threads:
        thread.join()

    save_results(invite, nexus)
    
    if channel_id:
        subprocess.Popen(
            ['python', "External/vcjoiner.py", nexus.guild_id, str(channel_id)],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        
    print_summary(nexus)


def save_results(invite: str, nexus: NexusTokenJoiner):
    """Save joined tokens to a file."""
    with open(f"Output/joined_{invite}.txt", "w", encoding="utf-8") as f:
        for token in nexus.joined:
            f.write(token + "\n")


def print_summary(nexus: NexusTokenJoiner):
    """Print a summary of the join operation."""
    print(
        f"{NexusLogging.LC} {NexusColor.LIGHTBLACK}Joined: {NexusColor.GREEN}{len(nexus.joined)}{NexusColor.LIGHTBLACK} "
        f"| Failed: {NexusColor.RED}{nexus.failed}{NexusColor.LIGHTBLACK} "
        f"| Total: {pink_gradient[2]}{len(nexus.joined) + nexus.failed}{NexusColor.RESET}"
    )
    input()

def main() -> None:
    """Main function to run the token joiner."""
    utils = Utils()
    discord = Discord()
    xcontext = None
    utils.clear()
    HandleSetup.show_initial_title()

    useragent = HandleSetup.fetch_user_agent()

    intro()

    use_proxies, proxy = HandleSetup.handle_proxies(utils)

    invite = HandleSetup.get_invite_link()
    
    HandleSetup.validate_invite(invite)
    
    location, guild_id, channel_id, type = utils.get_xcontext_values(invite=invite, token=utils.get_random_token())
    if guild_id:
        xcontext=(location, guild_id, channel_id, type)
        
    HandleSetup.setup_headers(
        discord=discord,
        user_agent=useragent,
        xcontext=xcontext)

    nickname = HandleSetup.get_nickname()
    
    delay = HandleSetup.get_delay()

    channel_id = HandleSetup.get_vcjoin()
    
    run_joiner(utils, invite, nickname, use_proxies, proxy, useragent, delay, channel_id)

if __name__ == "__main__":
    main()



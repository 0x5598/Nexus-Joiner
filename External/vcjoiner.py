"""vcjoiner.py File for the Discord Vc Joiner"""
import json
import sys
import os
import threading

import asyncio
import websockets

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from Helper import (
    NexusColor,
    NexusLogging,
    pink_gradient,
    Utils
)

class DiscordVCJoiner:
    """
    A class to handle joining Discord voice channels programmatically via the Discord Gateway.
    """
    def __init__(self, token: str, guild_id: int, channel_id: int) -> None:
        """
        Initialize the DiscordVCJoiner.
        """
        self.token: str = token
        self.guild_id: int = guild_id
        self.channel_id: int = channel_id

        self.heartbeat_interval: int = None
        self.session_id: str = None
        self.voice_server_info: dict = None
        self.websocket = None

    async def connect_to_gateway(self) -> None:
        """
        Establish a WebSocket connection to the Discord Gateway.
        """
        async with websockets.connect("wss://gateway.discord.gg/?v=9&encoding=json") as ws:
            self.websocket = ws
            await self.identify()
            await self.event_listener()

    async def identify(self) -> None:
        """
        Send the IDENTIFY payload to the Discord Gateway to authenticate the client.
        """
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": 513, 
                "properties": {
                    "$os": "linux",
                    "$browser": "disco",
                    "$device": "disco"
                }
            }
        }
        await self.send_json(payload)

    async def heartbeat(self) -> None:
        """
        Start sending periodic heartbeats to keep the WebSocket connection alive.
        """
        while self.heartbeat_interval:
            await asyncio.sleep(self.heartbeat_interval / 1000)
            await self.send_json({"op": 1, "d": None})

    async def join_vc(self) -> None:
        """
        Send the payload to join a voice channel.
        """
        payload = {
            "op": 4,
            "d": {
                "guild_id": str(self.guild_id),
                "channel_id": str(self.channel_id),
                "self_mute": False,
                "self_deaf": False
            }
        }
        await self.send_json(payload)

    async def event_listener(self) -> None:
        """
        Listen for and handle events from the Discord Gateway.
        """
        try:
            async for message in self.websocket:
                event = json.loads(message)

                if event["op"] == 10:
                    self.heartbeat_interval = event["d"]["heartbeat_interval"]
                    asyncio.create_task(self.heartbeat())

                elif event["op"] == 0 and event["t"] == "READY":
                    self.session_id = event["d"]["session_id"]
                    await self.join_vc()

                elif event["op"] == 0 and event["t"] == "VOICE_SERVER_UPDATE":
                    self.voice_server_info = event["d"]
                    NexusLogging.print_status(
                        token=self.token,
                        message="Joined VC",
                        color=NexusColor.GREEN,
                        prefix=f"        {NexusLogging.LC} "
                    )
        except Exception as e:
            NexusLogging.print_status(
                token=self.token,
                message=f"Error: {str(e)}",
                color=NexusColor.RED,
                prefix=f"        {NexusLogging.LC} "
            )

    async def send_json(self, data: dict) -> None:
        """
        Send a JSON payload over the WebSocket.

        Args:
            data (dict): The JSON data to send.
        """
        await self.websocket.send(json.dumps(data))

    @staticmethod
    def run_join_vc(token: str, guild_id: int, channel_id: int) -> None:
        """
        Run the DiscordVCJoiner to join a voice channel.

        Args:
            token (str): The user's Discord token.
            guild_id (int): The guild (server) ID.
            channel_id (int): The voice channel ID.
        """
        asyncio.run(DiscordVCJoiner(
            token=token,
            guild_id=guild_id,
            channel_id=channel_id
        ).connect_to_gateway())


def main() -> None:
    """
    Main entry point for the script. Initializes the tool and starts joining voice channels.
    """
    Utils.change_window_size(width=92, height=20)
    Utils.new_title("Nexus Joiner V2 │ VC Joiner")

    sys.stdout.write(
        fr'''
{pink_gradient[0]}            _   __                        ______            __
{pink_gradient[1]}           / | / /__  _  ____  _______   /_  __/___  ____  / /____    
{pink_gradient[2]}          /  |/ / _ \| |/_/ / / / ___/    / / / __ \/ __ \/ / ___/    __
{pink_gradient[3]}         / /|  /  __/>  </ /_/ (__  )    / / / /_/ / /_/ / (__  )     .-'--`-._
{pink_gradient[0]}        /_/ |_/\___/_/|_|\__,_/____/    /_/  \____/\____/_/____/      '-O---O--' 
''')
    print("")
    threads = []

    for token in Utils.get_tokens(formatting=True):
        thread = threading.Thread(
            target=DiscordVCJoiner.run_join_vc,
            args=(token, sys.argv[1], sys.argv[2])
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
import re

import pyfiglet

from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class FigletBotHandler:

    META = {
        "name": "FIGLet",
        "description": "Render any message using FIGlet. Power by pyfiglet.",
    }

    def usage(self) -> str:
        return """
            This plugin allows a user to render a message using FIGlet.
            Users should preface the command with "@mention-bot".

            There are several commands to use this bot:
            - @mention-bot --list -> List all available fonts
            - @mention-bot <message> -> Render <message> using default font
            - @mention-bot --font <font> <message> -> Render <message> using <font>
            """

    def handle_message(self, message: Dict[str, str], bot_handler: Any) -> None:
        quoted_name = bot_handler.identity().mention
        content = message["content"].strip()
        try:
            if content.startswith("--list"):
                _, *param = content.split(" ", 1)
                if len(param) > 0:
                    regex = re.compile("^{}$".format(param[0].replace("*", ".*")))
                else:
                    regex = re.compile("^.*$")
                fonts = pyfiglet.FigletFont.getFonts()
                bot_handler.send_reply(
                    message, ", ".join(f for f in fonts if regex.match(f) is not None)
                )
            elif content.startswith("--font"):
                _, font, content = content.split(" ", 2)
            else:
                font = "standard"

            response = "```\n" + pyfiglet.figlet_format(content, font) + "```\n"
            bot_handler.send_reply(message, response)
        except pyfiglet.FontNotFound as font:
            bot_handler.send_reply(
                message, "Sorry, I don't know have a font name '{}'".format(font)
            )


handler_class = FigletBotHandler

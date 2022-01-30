import os

import dotenv
import hikari
import lightbulb 

dotenv.load_dotenv()

bot = lightbulb.BotApp(
  os.environ["BOT_TOKEN"],
  prefix="!",
  banner=None,
  intents=hikari.Intents.ALL,
  default_enabled_guilds=(902692574601543700,)
)

@bot.command
@lightbulb.command("ping", description="The bot's ping")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
  await ctx.respond("Pong!")

bot.load_extensions("extensions.info", "extensions.weather")

if __name__ == "__main__":
  if os.name != "nt":
    import uvloop

    uvloop.install()

  bot.run()
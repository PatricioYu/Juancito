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
@lightbulb.command("ping", description='The bot says "Pong!"')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
  await ctx.respond("Pong!")

bot.load_extensions("extensions.info", "extensions.weather", "extensions.mod")
# Error handler
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
  if isinstance(event.exception, lightbulb.CommandInvocationError):
    await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.")
    raise event.exception

  exception = event.exception.__cause__ or event.exception

  # Error due to not being the owner of the bot.
  if isinstance(exception, lightbulb.NotOwner):
    await event.context.respond("You are not the owner of this bot.")
  # Error raised due to cooldown timer not finished.
  elif isinstance(exception, lightbulb.CommandIsOnCooldown):
    await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.")
  # Error raised due to the lack of required options.
  elif isinstance(exception, lightbulb.NotEnoughArguments):
    await event.context.respond("Not enough arguments")
  # Error raised due to non existent command used.
  elif isinstance(exception, lightbulb.CommandNotFound):
    await event.context.respond("That command doesn't exist")
  
  else:
    raise exception

if __name__ == "__main__":
  if os.name != "nt":
    import uvloop

    uvloop.install()

  bot.run()
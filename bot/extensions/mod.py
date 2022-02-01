import asyncio

import hikari
import lightbulb

mod_plugin = lightbulb.Plugin("Mod")

@mod_plugin.command
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)
@lightbulb.option(
  "messages", 
  "amount of messages to delete", 
  type=int, 
  required=True
)
@lightbulb.command(
  "purge", "Deletes the amount of messages the mod indicates", aliases=["clear"]
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def purge_messages(ctx: lightbulb.Context) -> None:
  num_msgs = ctx.options.messages
  channel = ctx.channel_id

  if isinstance(ctx, lightbulb.PrefixContext):
    await ctx.event.message.delete()

  msgs = await ctx.bot.rest.fetch_messages(channel).limit(num_msgs)
  await ctx.bot.rest.delete_messages(channel, msgs)

  resp = await ctx.respond(f"{len(msgs)} messages deleted")

  await asyncio.sleep(5)
  await resp.delete()

def load(bot: lightbulb.BotApp) -> None:
  bot.add_plugin(mod_plugin)
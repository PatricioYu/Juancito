import lightbulb
import python_weather

weather_plugin = lightbulb.Plugin("Weather")

@weather_plugin.command
@lightbulb.option(
  "location",
  "Gets the location to show its weather.",
  modifier=lightbulb.commands.OptionModifier.CONSUME_REST,
  type=str,
  required=True
)
@lightbulb.command(
  "weather", "Gets the weather from a specific location the user inputs.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)

async def weather(ctx: lightbulb.Context) -> None:
  client = python_weather.Client(format=python_weather.METRIC)

  weather = await client.find(ctx.options.location)

  if weather.current.temperature >= 30:
    response = ":man_mage: The weather in " + ctx.options.location + " is " + str(weather.current.temperature) + "° 🥵"
  
  elif weather.current.temperature <= 10:
    response = ":man_mage: The weather in " + ctx.options.location + " is " + str(weather.current.temperature) + "° 🥶"

  else: 
    response = ":man_mage: The weather in " + ctx.options.location + " is " + str(weather.current.temperature) + "° 😎"

  await ctx.respond(response)

  await client.close()

def load(bot: lightbulb.BotApp) -> None:
  bot.add_plugin(weather_plugin)
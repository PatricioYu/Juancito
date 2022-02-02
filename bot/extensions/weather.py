import python_weather

import lightbulb

weather_plugin = lightbulb.Plugin("Weather")


@weather_plugin.command
@lightbulb.option(
  "location",
  "Gets the location.",
  modifier=lightbulb.commands.OptionModifier.CONSUME_REST,
  type=str,
  required=True
)
@lightbulb.command("weather", "gets the weather from a specific location.")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def weather(ctx: lightbulb.Context) -> None:
  client = python_weather.Client(format=python_weather.METRIC)

  weather = await client.find(ctx.options.location)

  await ctx.respond(f"{weather.current.sky_text} day in {ctx.options.location}")

  await client.close()

@weather.child
@lightbulb.option(
  "location",
  "Gets the location.",
  modifier=lightbulb.commands.OptionModifier.CONSUME_REST,
  type=str,
  required=True
)
@lightbulb.command("temp", "Gets the temperature from a specific location.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def weather(ctx: lightbulb.Context) -> None:
  client = python_weather.Client(format=python_weather.METRIC)

  weather = await client.find(ctx.options.location)

  # Different responses in relation to the temperature
  if weather.current.temperature >= 30:
    res = f":man_mage: The temperature in {ctx.options.location} is {weather.current.temperature}° 🥵"
  elif weather.current.temperature <= 10:
    res = f":man_mage: The temperature in {ctx.options.location} is {weather.current.temperature}° 🥶"
  else: 
    res = f":man_mage: The temperature in {ctx.options.location} is {weather.current.temperature}° 😎"

  await ctx.respond(res)

  await client.close()

def load(bot: lightbulb.BotApp) -> None:
  bot.add_plugin(weather_plugin)
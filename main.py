✅ ALL-IN-ONE ChatGPT-Like Discord Bot using OpenAI API

Requirements: Python 3.10+, OpenAI API key, Discord bot token

import discord from discord import app_commands from discord.ext import commands import openai import subprocess import json import asyncio import os import aiohttp import psutil import platform import datetime import random import logging from collections import defaultdict

TOKEN = "MTM5NjUyNTMwODkyODE5NjcxMg.GVuJ5u.3_XLF8ZdrI8XKcQ-As7l6kbcUVe0bj8HHcQDGo" GUILD_ID = None  # Global command sync OPENAI_API_KEY = "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" openai.api_key = OPENAI_API_KEY

ticket_channels = defaultdict(dict) intents = discord.Intents.all() bot = commands.Bot(command_prefix="!", intents=intents) tree = bot.tree logging.basicConfig(level=logging.INFO)

=============== AI ENGINE (OpenAI GPT-4) ===============

async def query_openai(prompt): try: response = openai.ChatCompletion.create( model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=2000, temperature=0.7 ) return response.choices[0].message.content.strip() except Exception as e: return f"❌ OpenAI Error: {str(e)}"

=============== IMAGE GENERATION PLACEHOLDER ===============

async def generate_image(prompt): return "🖼️ Image generation placeholder (DALL·E API not connected)."

=============== COMMANDS ===============

@tree.command(name="chat", description="Talk with AI (OpenAI GPT-4)") @app_commands.describe(prompt="Ask anything") async def chat(interaction: discord.Interaction, prompt: str): await interaction.response.defer() response = await query_openai(prompt) await interaction.followup.send(f"You: {prompt}\nAI: {response[:1900]}")

@tree.command(name="code", description="Generate code with AI") @app_commands.describe(task="What code do you want?") async def code(interaction: discord.Interaction, task: str): await interaction.response.defer() prompt = f"Write code for: {task}" response = await query_openai(prompt) await interaction.followup.send(f"python\n{response[:1900]}")

@tree.command(name="mod", description="Moderate a message with AI") @app_commands.describe(message="Message to analyze") async def mod(interaction: discord.Interaction, message: str): await interaction.response.defer() prompt = f"Is this message harmful, spammy, or offensive? Justify clearly.\nMessage: {message}" result = await query_openai(prompt) await interaction.followup.send(f"Moderation Result: {result[:1900]}")

@tree.command(name="stats", description="Get bot performance stats") async def stats(interaction: discord.Interaction): cpu = psutil.cpu_percent() ram = psutil.virtual_memory().percent await interaction.response.send_message(f"📊 CPU: {cpu}% | RAM: {ram}%")

=============== TICKET SYSTEM ===============

@tree.command(name="ticket", description="Create a support ticket") @app_commands.describe(reason="Reason for creating the ticket") async def ticket(interaction: discord.Interaction, reason: str): guild = interaction.guild category = discord.utils.get(guild.categories, name="Tickets") if not category: category = await guild.create_category("Tickets")

overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
}
channel = await guild.create_text_channel(name=f"ticket-{interaction.user.name}", overwrites=overwrites, category=category)
ticket_channels[interaction.user.id] = channel.id

await interaction.response.send_message(f"🎫 Ticket created: {channel.mention}", ephemeral=True)
await channel.send(f"{interaction.user.mention} Ticket created for: **{reason}**")

@tree.command(name="close_ticket", description="Close your ticket") async def close_ticket(interaction: discord.Interaction): if interaction.user.id in ticket_channels: channel_id = ticket_channels[interaction.user.id] channel = bot.get_channel(channel_id) if channel: await channel.delete() del ticket_channels[interaction.user.id] await interaction.response.send_message("✅ Ticket closed.", ephemeral=True) else: await interaction.response.send_message("❌ You don't have an open ticket.", ephemeral=True)

=============== EVENTS ===============

@bot.event async def on_ready(): if GUILD_ID: await tree.sync(guild=discord.Object(id=GUILD_ID)) else: await tree.sync() print(f"🤖 Bot ready as {bot.user}")

bot.run(TOKEN)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                                                                  ║
# ║   ░█▀▀░█▀█░█▀▄░█▀▀░█░█   ░█▀▄░█▀▀░█░█░█▀▀                     ║
# ║   ░█░░░█░█░█░█░█▀▀░▄▀▄   ░█░█░█▀▀░▀▄▀░▀▀█                     ║
# ║   ░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀░▀   ░▀▀░░▀▀▀░░▀░░▀▀▀                     ║
# ║                                                                  ║
# ║            © 2026 CodeX Devs — All Rights Reserved              ║
# ║                                                                  ║
# ║   discord  ──  https://discord.gg/codexdev                      ║
# ║   youtube  ──  https://youtube.com/@CodeXDevs                   ║
# ║   github   ──  https://github.com/RayExo                        ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝
import asyncio
import aiohttp
from fastapi import APIRouter, Depends
from api.dependencies import get_bot
from api.schemas import BotInfo, BotStatus
from typing import TYPE_CHECKING
from utils.config import *


if TYPE_CHECKING:
    from core.zyrox import zyrox

router = APIRouter()

async def start_self_ping():
    await asyncio.sleep(15)
    url = "https://zyrox-cv2-aio-with-dashboard-3.onrender.com/api/v1/bot/status"
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url) as resp:
                    print(f"[Auto-Ping] Estado: {resp.status}")
            except Exception as e:
                print(f"[Auto-Ping] Error: {e}")
            await asyncio.sleep(300)

@router.on_event("startup")
async def on_startup():
    asyncio.create_task(start_self_ping())

@router.head("/status")
@router.get("/status", response_model=BotStatus, summary="Get bot status", description="Returns real-time health metrics, latency, and scale information.")
async def get_status(bot: "zyrox" = Depends(get_bot)):
    """
    Returns the live status of the bot.
    """
    return BotStatus(
        user=str(bot.user),
        id=str(bot.user.id) if bot.user else None,
        latency=bot.latency * 1000,
        guild_count=len(bot.guilds),
        user_count=sum(g.member_count or 0 for g in bot.guilds),
        shards=bot.shard_count
    )

@router.get("/info", response_model=BotInfo, summary="Get bot info", description="Returns general information about the bot including command count and user reach.")
async def get_bot_info(bot: "zyrox" = Depends(get_bot)):
    """
    Get general information about the Discord bot.
    """
    return BotInfo(
        name=bot.user.name if bot.user else BRAND_NAME,
        id=str(bot.user.id) if bot.user else None,
        guilds=len(bot.guilds),
        users=sum(g.member_count or 0 for g in bot.guilds),
        commands=len(bot.commands),
        latency=f"{round(bot.latency * 1000, 2)}ms"
    )

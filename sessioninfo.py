# -*- coding: utf-8 -*-
# meta developer: @NEBULASoftware
# scope: hikka_only
# scope: hikka_min 1.6.2
# 🔍 SessionInfo PRO — полная информация о сессии и устройстве
# ⚠️ Показывает IP, телефон, страну и многое другое

__version__ = (1, 0, 3)

from .. import loader, utils
from telethon.tl.types import Message
import asyncio
import aiohttp
import platform
import sys
import os
import socket
import datetime
import time

@loader.tds
class SessionInfoMod(loader.Module):
    """🔍 Полная информация о сессии, устройстве и IP
    Разработчик: @NEBULASoftware
    Версия: 1.0.3
    
    📌 Основные команды:
    • .session - показать всю информацию о сессии
    • .sessionip - только информация об IP
    • .sessionphone - информация о номере телефона
    • .sessiondevice - информация об устройстве
    • .sessiondc - информация о дата-центре
    • .sessionfull - полная информация (все разделы)
    
    🛡️ Безопасность:
    • .sessionhide - настройка скрытия данных
    • .sessionalert - уведомления о подозрительной активности
    
    ⚙️ Настройки:
    • .sessionconfig - показать текущие настройки
    • .sessiontoggle - вкл/выкл модуль
    • .sessionhelp - это сообщение"""
    
    strings = {
        "name": "SessionInfoPRO",
        "enabled": "✅ <b>Модуль включен</b>",
        "disabled": "⚠ <b>Модуль выключен</b>",
        "no_permission": "🚫 <b>Нет прав</b>",
        "config": "⚙️ <b>Текущие настройки:</b>\n{data}",
        "fetching": "🔍 <b>Получаю информацию...</b>",
        
        "session_title": "🔐 <b>Информация о сессии</b>\n\n",
        "user_info": "👤 <b>Пользователь:</b> <code>{}</code>",
        "user_id": "🆔 <b>ID:</b> <code>{}</code>",
        "phone": "📱 <b>Телефон:</b> <code>{}</code>",
        "dc": "🌐 <b>Дата-центр:</b> <code>DC{}</code>",
        "dc_ip": "📡 <b>IP DC:</b> <code>{}</code>",
        "dc_location": "📍 <b>Локация DC:</b> <code>{}</code>",
        "premium": "⭐ <b>Premium:</b> <code>{}</code>",
        "verified": "✅ <b>Верифицирован:</b> <code>{}</code>",
        "bot": "🤖 <b>Бот:</b> <code>{}</code>",
        "scam": "⚠️ <b>Скам:</b> <code>{}</code>",
        "fake": "🎭 <b>Фейк:</b> <code>{}</code>",
        
        "ip_title": "🌍 <b>Информация об IP</b>\n\n",
        "ip_address": "🌐 <b>IP адрес:</b> <code>{}</code>",
        "ip_country": "🇺🇳 <b>Страна:</b> <code>{}</code>",
        "ip_region": "🏙️ <b>Регион:</b> <code>{}</code>",
        "ip_city": "🏠 <b>Город:</b> <code>{}</code>",
        "ip_isp": "🏢 <b>Провайдер:</b> <code>{}</code>",
        "ip_timezone": "⏰ <b>Часовой пояс:</b> <code>{}</code>",
        
        "device_title": "💻 <b>Информация об устройстве</b>\n\n",
        "device_system": "🖥️ <b>ОС:</b> <code>{}</code>",
        "device_release": "📀 <b>Версия:</b> <code>{}</code>",
        "device_arch": "🔧 <b>Архитектура:</b> <code>{}</code>",
        "device_hostname": "🏷️ <b>Имя хоста:</b> <code>{}</code>",
        "device_python": "🐍 <b>Python:</b> <code>{}</code>",
        "device_uptime": "⏱️ <b>Аптайм:</b> <code>{}</code>",
        "device_cpu": "💾 <b>Процессор:</b> <code>{}</code>",
        "device_cores": "⚡ <b>Ядер:</b> <code>{}</code>",
        "device_ram": "🧠 <b>RAM:</b> <code>{}/{} ({}%)</code>",
        "device_disk": "💿 <b>Диск:</b> <code>{}/{} ({}%)</code>",
        
        "hide_title": "🎭 <b>Настройки скрытия данных</b>\n\n",
        "hide_current": "📋 <b>Текущие настройки:</b>\n{settings}",
        "hide_help": "🔧 <b>Команды:</b>\n"
                     "• <code>.sessionhide ip</code> - скрыть IP\n"
                     "• <code>.sessionhide phone</code> - скрыть телефон\n"
                     "• <code>.sessionhide location</code> - скрыть локацию\n"
                     "• <code>.sessionhide device</code> - скрыть устройство\n"
                     "• <code>.sessionhide all</code> - скрыть все\n"
                     "• <code>.sessionhide none</code> - показать все",
        "hide_updated": "✅ <b>Настройки скрытия обновлены</b>",
        
        "alert_status": "⚠️ <b>Оповещения безопасности:</b> {status}",
        "alert_on": "🟢 Включены",
        "alert_off": "🔴 Выключены",
        
        "banner": "https://i.postimg.cc/vZzHZtqn/images.png"
    }
    
    strings_ru = {
        "name": "SessionInfoPRO",
        "enabled": "✅ <b>Модуль включен</b>",
        "disabled": "⚠ <b>Модуль выключен</b>",
        "no_permission": "🚫 <b>Нет прав</b>",
        "config": "⚙️ <b>Текущие настройки:</b>\n{data}",
        "fetching": "🔍 <b>Получаю информацию...</b>",
        
        "session_title": "🔐 <b>Информация о сессии</b>\n\n",
        "user_info": "👤 <b>Пользователь:</b> <code>{}</code>",
        "user_id": "🆔 <b>ID:</b> <code>{}</code>",
        "phone": "📱 <b>Телефон:</b> <code>{}</code>",
        "dc": "🌐 <b>Дата-центр:</b> <code>DC{}</code>",
        "dc_ip": "📡 <b>IP DC:</b> <code>{}</code>",
        "dc_location": "📍 <b>Локация DC:</b> <code>{}</code>",
        "premium": "⭐ <b>Premium:</b> <code>{}</code>",
        "verified": "✅ <b>Верифицирован:</b> <code>{}</code>",
        "bot": "🤖 <b>Бот:</b> <code>{}</code>",
        "scam": "⚠️ <b>Скам:</b> <code>{}</code>",
        "fake": "🎭 <b>Фейк:</b> <code>{}</code>",
        
        "ip_title": "🌍 <b>Информация об IP</b>\n\n",
        "ip_address": "🌐 <b>IP адрес:</b> <code>{}</code>",
        "ip_country": "🇺🇳 <b>Страна:</b> <code>{}</code>",
        "ip_region": "🏙️ <b>Регион:</b> <code>{}</code>",
        "ip_city": "🏠 <b>Город:</b> <code>{}</code>",
        "ip_isp": "🏢 <b>Провайдер:</b> <code>{}</code>",
        "ip_timezone": "⏰ <b>Часовой пояс:</b> <code>{}</code>",
        
        "device_title": "💻 <b>Информация об устройстве</b>\n\n",
        "device_system": "🖥️ <b>ОС:</b> <code>{}</code>",
        "device_release": "📀 <b>Версия:</b> <code>{}</code>",
        "device_arch": "🔧 <b>Архитектура:</b> <code>{}</code>",
        "device_hostname": "🏷️ <b>Имя хоста:</b> <code>{}</code>",
        "device_python": "🐍 <b>Python:</b> <code>{}</code>",
        "device_uptime": "⏱️ <b>Аптайм:</b> <code>{}</code>",
        "device_cpu": "💾 <b>Процессор:</b> <code>{}</code>",
        "device_cores": "⚡ <b>Ядер:</b> <code>{}</code>",
        "device_ram": "🧠 <b>RAM:</b> <code>{}/{} ({}%)</code>",
        "device_disk": "💿 <b>Диск:</b> <code>{}/{} ({}%)</code>",
        
        "hide_title": "🎭 <b>Настройки скрытия данных</b>\n\n",
        "hide_current": "📋 <b>Текущие настройки:</b>\n{settings}",
        "hide_help": "🔧 <b>Команды:</b>\n"
                     "• <code>.sessionhide ip</code> - скрыть IP\n"
                     "• <code>.sessionhide phone</code> - скрыть телефон\n"
                     "• <code>.sessionhide location</code> - скрыть локацию\n"
                     "• <code>.sessionhide device</code> - скрыть устройство\n"
                     "• <code>.sessionhide all</code> - скрыть все\n"
                     "• <code>.sessionhide none</code> - показать все",
        "hide_updated": "✅ <b>Настройки скрытия обновлены</b>",
        
        "alert_status": "⚠️ <b>Оповещения безопасности:</b> {status}",
        "alert_on": "🟢 Включены",
        "alert_off": "🔴 Выключены",
        
        "banner": "https://i.postimg.cc/vZzHZtqn/images.png"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "is_active",
                True,
                "Активность модуля",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "hide_ip",
                False,
                "Скрывать IP адрес",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "hide_phone",
                False,
                "Скрывать номер телефона",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "hide_location",
                False,
                "Скрывать геолокацию",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "hide_device",
                False,
                "Скрывать информацию об устройстве",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "security_alerts",
                True,
                "Оповещения о подозрительной активности",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "allowed_users",
                [],
                "ID разрешенных пользователей",
                validator=loader.validators.Series()
            )
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.start_time = time.time()
        self.me = await client.get_me()
        self.dc_info = {
            1: {"ip": "149.154.175.50", "location": "Miami, USA"},
            2: {"ip": "149.154.167.51", "location": "Amsterdam, Netherlands"},
            3: {"ip": "149.154.175.100", "location": "Miami, USA"},
            4: {"ip": "149.154.167.91", "location": "Amsterdam, Netherlands"},
            5: {"ip": "91.108.56.100", "location": "Singapore"},
            6: {"ip": "2001:67c:4e8::f", "location": "Sydney, Australia"}
        }

    async def _check_permission(self, message: Message) -> bool:
        if not self.config["is_active"]:
            await utils.answer(message, self.strings["disabled"])
            return False
        
        user_id = message.sender_id
        if user_id == self.me.id:
            return True
        if user_id in self.config["allowed_users"]:
            return True
        
        await utils.answer(message, self.strings("no_permission"))
        return False

    async def _get_ip_info(self) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://ipapi.co/json/', timeout=5) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except:
            pass
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://ipinfo.io/json', timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        loc = data.get('loc', ',').split(',') if data.get('loc') else ['', '']
                        return {
                            'ip': data.get('ip'),
                            'country': data.get('country'),
                            'region': data.get('region'),
                            'city': data.get('city'),
                            'org': data.get('org'),
                            'timezone': data.get('timezone'),
                            'latitude': loc[0] if len(loc) > 0 else '',
                            'longitude': loc[1] if len(loc) > 1 else ''
                        }
        except:
            pass
        
        return {}

    async def _get_system_info(self) -> dict:
        info = {}
        try:
            info['system'] = platform.system()
            info['release'] = platform.release()
            info['arch'] = platform.machine()
            info['hostname'] = socket.gethostname()
            info['python'] = sys.version.split()[0]
            
            try:
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.readline().split()[0])
                    days = int(uptime_seconds // 86400)
                    hours = int((uptime_seconds % 86400) // 3600)
                    minutes = int((uptime_seconds % 3600) // 60)
                    info['uptime'] = f"{days}д {hours}ч {minutes}м"
            except:
                info['uptime'] = "Unknown"
            
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read()
                    for line in cpuinfo.split('\n'):
                        if 'model name' in line:
                            info['cpu'] = line.split(':')[1].strip()
                            break
                    info['cores'] = cpuinfo.count('processor')
            except:
                info['cpu'] = platform.processor() or "Unknown"
                info['cores'] = os.cpu_count() or "Unknown"
            
            try:
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                    mem_total = 0
                    mem_available = 0
                    for line in meminfo.split('\n'):
                        if 'MemTotal' in line:
                            mem_total = int(line.split()[1]) * 1024
                        if 'MemAvailable' in line:
                            mem_available = int(line.split()[1]) * 1024
                    if mem_total > 0:
                        mem_used = mem_total - mem_available
                        info['ram_total'] = self._bytes_to_human(mem_total)
                        info['ram_used'] = self._bytes_to_human(mem_used)
                        info['ram_percent'] = round((mem_used / mem_total) * 100, 1)
            except:
                info['ram_total'] = "Unknown"
                info['ram_used'] = "Unknown"
                info['ram_percent'] = "Unknown"
            
            try:
                if os.path.exists('/'):
                    stat = os.statvfs('/')
                    disk_total = stat.f_frsize * stat.f_blocks
                    disk_free = stat.f_frsize * stat.f_bfree
                    disk_used = disk_total - disk_free
                    info['disk_total'] = self._bytes_to_human(disk_total)
                    info['disk_used'] = self._bytes_to_human(disk_used)
                    info['disk_percent'] = round((disk_used / disk_total) * 100, 1)
            except:
                info['disk_total'] = "Unknown"
                info['disk_used'] = "Unknown"
                info['disk_percent'] = "Unknown"
            
        except Exception:
            pass
        
        return info

    def _bytes_to_human(self, bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.1f}{unit}"
            bytes /= 1024
        return f"{bytes:.1f}PB"

    def _mask_string(self, text: str, show_first: int = 3, show_last: int = 2) -> str:
        if not text:
            return "Скрыто"
        text = str(text)
        if len(text) > show_first + show_last:
            return text[:show_first] + '*' * (len(text) - show_first - show_last) + text[-show_last:]
        return '*' * len(text)

    def _get_dc_id(self) -> int:
        try:
            if hasattr(self.client, 'session') and hasattr(self.client.session, 'dc_id'):
                return self.client.session.dc_id
            if hasattr(self.client, 'auth_key') and hasattr(self.client.auth_key, 'dc_id'):
                return self.client.auth_key.dc_id
            return 2
        except:
            return 2

    async def _send_with_banner(self, message: Message, text: str):
        """Отправляет сообщение с баннером вверху"""
        # Создаем невидимый спойлер с картинкой для баннера
        banner_code = f"<a href=\"{self.strings['banner']}\">⁠</a>"
        full_text = banner_code + "\n" + text
        await utils.answer(message, full_text)

    @loader.command()
    async def session(self, message: Message):
        """Показать полную информацию о сессии"""
        if not await self._check_permission(message):
            return
        
        msg = await utils.answer(message, self.strings("fetching"))
        
        ip_info = await self._get_ip_info()
        system_info = await self._get_system_info()
        user = self.me
        dc_id = self._get_dc_id()
        dc_info = self.dc_info.get(dc_id, {"ip": "Unknown", "location": "Unknown"})
        
        text = self.strings["session_title"]
        
        name = user.first_name or "None"
        if user.last_name:
            name += " " + user.last_name
        text += self.strings["user_info"].format(name) + "\n"
        text += self.strings["user_id"].format(user.id) + "\n"
        
        phone = user.phone or "Нет"
        if self.config["hide_phone"] and phone != "Нет":
            phone = self._mask_string(phone, 2, 2)
        text += self.strings["phone"].format(phone) + "\n"
        
        text += self.strings["dc"].format(dc_id) + "\n"
        text += self.strings["dc_ip"].format(dc_info["ip"]) + "\n"
        text += self.strings["dc_location"].format(dc_info["location"]) + "\n"
        
        text += self.strings["premium"].format("✅" if getattr(user, 'premium', False) else "❌") + "\n"
        text += self.strings["verified"].format("✅" if getattr(user, 'verified', False) else "❌") + "\n"
        text += self.strings["bot"].format("✅" if getattr(user, 'bot', False) else "❌") + "\n"
        text += self.strings["scam"].format("✅" if getattr(user, 'scam', False) else "❌") + "\n"
        text += self.strings["fake"].format("✅" if getattr(user, 'fake', False) else "❌") + "\n\n"
        
        if ip_info:
            text += self.strings["ip_title"]
            
            ip = ip_info.get('ip', 'Unknown')
            if self.config["hide_ip"] and ip != 'Unknown':
                ip = self._mask_string(ip, 3, 3)
            text += self.strings["ip_address"].format(ip) + "\n"
            
            if not self.config["hide_location"]:
                text += self.strings["ip_country"].format(ip_info.get('country', 'Unknown')) + "\n"
                text += self.strings["ip_region"].format(ip_info.get('region', 'Unknown')) + "\n"
                text += self.strings["ip_city"].format(ip_info.get('city', 'Unknown')) + "\n"
            
            text += self.strings["ip_isp"].format(ip_info.get('org', 'Unknown')) + "\n"
            text += self.strings["ip_timezone"].format(ip_info.get('timezone', 'Unknown')) + "\n\n"
        
        if not self.config["hide_device"] and system_info:
            text += self.strings["device_title"]
            text += self.strings["device_system"].format(system_info.get('system', 'Unknown')) + "\n"
            text += self.strings["device_release"].format(system_info.get('release', 'Unknown')) + "\n"
            text += self.strings["device_arch"].format(system_info.get('arch', 'Unknown')) + "\n"
            text += self.strings["device_hostname"].format(system_info.get('hostname', 'Unknown')) + "\n"
            text += self.strings["device_python"].format(system_info.get('python', 'Unknown')) + "\n"
            text += self.strings["device_uptime"].format(system_info.get('uptime', 'Unknown')) + "\n"
            text += self.strings["device_cpu"].format(system_info.get('cpu', 'Unknown')) + "\n"
            text += self.strings["device_cores"].format(system_info.get('cores', 'Unknown')) + "\n"
            
            if system_info.get('ram_used') and system_info.get('ram_total') and system_info.get('ram_percent'):
                text += self.strings["device_ram"].format(
                    system_info.get('ram_used', '0'),
                    system_info.get('ram_total', '0'),
                    system_info.get('ram_percent', '0')
                ) + "\n"
            
            if system_info.get('disk_used') and system_info.get('disk_total') and system_info.get('disk_percent'):
                text += self.strings["device_disk"].format(
                    system_info.get('disk_used', '0'),
                    system_info.get('disk_total', '0'),
                    system_info.get('disk_percent', '0')
                )
        
        await self._send_with_banner(msg, text)

    @loader.command()
    async def sessionip(self, message: Message):
        """Показать только информацию об IP"""
        if not await self._check_permission(message):
            return
        
        msg = await utils.answer(message, self.strings("fetching"))
        ip_info = await self._get_ip_info()
        
        if not ip_info:
            await self._send_with_banner(msg, "❌ Не удалось получить информацию об IP")
            return
        
        text = self.strings["ip_title"]
        
        ip = ip_info.get('ip', 'Unknown')
        if self.config["hide_ip"] and ip != 'Unknown':
            ip = self._mask_string(ip, 3, 3)
        text += self.strings["ip_address"].format(ip) + "\n"
        
        if not self.config["hide_location"]:
            text += self.strings["ip_country"].format(ip_info.get('country', 'Unknown')) + "\n"
            text += self.strings["ip_region"].format(ip_info.get('region', 'Unknown')) + "\n"
            text += self.strings["ip_city"].format(ip_info.get('city', 'Unknown')) + "\n"
        
        text += self.strings["ip_isp"].format(ip_info.get('org', 'Unknown')) + "\n"
        text += self.strings["ip_timezone"].format(ip_info.get('timezone', 'Unknown'))
        
        await self._send_with_banner(msg, text)

    @loader.command()
    async def sessionphone(self, message: Message):
        """Показать информацию о номере телефона"""
        if not await self._check_permission(message):
            return
        
        phone = self.me.phone or "Нет"
        if self.config["hide_phone"] and phone != "Нет":
            phone = self._mask_string(phone, 2, 2)
        
        dc_id = self._get_dc_id()
        
        text = f"""
📱 <b>Информация о номере</b>

<b>Номер:</b> <code>{phone}</code>
<b>ID:</b> <code>{self.me.id}</code>
<b>DC:</b> <code>DC{dc_id}</code>
<b>Premium:</b> {"✅" if getattr(self.me, 'premium', False) else "❌"}
"""
        await self._send_with_banner(message, text)

    @loader.command()
    async def sessiondevice(self, message: Message):
        """Показать информацию об устройстве"""
        if not await self._check_permission(message):
            return
        
        if self.config["hide_device"]:
            await self._send_with_banner(message, "❌ Информация об устройстве скрыта в настройках")
            return
        
        msg = await utils.answer(message, self.strings("fetching"))
        system_info = await self._get_system_info()
        
        text = self.strings["device_title"]
        text += self.strings["device_system"].format(system_info.get('system', 'Unknown')) + "\n"
        text += self.strings["device_release"].format(system_info.get('release', 'Unknown')) + "\n"
        text += self.strings["device_arch"].format(system_info.get('arch', 'Unknown')) + "\n"
        text += self.strings["device_hostname"].format(system_info.get('hostname', 'Unknown')) + "\n"
        text += self.strings["device_python"].format(system_info.get('python', 'Unknown')) + "\n"
        text += self.strings["device_uptime"].format(system_info.get('uptime', 'Unknown')) + "\n"
        text += self.strings["device_cpu"].format(system_info.get('cpu', 'Unknown')) + "\n"
        text += self.strings["device_cores"].format(system_info.get('cores', 'Unknown')) + "\n"
        
        if system_info.get('ram_used') and system_info.get('ram_total') and system_info.get('ram_percent'):
            text += self.strings["device_ram"].format(
                system_info.get('ram_used', '0'),
                system_info.get('ram_total', '0'),
                system_info.get('ram_percent', '0')
            ) + "\n"
        
        if system_info.get('disk_used') and system_info.get('disk_total') and system_info.get('disk_percent'):
            text += self.strings["device_disk"].format(
                system_info.get('disk_used', '0'),
                system_info.get('disk_total', '0'),
                system_info.get('disk_percent', '0')
            )
        
        await self._send_with_banner(msg, text)

    @loader.command()
    async def sessiondc(self, message: Message):
        """Показать информацию о дата-центре"""
        if not await self._check_permission(message):
            return
        
        dc_id = self._get_dc_id()
        dc_info = self.dc_info.get(dc_id, {"ip": "Unknown", "location": "Unknown"})
        
        text = f"""
🌐 <b>Информация о дата-центре</b>

<b>DC:</b> <code>DC{dc_id}</code>
<b>IP:</b> <code>{dc_info['ip']}</code>
<b>Локация:</b> <code>{dc_info['location']}</code>
"""
        await self._send_with_banner(message, text)

    @loader.command()
    async def sessionfull(self, message: Message):
        """Показать полную информацию (все разделы)"""
        await self.session(message)

    @loader.command()
    async def sessionhide(self, message: Message):
        """Настройка скрытия данных. Использование: .sessionhide <ip/phone/location/device/all/none>"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message).lower()
        
        if not args:
            settings = (
                f"• IP: {'🔴 Скрыт' if self.config['hide_ip'] else '🟢 Показан'}\n"
                f"• Телефон: {'🔴 Скрыт' if self.config['hide_phone'] else '🟢 Показан'}\n"
                f"• Локация: {'🔴 Скрыта' if self.config['hide_location'] else '🟢 Показана'}\n"
                f"• Устройство: {'🔴 Скрыто' if self.config['hide_device'] else '🟢 Показано'}"
            )
            
            text = self.strings["hide_title"]
            text += self.strings["hide_current"].format(settings=settings) + "\n\n"
            text += self.strings["hide_help"]
            await self._send_with_banner(message, text)
            return
        
        if args == "ip":
            self.config["hide_ip"] = not self.config["hide_ip"]
        elif args == "phone":
            self.config["hide_phone"] = not self.config["hide_phone"]
        elif args == "location":
            self.config["hide_location"] = not self.config["hide_location"]
        elif args == "device":
            self.config["hide_device"] = not self.config["hide_device"]
        elif args == "all":
            self.config["hide_ip"] = True
            self.config["hide_phone"] = True
            self.config["hide_location"] = True
            self.config["hide_device"] = True
        elif args == "none":
            self.config["hide_ip"] = False
            self.config["hide_phone"] = False
            self.config["hide_location"] = False
            self.config["hide_device"] = False
        else:
            await self._send_with_banner(message, "❌ Неизвестная опция. Используйте: ip/phone/location/device/all/none")
            return
        
        await self._send_with_banner(message, self.strings("hide_updated"))

    @loader.command()
    async def sessionalert(self, message: Message):
        """Включить/выключить оповещения безопасности"""
        self.config["security_alerts"] = not self.config["security_alerts"]
        status = self.strings["alert_on"] if self.config["security_alerts"] else self.strings["alert_off"]
        await self._send_with_banner(message, self.strings["alert_status"].format(status=status))

    @loader.command()
    async def sessiontoggle(self, message: Message):
        """Включить/выключить модуль"""
        self.config["is_active"] = not self.config["is_active"]
        status = self.strings["enabled"] if self.config["is_active"] else self.strings["disabled"]
        await self._send_with_banner(message, status)

    @loader.command()
    async def sessionconfig(self, message: Message):
        """Показать текущие настройки модуля"""
        config_lines = []
        for key, value in self.config.items():
            if isinstance(value, bool):
                display_value = "✅ Да" if value else "❌ Нет"
            elif isinstance(value, list):
                display_value = ", ".join(map(str, value)) if value else "Пусто"
            else:
                display_value = str(value)
            config_lines.append(f"• <b>{key}:</b> <code>{display_value}</code>")
        
        config_data = "\n".join(config_lines)
        text = self.strings["config"].format(data=config_data)
        await self._send_with_banner(message, text)

    @loader.command()
    async def sessionhelp(self, message: Message):
        """Показать это сообщение"""
        banner_code = f"<a href=\"{self.strings['banner']}\">⁠</a>"
        help_text = banner_code + """
🔍 <b>SessionInfo PRO v1.0.3</b>
Разработчик: @NEBULASoftware

📌 <b>Основные команды:</b>
• <code>.session</code> - полная информация
• <code>.sessionip</code> - только IP
• <code>.sessionphone</code> - только телефон
• <code>.sessiondevice</code> - только устройство
• <code>.sessiondc</code> - только дата-центр
• <code>.sessionfull</code> - все разделы

🛡️ <b>Безопасность:</b>
• <code>.sessionhide</code> - настройки скрытия
• <code>.sessionalert</code> - оповещения безопасности

⚙️ <b>Управление:</b>
• <code>.sessiontoggle</code> - вкл/выкл модуль
• <code>.sessionconfig</code> - показать настройки
• <code>.sessionhelp</code> - это сообщение
• <code>.cfg SessionInfoPRO</code> - настройки через конфиг

📊 <b>Что показывает:</b>
• 👤 Информация о пользователе
• 📱 Номер телефона
• 🌐 IP адрес и геолокация
• 🏢 Провайдер
• 💻 Информация об устройстве
• 🌍 Дата-центр Telegram

🔧 <b>Настройки скрытия:</b>
• <code>.sessionhide ip</code> - скрыть IP
• <code>.sessionhide phone</code> - скрыть телефон
• <code>.sessionhide location</code> - скрыть локацию
• <code>.sessionhide device</code> - скрыть устройство
• <code>.sessionhide all</code> - скрыть все
• <code>.sessionhide none</code> - показать все
"""
        await utils.answer(message, help_text)
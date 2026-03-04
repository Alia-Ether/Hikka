# -*- coding: utf-8 -*-
# meta developer: @NEBULASoftware
# scope: hikka_only
# scope: hikka_min 1.6.2
# 🔥 TermControl PRO — полное управление терминалом + избранное

__version__ = (3, 0, 0)

from .. import loader, utils
from telethon.tl.types import Message
import asyncio
import subprocess
import os
import signal
import sys
from datetime import datetime

@loader.tds
class TermControlMod(loader.Module):
    """🔥 Полное управление терминалом: любые команды + избранное
    Разработчик: @NEBULASoftware
    Версия: 3.0.0
    
    📌 Основные команды:
    • .t <команда> - выполнить любую команду (короткая версия)
    • .term <команда> - выполнить любую команду
    • .termbg <команда> - выполнить в фоне
    • .termcd <путь> - сменить директорию
    • .termls - список файлов
    • .termpwd - показать текущую директорию
    
    📊 Мониторинг:
    • .termcpu - загрузка CPU
    • .termmem - использование памяти
    • .termdisk - место на диске
    • .termnet - сетевые порты
    • .termps - список процессов
    • .termpsgrep <процесс> - поиск процесса
    • .termkill <PID> - остановить процесс
    • .termwhich <команда> - путь к команде
    
    ⭐ Избранное:
    • .fav - список избранных команд
    • .fav add <название> <команда> - добавить
    • .fav remove <название> - удалить
    • .fav run <название> - выполнить
    • .fav edit <название> <команда> - изменить
    
    ⚙️ Управление:
    • .termtoggle - вкл/выкл модуль
    • .termconfig - показать конфиг
    • .termclear - очистить историю
    • .termtimeout <сек> - установить таймаут
    • .termdir <путь> - установить рабочую директорию
    • .termhelp - это сообщение"""
    
    strings = {
        "name": "TermControlPRO",
        "enabled": "✅ <b>Модуль включен</b>",
        "disabled": "⚠ <b>Модуль выключен</b>",
        "no_command": "❌ <b>Введите команду</b>",
        "executing": "⚙️ <b>Выполняю:</b> <code>{}</code>\n📍 <b>Директория:</b> <code>{}</code>\n\n",
        "output": "📤 <b>Вывод</b> ({}):\n<pre>{}</pre>",
        "error": "❌ <b>Ошибка</b> ({}):\n<pre>{}</pre>",
        "timeout": "⏱️ <b>Таймаут</b> (>{}с)",
        "killed": "🛑 <b>Процесс</b> <code>{}</code> <b>остановлен</b>",
        "dir_changed": "📁 <b>Текущая директория:</b> <code>{}</code>",
        "pwd": "📁 <b>Текущая директория:</b> <code>{}</code>",
        "bg_started": "🔄 <b>Фоновая команда:</b> <code>{}</code>\n<b>PID:</b> <code>{}</code>",
        "no_permission": "🚫 <b>Нет прав на выполнение</b>",
        "fav_list": "⭐ <b>Избранные команды:</b>\n{}",
        "fav_added": "✅ <b>Добавлено:</b> <code>{}</code> → <code>{}</code>",
        "fav_removed": "✅ <b>Удалено:</b> <code>{}</code>",
        "fav_not_found": "❌ <b>Команда</b> <code>{}</code> <b>не найдена</b>",
        "fav_exists": "❌ <b>Команда</b> <code>{}</code> <b>уже существует</b>",
        "fav_edited": "✅ <b>Изменено:</b> <code>{}</code> → <code>{}</code>",
        "fav_empty": "⭐ <b>Избранное пусто</b>",
        "long_output": "📤 <b>Вывод</b> ({} строк, первые 30):\n<pre>{}</pre>",
        "process_list": "📋 <b>Активные процессы:</b>\n{}",
        "no_processes": "📋 <b>Нет активных процессов</b>",
        "which": "🔍 <b>{}</b> → <code>{}</code>",
        "which_not_found": "❌ <b>Команда</b> <code>{}</code> <b>не найдена</b>",
        "cpu_info": "💻 <b>CPU:</b>\n<pre>{}</pre>",
        "mem_info": "🧠 <b>Память:</b>\n<pre>{}</pre>",
        "disk_info": "💾 <b>Диск:</b>\n<pre>{}</pre>",
        "net_info": "🌐 <b>Сеть:</b>\n<pre>{}</pre>",
        "ps_found": "🔍 <b>Процессы</b> <code>{}</code>:\n<pre>{}</pre>",
        "ps_not_found": "❌ <b>Процесс</b> <code>{}</code> <b>не найден</b>",
        "history_cleared": "🧹 <b>История очищена</b>",
        "timeout_set": "⏱️ <b>Таймаут установлен:</b> {} сек",
        "dir_set": "📁 <b>Рабочая директория установлена:</b> <code>{}</code>",
        "config": "⚙️ <b>Текущий конфиг:</b>\n{}"
    }
    
    strings_ru = {
        "name": "TermControlPRO",
        "enabled": "✅ <b>Модуль включен</b>",
        "disabled": "⚠ <b>Модуль выключен</b>",
        "no_command": "❌ <b>Введите команду</b>",
        "executing": "⚙️ <b>Выполняю:</b> <code>{}</code>\n📍 <b>Директория:</b> <code>{}</code>\n\n",
        "output": "📤 <b>Вывод</b> ({}):\n<pre>{}</pre>",
        "error": "❌ <b>Ошибка</b> ({}):\n<pre>{}</pre>",
        "timeout": "⏱️ <b>Таймаут</b> (>{}с)",
        "killed": "🛑 <b>Процесс</b> <code>{}</code> <b>остановлен</b>",
        "dir_changed": "📁 <b>Текущая директория:</b> <code>{}</code>",
        "pwd": "📁 <b>Текущая директория:</b> <code>{}</code>",
        "bg_started": "🔄 <b>Фоновая команда:</b> <code>{}</code>\n<b>PID:</b> <code>{}</code>",
        "no_permission": "🚫 <b>Нет прав на выполнение</b>",
        "fav_list": "⭐ <b>Избранные команды:</b>\n{}",
        "fav_added": "✅ <b>Добавлено:</b> <code>{}</code> → <code>{}</code>",
        "fav_removed": "✅ <b>Удалено:</b> <code>{}</code>",
        "fav_not_found": "❌ <b>Команда</b> <code>{}</code> <b>не найдена</b>",
        "fav_exists": "❌ <b>Команда</b> <code>{}</code> <b>уже существует</b>",
        "fav_edited": "✅ <b>Изменено:</b> <code>{}</code> → <code>{}</code>",
        "fav_empty": "⭐ <b>Избранное пусто</b>",
        "long_output": "📤 <b>Вывод</b> ({} строк, первые 30):\n<pre>{}</pre>",
        "process_list": "📋 <b>Активные процессы:</b>\n{}",
        "no_processes": "📋 <b>Нет активных процессов</b>",
        "which": "🔍 <b>{}</b> → <code>{}</code>",
        "which_not_found": "❌ <b>Команда</b> <code>{}</code> <b>не найдена</b>",
        "cpu_info": "💻 <b>CPU:</b>\n<pre>{}</pre>",
        "mem_info": "🧠 <b>Память:</b>\n<pre>{}</pre>",
        "disk_info": "💾 <b>Диск:</b>\n<pre>{}</pre>",
        "net_info": "🌐 <b>Сеть:</b>\n<pre>{}</pre>",
        "ps_found": "🔍 <b>Процессы</b> <code>{}</code>:\n<pre>{}</pre>",
        "ps_not_found": "❌ <b>Процесс</b> <code>{}</code> <b>не найден</b>",
        "history_cleared": "🧹 <b>История очищена</b>",
        "timeout_set": "⏱️ <b>Таймаут установлен:</b> {} сек",
        "dir_set": "📁 <b>Рабочая директория установлена:</b> <code>{}</code>",
        "config": "⚙️ <b>Текущий конфиг:</b>\n{}"
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
                "timeout",
                60,
                "Таймаут команд (секунд)",
                validator=loader.validators.Integer(minimum=5, maximum=3600)
            ),
            loader.ConfigValue(
                "working_dir",
                ".",
                "Рабочая директория",
                validator=None
            ),
            loader.ConfigValue(
                "allow_for_all",
                False,
                "Разрешить всем пользователям",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "allowed_users",
                [],
                "ID разрешенных пользователей",
                validator=loader.validators.Series()
            ),
            loader.ConfigValue(
                "max_output_lines",
                30,
                "Макс. строк в выводе",
                validator=loader.validators.Integer(minimum=10, maximum=200)
            ),
            loader.ConfigValue(
                "log_commands",
                True,
                "Логировать команды",
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.current_dir = os.path.abspath(self.config["working_dir"])
        self.command_history = []
        self.background_processes = {}
        self.favorites = self.db.get("TermControlPRO", "favorites", {})
        os.makedirs(self.current_dir, exist_ok=True)

    @loader.command(alias="t")
    async def termcmd(self, message: Message):
        """Выполнить команду (короткая версия)"""
        await self.term(message)

    async def _check_permission(self, message: Message) -> bool:
        if not self.config["is_active"]:
            await utils.answer(message, self.strings["disabled"])
            return False
        if self.config["allow_for_all"]:
            return True
        user_id = message.sender_id
        me = await self.client.get_me()
        if user_id == me.id:
            return True
        if user_id in self.config["allowed_users"]:
            return True
        await utils.answer(message, self.strings("no_permission"))
        return False

    @loader.command()
    async def term(self, message: Message):
        """Выполнить любую команду в терминале"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_command"))
            return
        
        self.command_history.append(args)
        if len(self.command_history) > 50:
            self.command_history = self.command_history[-50:]
        
        msg = await utils.answer(message, 
            self.strings("executing").format(args, self.current_dir))
        
        try:
            process = await asyncio.create_subprocess_shell(
                args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.current_dir,
                shell=True
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=self.config["timeout"]
                )
            except asyncio.TimeoutError:
                process.kill()
                await utils.answer(msg, self.strings("timeout").format(self.config["timeout"]))
                return
            
            output = stdout.decode('utf-8', errors='ignore') if stdout else ""
            error = stderr.decode('utf-8', errors='ignore') if stderr else ""
            
            if error and not output:
                await utils.answer(msg, self.strings("error").format(args, error.strip()))
                return
            
            lines = output.strip().split('\n')
            if len(lines) > self.config["max_output_lines"]:
                short_output = '\n'.join(lines[:self.config["max_output_lines"]])
                await utils.answer(msg, 
                    self.strings("long_output").format(len(lines), short_output.strip()))
            else:
                await utils.answer(msg, 
                    self.strings("output").format(args, output.strip() if output else "(пусто)"))
                
        except Exception as e:
            await utils.answer(msg, self.strings("error").format(args, str(e)))

    @loader.command(alias="termbg")
    async def term_background(self, message: Message):
        """Запустить команду в фоне"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_command"))
            return
        
        try:
            process = await asyncio.create_subprocess_shell(
                args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.current_dir,
                shell=True,
                start_new_session=True
            )
            
            pid = process.pid
            self.background_processes[pid] = {
                "command": args,
                "process": process,
                "start_time": datetime.now()
            }
            
            asyncio.create_task(self._monitor_background(pid, process))
            await utils.answer(message, self.strings("bg_started").format(args, pid))
            
        except Exception as e:
            await utils.answer(message, f"❌ {str(e)}")

    async def _monitor_background(self, pid: int, process):
        try:
            await process.communicate()
            if pid in self.background_processes:
                del self.background_processes[pid]
        except:
            pass

    @loader.command(alias="termps")
    async def term_processes(self, message: Message):
        """Показать активные фоновые процессы"""
        if not await self._check_permission(message):
            return
        
        if not self.background_processes:
            await utils.answer(message, self.strings("no_processes"))
            return
        
        processes = ""
        for pid, info in self.background_processes.items():
            runtime = (datetime.now() - info["start_time"]).seconds
            processes += f"• PID <code>{pid}</code>: <code>{info['command']}</code> ({runtime}с)\n"
        
        await utils.answer(message, self.strings("process_list").format(processes))

    @loader.command(alias="termkill")
    async def term_kill(self, message: Message):
        """Остановить процесс по PID"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message)
        if not args:
            await self.term_processes(message)
            return
        
        try:
            pid = int(args)
            
            if pid in self.background_processes:
                process = self.background_processes[pid]["process"]
                try:
                    os.kill(pid, signal.SIGTERM)
                except:
                    process.kill()
                del self.background_processes[pid]
                await utils.answer(message, self.strings("killed").format(pid))
                return
            
            try:
                os.kill(pid, signal.SIGTERM)
                await utils.answer(message, self.strings("killed").format(pid))
            except ProcessLookupError:
                await utils.answer(message, f"❌ Процесс {pid} не найден")
            except Exception as e:
                await utils.answer(message, f"❌ {e}")
                
        except ValueError:
            await utils.answer(message, "❌ Некорректный PID")

    @loader.command(alias="termcd")
    async def term_chdir(self, message: Message):
        """Сменить рабочую директорию"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("pwd").format(self.current_dir))
            return
        
        try:
            new_dir = os.path.abspath(os.path.join(self.current_dir, args))
            if not os.path.exists(new_dir):
                await utils.answer(message, f"❌ Нет такой директории: <code>{new_dir}</code>")
                return
            
            if not os.path.isdir(new_dir):
                await utils.answer(message, f"❌ Это не директория: <code>{new_dir}</code>")
                return
            
            os.chdir(new_dir)
            self.current_dir = new_dir
            await utils.answer(message, self.strings("dir_changed").format(new_dir))
            
        except Exception as e:
            await utils.answer(message, f"❌ {e}")

    @loader.command(alias="termls")
    async def term_list(self, message: Message):
        """Показать содержимое директории"""
        if not await self._check_permission(message):
            return
        
        try:
            items = os.listdir(self.current_dir)
            dirs = []
            files = []
            
            for item in sorted(items):
                full = os.path.join(self.current_dir, item)
                if os.path.isdir(full):
                    dirs.append(f"📁 <code>{item}/</code>")
                else:
                    size = os.path.getsize(full)
                    if size < 1024:
                        size_str = f"{size}B"
                    elif size < 1024**2:
                        size_str = f"{size/1024:.1f}KB"
                    elif size < 1024**3:
                        size_str = f"{size/1024**2:.1f}MB"
                    else:
                        size_str = f"{size/1024**3:.1f}GB"
                    files.append(f"📄 <code>{item}</code> ({size_str})")
            
            result = dirs + files
            if not result:
                result = ["(пусто)"]
            
            output = f"📁 <b>{self.current_dir}</b>\n" + "\n".join(result[:30])
            if len(result) > 30:
                output += f"\n... и ещё {len(result)-30}"
            
            await utils.answer(message, output)
            
        except Exception as e:
            await utils.answer(message, f"❌ {e}")

    @loader.command(alias="termpwd")
    async def term_pwd(self, message: Message):
        """Показать текущую директорию"""
        if not await self._check_permission(message):
            return
        
        await utils.answer(message, self.strings("pwd").format(self.current_dir))

    @loader.command(alias="termwhich")
    async def term_which(self, message: Message):
        """Показать путь к команде"""
        if not await self._check_permission(message):
            return
        
        cmd = utils.get_args_raw(message)
        if not cmd:
            await utils.answer(message, "❌ Укажите команду")
            return
        
        try:
            process = await asyncio.create_subprocess_shell(
                f"which {cmd}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, _ = await process.communicate()
            path = stdout.decode().strip()
            
            if path:
                await utils.answer(message, self.strings("which").format(cmd, path))
            else:
                await utils.answer(message, self.strings("which_not_found").format(cmd))
        except:
            await utils.answer(message, self.strings("which_not_found").format(cmd))

    @loader.command(alias="termcpu")
    async def term_cpu(self, message: Message):
        """Показать загрузку CPU"""
        if not await self._check_permission(message):
            return
        
        try:
            process = await asyncio.create_subprocess_shell(
                "top -b -n 1 | grep '%Cpu'",
                stdout=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, _ = await process.communicate()
            await utils.answer(message, self.strings("cpu_info").format(stdout.decode()))
        except:
            await utils.answer(message, "❌ Не удалось получить информацию о CPU")

    @loader.command(alias="termmem")
    async def term_memory(self, message: Message):
        """Показать использование памяти"""
        if not await self._check_permission(message):
            return
        
        try:
            process = await asyncio.create_subprocess_shell(
                "free -h",
                stdout=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, _ = await process.communicate()
            await utils.answer(message, self.strings("mem_info").format(stdout.decode()))
        except:
            await utils.answer(message, "❌ Не удалось получить информацию о памяти")

    @loader.command(alias="termdisk")
    async def term_disk(self, message: Message):
        """Показать использование диска"""
        if not await self._check_permission(message):
            return
        
        try:
            process = await asyncio.create_subprocess_shell(
                "df -h",
                stdout=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, _ = await process.communicate()
            await utils.answer(message, self.strings("disk_info").format(stdout.decode()))
        except:
            await utils.answer(message, "❌ Не удалось получить информацию о диске")

    @loader.command(alias="termnet")
    async def term_network(self, message: Message):
        """Показать сетевые порты"""
        if not await self._check_permission(message):
            return
        
        try:
            process = await asyncio.create_subprocess_shell(
                "netstat -tulpn 2>/dev/null | head -30",
                stdout=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, _ = await process.communicate()
            await utils.answer(message, self.strings("net_info").format(stdout.decode()))
        except:
            await utils.answer(message, "❌ Не удалось получить информацию о сети")

    @loader.command(alias="termpsgrep")
    async def term_ps_grep(self, message: Message):
        """Поиск процесса"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Укажите процесс")
            return
        
        try:
            process = await asyncio.create_subprocess_shell(
                f"ps aux | grep -v grep | grep {args}",
                stdout=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, _ = await process.communicate()
            output = stdout.decode()
            if output:
                await utils.answer(message, self.strings("ps_found").format(args, output))
            else:
                await utils.answer(message, self.strings("ps_not_found").format(args))
        except:
            await utils.answer(message, self.strings("ps_not_found").format(args))

    @loader.command(alias="fav")
    async def fav_list(self, message: Message):
        """Показать список избранных команд"""
        if not await self._check_permission(message):
            return
        
        if not self.favorites:
            await utils.answer(message, self.strings("fav_empty"))
            return
        
        fav_list = ""
        for name, cmd in sorted(self.favorites.items()):
            fav_list += f"⭐ <code>{name}</code> → <code>{cmd}</code>\n"
        
        await utils.answer(message, self.strings("fav_list").format(fav_list))

    @loader.command(alias="favadd")
    async def fav_add(self, message: Message):
        """Добавить команду в избранное"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message).split(maxsplit=1)
        if len(args) < 2:
            await utils.answer(message, "❌ Использование: .fav add <название> <команда>")
            return
        
        name = args[0].lower()
        command = args[1]
        
        if name in self.favorites:
            await utils.answer(message, self.strings("fav_exists").format(name))
            return
        
        self.favorites[name] = command
        self.db.set("TermControlPRO", "favorites", self.favorites)
        await utils.answer(message, self.strings("fav_added").format(name, command))

    @loader.command(alias="favremove")
    async def fav_remove(self, message: Message):
        """Удалить команду из избранного"""
        if not await self._check_permission(message):
            return
        
        name = utils.get_args_raw(message).lower()
        if not name:
            await utils.answer(message, "❌ Укажите название команды")
            return
        
        if name not in self.favorites:
            await utils.answer(message, self.strings("fav_not_found").format(name))
            return
        
        del self.favorites[name]
        self.db.set("TermControlPRO", "favorites", self.favorites)
        await utils.answer(message, self.strings("fav_removed").format(name))

    @loader.command(alias="favrun")
    async def fav_run(self, message: Message):
        """Выполнить избранную команду"""
        if not await self._check_permission(message):
            return
        
        name = utils.get_args_raw(message).lower()
        if not name:
            await utils.answer(message, "❌ Укажите название команды")
            return
        
        if name not in self.favorites:
            await utils.answer(message, self.strings("fav_not_found").format(name))
            return
        
        message.raw_text = f".term {self.favorites[name]}"
        await self.term(message)

    @loader.command(alias="favedit")
    async def fav_edit(self, message: Message):
        """Изменить избранную команду"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message).split(maxsplit=1)
        if len(args) < 2:
            await utils.answer(message, "❌ Использование: .fav edit <название> <новая_команда>")
            return
        
        name = args[0].lower()
        new_command = args[1]
        
        if name not in self.favorites:
            await utils.answer(message, self.strings("fav_not_found").format(name))
            return
        
        self.favorites[name] = new_command
        self.db.set("TermControlPRO", "favorites", self.favorites)
        await utils.answer(message, self.strings("fav_edited").format(name, new_command))

    @loader.command(alias="termtoggle")
    async def term_toggle(self, message: Message):
        """Включить/выключить модуль"""
        self.config["is_active"] = not self.config["is_active"]
        status = self.strings["enabled"] if self.config["is_active"] else self.strings["disabled"]
        await utils.answer(message, status)

    @loader.command(alias="termclear")
    async def term_clear_history(self, message: Message):
        """Очистить историю команд"""
        if not await self._check_permission(message):
            return
        
        self.command_history.clear()
        await utils.answer(message, self.strings("history_cleared"))

    @loader.command(alias="termtimeout")
    async def term_set_timeout(self, message: Message):
        """Установить таймаут команд"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, f"⏱️ Текущий таймаут: {self.config['timeout']} сек")
            return
        
        try:
            timeout = int(args)
            if 5 <= timeout <= 3600:
                self.config["timeout"] = timeout
                await utils.answer(message, self.strings("timeout_set").format(timeout))
            else:
                await utils.answer(message, "❌ Таймаут должен быть от 5 до 3600 секунд")
        except ValueError:
            await utils.answer(message, "❌ Укажите число секунд")

    @loader.command(alias="termdir")
    async def term_set_dir(self, message: Message):
        """Установить рабочую директорию"""
        if not await self._check_permission(message):
            return
        
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, f"📁 Текущая директория: <code>{self.current_dir}</code>")
            return
        
        try:
            new_dir = os.path.abspath(args)
            if not os.path.exists(new_dir):
                await utils.answer(message, f"❌ Директория не существует: <code>{new_dir}</code>")
                return
            
            if not os.path.isdir(new_dir):
                await utils.answer(message, f"❌ Это не директория: <code>{new_dir}</code>")
                return
            
            self.current_dir = new_dir
            self.config["working_dir"] = new_dir
            await utils.answer(message, self.strings("dir_set").format(new_dir))
            
        except Exception as e:
            await utils.answer(message, f"❌ {e}")

    @loader.command(alias="termconfig")
    async def term_config(self, message: Message):
        """Показать конфигурацию модуля"""
        config_data = "\n".join(
            f"• <b>{key}:</b> <code>{value}</code>"
            for key, value in self.config.items()
        )
        await utils.answer(message, self.strings["config"].format(data=config_data))

    @loader.command(alias="termhelp")
    async def term_help(self, message: Message):
        """Показать это сообщение"""
        help_text = """
🔥 <b>TermControl PRO v3.0.0</b>
Разработчик: @NEBULASoftware

📌 <b>Основные команды:</b>
• <code>.t &lt;команда&gt;</code> - выполнить команду
• <code>.term &lt;команда&gt;</code> - выполнить команду
• <code>.termbg &lt;команда&gt;</code> - выполнить в фоне
• <code>.termcd &lt;путь&gt;</code> - сменить директорию
• <code>.termls</code> - список файлов
• <code>.termpwd</code> - текущая директория

📊 <b>Мониторинг:</b>
• <code>.termcpu</code> - загрузка CPU
• <code>.termmem</code> - использование памяти
• <code>.termdisk</code> - место на диске
• <code>.termnet</code> - сетевые порты
• <code>.termps</code> - список процессов
• <code>.termpsgrep &lt;процесс&gt;</code> - поиск процесса
• <code>.termkill &lt;PID&gt;</code> - остановить процесс
• <code>.termwhich &lt;команда&gt;</code> - путь к команде

⭐ <b>Избранное:</b>
• <code>.fav</code> - список команд
• <code>.fav add &lt;название&gt; &lt;команда&gt;</code> - добавить
• <code>.fav remove &lt;название&gt;</code> - удалить
• <code>.fav run &lt;название&gt;</code> - выполнить
• <code>.fav edit &lt;название&gt; &lt;команда&gt;</code> - изменить

⚙️ <b>Управление:</b>
• <code>.termtoggle</code> - вкл/выкл модуль
• <code>.termconfig</code> - показать конфиг
• <code>.termclear</code> - очистить историю
• <code>.termtimeout &lt;сек&gt;</code> - установить таймаут
• <code>.termdir &lt;путь&gt;</code> - установить директорию
• <code>.termhelp</code> - это сообщение

⚠️ <b>Внимание:</b> Модуль дает полный доступ к системе!
"""
        await utils.answer(message, help_text)
# -*- coding: utf-8 -*-
# meta developer: @NEBULASoftware
# scope: hikka_only
# scope: hikka_min 1.6.2
# 📦 Linux Watcher Ultra — мониторинг пакетов и системы в Linux/Termux

__version__ = (6, 0, 0)

from .. import loader, utils
from telethon.tl.types import Message
import asyncio
import os
import json
import datetime
import platform
import hashlib
from typing import Dict, List, Tuple

@loader.tds
class LinuxWatcherUltraMod(loader.Module):
    """🖥️ Полный мониторинг Linux/Termux: пакеты, обновления, Python, система
    Разработчик: @NEBULASoftware
    Версия: 6.0.0
    
    Команды:
    🔹 .upd — главное меню и статус системы
    🔹 .pkgs [страница] [источник] — список пакетов (all/system/pip/npm)
    🔹 .pkgsearch <запрос> — поиск пакетов по имени
    🔹 .pkginfo <пакет> [источник] — подробная информация о пакете
    🔹 .pyver — список версий Python
    🔹 .updstats — статистика и обновления
    🔹 .updhistory — история проверок обновлений
    🔹 .sysinfo — информация о системе (CPU, память, диски)
    
    Примеры:
    .pkgs 2 pip          — вторая страница Python-пакетов
    .pkgsearch nginx     — поиск пакетов с nginx
    .pkginfo python      — информация о пакете python
    """
    
    strings = {
        "name": "LinuxWatcherUltra",
        "enabled": "✅ <b>Модуль включен</b>",
        "disabled": "⚠ <b>Модуль выключен</b>",
        "no_permission": "🚫 <b>Нет прав</b>",
        "fetching": "🔍 <b>Получаю информацию...</b>",
        "error": "❌ <b>Ошибка:</b> {}",
        "no_python": "❌ Python не найден",
        "main_info": (
            "📦 <b>Linux Watcher Ultra v{}</b>\n"
            "👤 Разработчик: @NEBULASoftware\n\n"
            "💻 <b>Система:</b> <code>{}</code>\n"
            "🐍 <b>Python:</b> {}\n"
            "📦 <b>Всего пакетов:</b> {}\n"
            "🔄 <b>Доступно обновлений:</b> {}\n"
            "🔐 <b>Критических:</b> {}\n\n"
            "📌 <b>Команды:</b>\n"
            "• <code>.pkgs [страница] [источник]</code> — список пакетов\n"
            "• <code>.pkgsearch &lt;запрос&gt;</code> — поиск\n"
            "• <code>.pkginfo &lt;пакет&gt; [источник]</code> — детали\n"
            "• <code>.pyver</code> — версии Python\n"
            "• <code>.updstats</code> — статистика и обновления\n"
            "• <code>.updhistory</code> — история проверок\n"
            "• <code>.sysinfo</code> — информация о системе\n"
            "<i>Источники: system, pip, npm, all (по умолч. all)</i>"
        ),
        "pkgs_header": "📦 <b>Список пакетов ({})</b>\n📊 Всего: {} | Страница {}/{}\n\n",
        "pkgs_item": "• <code>{}</code> ({}) [{}]\n",
        "no_pkgs": "❌ Пакеты не найдены.",
        "search_header": "🔍 <b>Результаты поиска: {}</b>\n📊 Найдено: {}\n\n",
        "search_item": "• <code>{}</code> ({}) [{}]\n",
        "no_search": "❌ По запросу «{}» ничего не найдено.",
        "pkg_info": (
            "📦 <b>{}</b>\n"
            "📌 <b>Версия:</b> <code>{}</code>\n"
            "📦 <b>Источник:</b> <code>{}</code>\n"
            "📝 <b>Описание:</b> <i>{}</i>\n"
        ),
        "pkg_extra": "🌐 <b>Сайт:</b> {}\n👤 <b>Автор:</b> {}\n",
        "pkg_no_desc": "Описание отсутствует",
        "stats_header": (
            "📊 <b>Статистика системы</b>\n\n"
            "💻 <b>Система:</b> <code>{}</code>\n"
            "📦 <b>Всего пакетов:</b> {}\n"
            "  • Системных: {}\n"
            "  • Python: {}\n"
            "  • NPM: {}\n"
            "🔄 <b>Доступно обновлений:</b> {}\n"
            "🔐 <b>Критических:</b> {}\n"
            "🐍 <b>Версии Python:</b>\n{}"
        ),
        "updates_sec": "🔐 <b>Критические:</b>\n{}\n",
        "updates_normal": "📦 <b>Обычные:</b>\n{}\n",
        "history_header": "📋 <b>История проверок обновлений</b>\n\n",
        "history_item": "• {} — найдено обновлений: {} (крит. {})\n",
        "no_history": "История пока пуста.",
        "sysinfo_header": "💻 <b>Информация о системе</b>\n\n",
        "sysinfo_os": "🖥️ <b>ОС:</b> <code>{}</code>",
        "sysinfo_kernel": "📀 <b>Ядро:</b> <code>{}</code>",
        "sysinfo_arch": "🔧 <b>Архитектура:</b> <code>{}</code>",
        "sysinfo_host": "🏷️ <b>Имя хоста:</b> <code>{}</code>",
        "sysinfo_cpu": "💾 <b>Процессор:</b> <code>{}</code>",
        "sysinfo_cores": "⚡ <b>Ядер:</b> <code>{}</code>",
        "sysinfo_mem": "🧠 <b>Память:</b> <code>{}</code>",
        "sysinfo_uptime": "⏱️ <b>Аптайм:</b> <code>{}</code>",
        "sysinfo_disk": "💿 <b>Диск ({}):</b> <code>{}/{} ({}%)</code>",
        "auto_on": "✅ Автопроверка включена",
        "auto_off": "❌ Автопроверка выключена"
    }
    
    strings_ru = {
        "name": "LinuxWatcherUltra",
        "enabled": "✅ <b>Модуль включен</b>",
        "disabled": "⚠ <b>Модуль выключен</b>",
        "no_permission": "🚫 <b>Нет прав</b>",
        "fetching": "🔍 <b>Получаю информацию...</b>",
        "error": "❌ <b>Ошибка:</b> {}",
        "no_python": "❌ Python не найден",
        "main_info": (
            "📦 <b>Linux Watcher Ultra v{}</b>\n"
            "👤 Разработчик: @NEBULASoftware\n\n"
            "💻 <b>Система:</b> <code>{}</code>\n"
            "🐍 <b>Python:</b> {}\n"
            "📦 <b>Всего пакетов:</b> {}\n"
            "🔄 <b>Доступно обновлений:</b> {}\n"
            "🔐 <b>Критических:</b> {}\n\n"
            "📌 <b>Команды:</b>\n"
            "• <code>.pkgs [страница] [источник]</code> — список пакетов\n"
            "• <code>.pkgsearch &lt;запрос&gt;</code> — поиск\n"
            "• <code>.pkginfo &lt;пакет&gt; [источник]</code> — детали\n"
            "• <code>.pyver</code> — версии Python\n"
            "• <code>.updstats</code> — статистика и обновления\n"
            "• <code>.updhistory</code> — история проверок\n"
            "• <code>.sysinfo</code> — информация о системе\n"
            "<i>Источники: system, pip, npm, all (по умолч. all)</i>"
        ),
        "pkgs_header": "📦 <b>Список пакетов ({})</b>\n📊 Всего: {} | Страница {}/{}\n\n",
        "pkgs_item": "• <code>{}</code> ({}) [{}]\n",
        "no_pkgs": "❌ Пакеты не найдены.",
        "search_header": "🔍 <b>Результаты поиска: {}</b>\n📊 Найдено: {}\n\n",
        "search_item": "• <code>{}</code> ({}) [{}]\n",
        "no_search": "❌ По запросу «{}» ничего не найдено.",
        "pkg_info": (
            "📦 <b>{}</b>\n"
            "📌 <b>Версия:</b> <code>{}</code>\n"
            "📦 <b>Источник:</b> <code>{}</code>\n"
            "📝 <b>Описание:</b> <i>{}</i>\n"
        ),
        "pkg_extra": "🌐 <b>Сайт:</b> {}\n👤 <b>Автор:</b> {}\n",
        "pkg_no_desc": "Описание отсутствует",
        "stats_header": (
            "📊 <b>Статистика системы</b>\n\n"
            "💻 <b>Система:</b> <code>{}</code>\n"
            "📦 <b>Всего пакетов:</b> {}\n"
            "  • Системных: {}\n"
            "  • Python: {}\n"
            "  • NPM: {}\n"
            "🔄 <b>Доступно обновлений:</b> {}\n"
            "🔐 <b>Критических:</b> {}\n"
            "🐍 <b>Версии Python:</b>\n{}"
        ),
        "updates_sec": "🔐 <b>Критические:</b>\n{}\n",
        "updates_normal": "📦 <b>Обычные:</b>\n{}\n",
        "history_header": "📋 <b>История проверок обновлений</b>\n\n",
        "history_item": "• {} — найдено обновлений: {} (крит. {})\n",
        "no_history": "История пока пуста.",
        "sysinfo_header": "💻 <b>Информация о системе</b>\n\n",
        "sysinfo_os": "🖥️ <b>ОС:</b> <code>{}</code>",
        "sysinfo_kernel": "📀 <b>Ядро:</b> <code>{}</code>",
        "sysinfo_arch": "🔧 <b>Архитектура:</b> <code>{}</code>",
        "sysinfo_host": "🏷️ <b>Имя хоста:</b> <code>{}</code>",
        "sysinfo_cpu": "💾 <b>Процессор:</b> <code>{}</code>",
        "sysinfo_cores": "⚡ <b>Ядер:</b> <code>{}</code>",
        "sysinfo_mem": "🧠 <b>Память:</b> <code>{}</code>",
        "sysinfo_uptime": "⏱️ <b>Аптайм:</b> <code>{}</code>",
        "sysinfo_disk": "💿 <b>Диск ({}):</b> <code>{}/{} ({}%)</code>",
        "auto_on": "✅ Автопроверка включена",
        "auto_off": "❌ Автопроверка выключена"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("is_active", True, "Активность модуля", validator=loader.validators.Boolean()),
            loader.ConfigValue("auto_check", True, "Автопроверка обновлений", validator=loader.validators.Boolean()),
            loader.ConfigValue("check_interval", 86400, "Интервал проверки (секунд)", validator=loader.validators.Integer(minimum=3600)),
            loader.ConfigValue("ignored_packages", [], "Пакеты для игнорирования", validator=loader.validators.Series()),
            loader.ConfigValue("allowed_users", [], "ID разрешенных пользователей", validator=loader.validators.Series()),
            loader.ConfigValue("items_per_page", 10, "Количество пакетов на странице", validator=loader.validators.Integer(minimum=5, maximum=25)),
            loader.ConfigValue("keep_history", True, "Сохранять историю проверок", validator=loader.validators.Boolean())
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.me = await client.get_me()
        self.user_hash = hashlib.md5(str(self.me.id).encode()).hexdigest()[:16]
        self.system_type = await self._detect_system()
        self.python_versions = await self._detect_python_versions()
        self.update_history = self.db.get("LinuxWatcherUltra", "update_history", [])
        
        if self.config["auto_check"]:
            asyncio.create_task(self._auto_checker())

    async def _run_cmd(self, cmd: list) -> Tuple[str, str, int]:
        """Запустить команду, вернуть stdout, stderr, код"""
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            return stdout.decode('utf-8', errors='ignore'), stderr.decode('utf-8', errors='ignore'), proc.returncode
        except Exception as e:
            return '', str(e), -1

    async def _detect_system(self):
        if os.path.exists('/data/data/com.termux'):
            return 'termux'
        for pkg_mgr in ['apt', 'yum', 'pacman']:
            _, _, code = await self._run_cmd(['which', pkg_mgr])
            if code == 0:
                return pkg_mgr
        return 'unknown'

    async def _detect_python_versions(self):
        versions = {}
        if self.system_type == 'termux':
            prefix = os.environ.get('PREFIX', '/data/data/com.termux/files/usr')
            bin_dir = os.path.join(prefix, 'bin')
            if not os.path.isdir(bin_dir):
                return versions
            for f in os.listdir(bin_dir):
                if f.startswith('python') and os.access(os.path.join(bin_dir, f), os.X_OK):
                    if f.endswith('-config'):
                        continue
                    out, _, _ = await self._run_cmd([os.path.join(bin_dir, f), '--version'])
                    if 'Python' in out:
                        versions[f] = out.strip()
        else:
            out, _, _ = await self._run_cmd(['ls', '/usr/bin/python*'])
            for line in out.splitlines():
                path = line.strip()
                base = os.path.basename(path)
                if base.startswith('python') and not base.endswith('-config') and os.access(path, os.X_OK):
                    ver_out, _, _ = await self._run_cmd([path, '--version'])
                    if 'Python' in ver_out:
                        versions[base] = ver_out.strip()
        return versions

    async def _check_permission(self, message: Message) -> bool:
        if not self.config["is_active"]:
            await utils.answer(message, self.strings["disabled"])
            return False
        if message.sender_id == self.me.id or message.sender_id in self.config["allowed_users"]:
            return True
        await utils.answer(message, self.strings("no_permission"))
        return False

    async def _get_packages(self, source: str = 'system') -> List[Dict]:
        packages = []
        try:
            if source in ('system', 'all'):
                if self.system_type == 'termux':
                    out, _, _ = await self._run_cmd(['pkg', 'list-installed'])
                    for line in out.splitlines()[1:]:
                        if '/' in line:
                            name = line.split('/')[0].strip()
                            ver = line.split('/')[1].split()[0] if len(line.split('/')) > 1 else '?'
                            packages.append({'name': name, 'version': ver, 'source': 'termux', 'type': 'system'})
                elif self.system_type == 'apt':
                    out, _, _ = await self._run_cmd(['dpkg', '-l'])
                    for line in out.splitlines():
                        if line.startswith('ii'):
                            parts = line.split()
                            if len(parts) >= 3:
                                packages.append({'name': parts[1], 'version': parts[2], 'source': 'deb', 'type': 'system'})
            if source in ('pip', 'all'):
                for cmd in ['pip', 'pip3']:
                    out, _, code = await self._run_cmd([cmd, 'list', '--format=json'])
                    if code == 0 and out:
                        try:
                            data = json.loads(out)
                            for pkg in data:
                                packages.append({'name': pkg['name'], 'version': pkg['version'], 'source': cmd, 'type': 'python'})
                        except:
                            pass
            if source in ('npm', 'all'):
                out, _, code = await self._run_cmd(['npm', 'list', '-g', '--depth=0', '--json'])
                if code == 0 and out:
                    try:
                        data = json.loads(out)
                        if 'dependencies' in data:
                            for name, info in data['dependencies'].items():
                                packages.append({'name': name, 'version': info.get('version', '?'), 'source': 'npm', 'type': 'node'})
                    except:
                        pass
        except:
            pass
        return sorted(packages, key=lambda x: x['name'].lower())

    async def _get_updates(self) -> Dict:
        updates = {'total': 0, 'security': [], 'normal': []}
        try:
            if self.system_type == 'termux':
                await self._run_cmd(['pkg', 'update'])
                out, _, _ = await self._run_cmd(['pkg', 'list-upgradable'])
                for line in out.splitlines()[1:]:
                    pkg = line.strip()
                    if pkg and pkg not in self.config["ignored_packages"]:
                        updates['normal'].append(pkg)
                        updates['total'] += 1
            elif self.system_type == 'apt':
                await self._run_cmd(['apt', 'update'])
                out, _, _ = await self._run_cmd(['apt', 'list', '--upgradable'])
                for line in out.splitlines():
                    if '/' in line and 'upgradable' in line:
                        pkg = line.split('/')[0]
                        if pkg not in self.config["ignored_packages"]:
                            if '-security' in line:
                                updates['security'].append(pkg)
                            else:
                                updates['normal'].append(pkg)
                            updates['total'] += 1
        except:
            pass
        return updates

    async def _get_package_info(self, name: str, source: str = None) -> Dict:
        info = {'name': name, 'version': '?', 'description': self.strings("pkg_no_desc"), 'source': source or 'unknown', 'homepage': '', 'author': ''}
        try:
            if source in ('termux', 'deb', None) and self.system_type in ('termux', 'apt'):
                out, _, _ = await self._run_cmd(['apt', 'show', name])
                for line in out.splitlines():
                    if line.startswith('Version:'):
                        info['version'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Description:'):
                        desc = line.split(':', 1)[1].strip()
                        if desc:
                            info['description'] = desc
                    elif line.startswith('Homepage:'):
                        info['homepage'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Maintainer:'):
                        info['author'] = line.split(':', 1)[1].strip()
            elif source in ('pip', 'pip3'):
                out, _, _ = await self._run_cmd([source, 'show', name])
                for line in out.splitlines():
                    if line.startswith('Version:'):
                        info['version'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Summary:'):
                        desc = line.split(':', 1)[1].strip()
                        if desc:
                            info['description'] = desc
                    elif line.startswith('Author:'):
                        info['author'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Home-page:'):
                        info['homepage'] = line.split(':', 1)[1].strip()
            elif source == 'npm':
                out, _, code = await self._run_cmd(['npm', 'show', name, '--json'])
                if code == 0 and out:
                    data = json.loads(out)
                    info['version'] = data.get('version', '?')
                    info['description'] = data.get('description', self.strings("pkg_no_desc"))
                    info['author'] = data.get('author', {}).get('name', '') if isinstance(data.get('author'), dict) else data.get('author', '')
                    info['homepage'] = data.get('homepage', '')
        except:
            pass
        return info

    async def _get_sysinfo(self) -> Dict:
        """Собрать информацию о системе"""
        info = {}
        try:
            # ОС
            info['os'] = platform.system()
            info['release'] = platform.release()
            info['arch'] = platform.machine()
            info['hostname'] = platform.node()
            
            # CPU
            if os.path.exists('/proc/cpuinfo'):
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read()
                    for line in cpuinfo.split('\n'):
                        if 'model name' in line:
                            info['cpu'] = line.split(':')[1].strip()
                            break
                    info['cores'] = cpuinfo.count('processor')
            else:
                info['cpu'] = platform.processor() or 'Unknown'
                info['cores'] = os.cpu_count() or 'Unknown'
            
            # Память
            if os.path.exists('/proc/meminfo'):
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                    mem_total = 0
                    mem_available = 0
                    for line in meminfo.split('\n'):
                        if 'MemTotal' in line:
                            mem_total = int(line.split()[1]) * 1024
                        if 'MemAvailable' in line:
                            mem_available = int(line.split()[1]) * 1024
                    if mem_total:
                        mem_used = mem_total - mem_available
                        info['mem_total'] = self._bytes_to_human(mem_total)
                        info['mem_used'] = self._bytes_to_human(mem_used)
                        info['mem_percent'] = round((mem_used / mem_total) * 100, 1)
            
            # Аптайм
            if os.path.exists('/proc/uptime'):
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.readline().split()[0])
                    days = int(uptime_seconds // 86400)
                    hours = int((uptime_seconds % 86400) // 3600)
                    minutes = int((uptime_seconds % 3600) // 60)
                    info['uptime'] = f"{days}д {hours}ч {minutes}м"
            
            # Диск
            if os.path.exists('/'):
                stat = os.statvfs('/')
                disk_total = stat.f_frsize * stat.f_blocks
                disk_free = stat.f_frsize * stat.f_bfree
                disk_used = disk_total - disk_free
                info['disk_total'] = self._bytes_to_human(disk_total)
                info['disk_used'] = self._bytes_to_human(disk_used)
                info['disk_percent'] = round((disk_used / disk_total) * 100, 1)
        except:
            pass
        return info

    def _bytes_to_human(self, bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.1f}{unit}"
            bytes /= 1024
        return f"{bytes:.1f}TB"

    @loader.command()
    async def upd(self, message: Message):
        """Главное меню, информация о модуле"""
        if not await self._check_permission(message):
            return
        py_list = ', '.join(self.python_versions.keys()) if self.python_versions else 'не найдено'
        pkgs = await self._get_packages('all')
        updates = await self._get_updates()
        total_pkgs = len(pkgs)
        total_updates = updates['total']
        critical = len(updates['security'])
        text = self.strings("main_info").format(
            f"{__version__[0]}.{__version__[1]}.{__version__[2]}",
            self.system_type,
            py_list,
            total_pkgs,
            total_updates,
            critical
        )
        await utils.answer(message, text)

    @loader.command()
    async def pkgs(self, message: Message):
        """Список пакетов. Использование: .pkgs [страница] [источник] (system/pip/npm/all)"""
        if not await self._check_permission(message):
            return
        args = utils.get_args_raw(message).split()
        page = 0
        source = 'all'
        if args:
            try:
                page = int(args[0]) - 1
                if page < 0:
                    page = 0
                if len(args) > 1:
                    source = args[1]
            except ValueError:
                source = args[0]
        msg = await utils.answer(message, self.strings("fetching"))
        pkgs = await self._get_packages(source)
        if not pkgs:
            await utils.answer(msg, self.strings("no_pkgs"))
            return
        total = len(pkgs)
        per_page = self.config["items_per_page"]
        start = page * per_page
        end = start + per_page
        page_pkgs = pkgs[start:end]
        total_pages = (total + per_page - 1) // per_page
        text = self.strings("pkgs_header").format(source, total, page+1, total_pages)
        for p in page_pkgs:
            text += self.strings("pkgs_item").format(p['name'], p['version'], p['source'])
        text += f"\n📌 Используй: <code>.pkgs [страница] [источник]</code>"
        await utils.answer(msg, text)

    @loader.command()
    async def pkgsearch(self, message: Message):
        """Поиск пакетов по имени. Использование: .pkgsearch <запрос>"""
        if not await self._check_permission(message):
            return
        query = utils.get_args_raw(message)
        if not query:
            await utils.answer(message, "❌ Укажите поисковый запрос. Пример: .pkgsearch python")
            return
        msg = await utils.answer(message, self.strings("fetching"))
        pkgs = await self._get_packages('all')
        results = [p for p in pkgs if query.lower() in p['name'].lower()]
        if not results:
            await utils.answer(msg, self.strings("no_search").format(query))
            return
        text = self.strings("search_header").format(query, len(results))
        for p in results[:20]:
            text += self.strings("search_item").format(p['name'], p['version'], p['source'])
        if len(results) > 20:
            text += f"\n... и ещё {len(results) - 20}"
        await utils.answer(msg, text)

    @loader.command()
    async def pkginfo(self, message: Message):
        """Детальная информация о пакете. Использование: .pkginfo <пакет> [источник]"""
        if not await self._check_permission(message):
            return
        args = utils.get_args_raw(message).split()
        if not args:
            await utils.answer(message, "❌ Укажите имя пакета. Пример: .pkginfo python")
            return
        pkg_name = args[0]
        source = args[1] if len(args) > 1 else None
        msg = await utils.answer(message, self.strings("fetching"))
        info = await self._get_package_info(pkg_name, source)
        text = self.strings("pkg_info").format(info['name'], info['version'], info['source'], info['description'])
        if info['homepage'] or info['author']:
            text += self.strings("pkg_extra").format(info['homepage'] or '—', info['author'] or '—')
        await utils.answer(msg, text)

    @loader.command()
    async def pyver(self, message: Message):
        """Список установленных версий Python"""
        if not await self._check_permission(message):
            return
        text = "🐍 <b>Установленные версии Python</b>\n\n"
        if self.python_versions:
            for ver, full in self.python_versions.items():
                text += f"• <code>{ver}</code>: {full}\n"
        else:
            text += self.strings("no_python")
        await utils.answer(message, text)

    @loader.command()
    async def updstats(self, message: Message):
        """Статистика системы и доступные обновления"""
        if not await self._check_permission(message):
            return
        msg = await utils.answer(message, self.strings("fetching"))
        pkgs = await self._get_packages('all')
        updates = await self._get_updates()
        sys_count = len([p for p in pkgs if p['type'] == 'system'])
        py_count = len([p for p in pkgs if p['type'] == 'python'])
        npm_count = len([p for p in pkgs if p['type'] == 'node'])
        py_text = ""
        if self.python_versions:
            for ver, full in self.python_versions.items():
                py_text += f"  • {ver}: {full}\n"
        else:
            py_text = f"  • {self.strings('no_python')}\n"
        text = self.strings("stats_header").format(
            self.system_type,
            len(pkgs),
            sys_count,
            py_count,
            npm_count,
            updates['total'],
            len(updates['security']),
            py_text
        )
        if updates['security']:
            sec_list = "\n".join(f"  • {p}" for p in updates['security'][:5])
            text += self.strings("updates_sec").format(sec_list)
        if updates['normal']:
            norm_list = "\n".join(f"  • {p}" for p in updates['normal'][:10])
            text += self.strings("updates_normal").format(norm_list)
        if not updates['security'] and not updates['normal']:
            text += self.strings("no_updates")
        await utils.answer(msg, text)

    @loader.command()
    async def updhistory(self, message: Message):
        """История проверок обновлений"""
        if not await self._check_permission(message):
            return
        if not self.update_history:
            await utils.answer(message, self.strings("no_history"))
            return
        text = self.strings("history_header")
        for entry in self.update_history[-10:]:
            text += self.strings("history_item").format(
                entry['date'],
                entry['total'],
                entry['critical']
            )
        await utils.answer(message, text)

    @loader.command()
    async def sysinfo(self, message: Message):
        """Информация о системе: CPU, память, диск, аптайм"""
        if not await self._check_permission(message):
            return
        msg = await utils.answer(message, self.strings("fetching"))
        info = await self._get_sysinfo()
        text = self.strings("sysinfo_header")
        text += self.strings("sysinfo_os").format(info.get('os', 'Unknown')) + "\n"
        text += self.strings("sysinfo_kernel").format(info.get('release', 'Unknown')) + "\n"
        text += self.strings("sysinfo_arch").format(info.get('arch', 'Unknown')) + "\n"
        text += self.strings("sysinfo_host").format(info.get('hostname', 'Unknown')) + "\n"
        text += self.strings("sysinfo_cpu").format(info.get('cpu', 'Unknown')) + "\n"
        text += self.strings("sysinfo_cores").format(info.get('cores', 'Unknown')) + "\n"
        if 'mem_used' in info:
            text += self.strings("sysinfo_mem").format(f"{info['mem_used']}/{info['mem_total']} ({info['mem_percent']}%)") + "\n"
        if 'uptime' in info:
            text += self.strings("sysinfo_uptime").format(info['uptime']) + "\n"
        if 'disk_used' in info:
            text += self.strings("sysinfo_disk").format(
                '/',
                info['disk_used'],
                info['disk_total'],
                info['disk_percent']
            ) + "\n"
        await utils.answer(msg, text)

    async def _auto_checker(self):
        while self.config["auto_check"]:
            try:
                updates = await self._get_updates()
                if updates['total'] > 0:
                    if self.config["keep_history"]:
                        entry = {
                            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            'total': updates['total'],
                            'critical': len(updates['security'])
                        }
                        self.update_history.append(entry)
                        if len(self.update_history) > 50:
                            self.update_history = self.update_history[-50:]
                        self.db.set("LinuxWatcherUltra", "update_history", self.update_history)
                    if updates['security']:
                        text = f"🚨 <b>Критические обновления!</b>\n"
                        for pkg in updates['security'][:5]:
                            text += f"• {pkg}\n"
                        await self.client.send_message(self.me.id, text)
                await asyncio.sleep(self.config["check_interval"])
            except:
                await asyncio.sleep(3600)
# meta developer: @NEBULASoftware
# scope: hikka_only
# scope: hikka_min 1.6.2
# 🔗 Link Scanner PRO — мощный локальный антивирус для ссылок
# ⚠️ Обнаруживает вредоносные URL, RAT-панели, майнеры, фишинг и C2 серверы

from .. import loader, utils
from telethon.tl.types import Message
import re
import aiohttp
import asyncio
import json
import hashlib
import time
import ipaddress
import socket
from urllib.parse import urlparse, unquote
from collections import defaultdict

@loader.tds
class LinkScannerMod(loader.Module):
    """🛡️ Сканер ссылок на вирусы, RAT-панели и майнеры
    Команды:
    .scan <ссылка/ответ> - сканировать ссылки
    .deepscan <ссылка/ответ> - глубокое сканирование с проверкой IP
    .scanstats - статистика работы
    .clearcache - очистить кэш
    .addthreat <тип> <паттерн> - добавить свой паттерн
    .whitelist add/remove/list - управление белым списком"""
    
    strings = {
        "name": "LinkScannerPRO",
        "processing": "🔄 Сканирую ссылки...",
        "clean": "✅ Все ссылки чистые",
        "danger": "🚨 ОБНАРУЖЕНА УГРОЗА",
        "no_links": "❌ Ссылок не найдено",
        "stats": "📊 Статистика сканирования",
        "error": "❌ Ошибка при сканировании: {}",
        "deep_scan": "🔍 Глубокое сканирование завершено",
        "cache_cleared": "🧹 Кэш сканера очищен",
        "db_updated": "📚 Локальная база обновлена ({} записей)",
        "ip_threat": "⚠️ Опасный IP: {} ({} детекций)",
        "help": "🛡️ LinkScanner PRO - защита от вредоносных ссылок\n\n"
                "📌 Доступные команды:\n"
                "• .scan <ссылка/ответ> - проверить ссылки на угрозы\n"
                "• .deepscan <ссылка/ответ> - глубокая проверка с анализом IP\n"
                "• .scanstats - статистика работы сканера\n"
                "• .clearcache - очистить временный кэш\n"
                "• .addthreat <тип> <паттерн> - добавить свой паттерн\n"
                "• .whitelist add <домен> - добавить домен в белый список\n"
                "• .whitelist remove <домен> - удалить из белого списка\n"
                "• .whitelist list - показать белый список"
    }
    
    strings_ru = {
        "name": "LinkScannerPRO",
        "processing": "🔄 Сканирую ссылки...",
        "clean": "✅ Все ссылки чистые",
        "danger": "🚨 ОБНАРУЖЕНА УГРОЗА",
        "no_links": "❌ Ссылок не найдено",
        "stats": "📊 Статистика сканирования",
        "error": "❌ Ошибка при сканировании: {}",
        "deep_scan": "🔍 Глубокое сканирование завершено",
        "cache_cleared": "🧹 Кэш сканера очищен",
        "db_updated": "📚 Локальная база обновлена ({} записей)",
        "ip_threat": "⚠️ Опасный IP: {} ({} детекций)",
        "help": "🛡️ LinkScanner PRO - защита от вредоносных ссылок\n\n"
                "📌 Доступные команды:\n"
                "• .scan <ссылка/ответ> - проверить ссылки на угрозы\n"
                "• .deepscan <ссылка/ответ> - глубокая проверка с анализом IP\n"
                "• .scanstats - статистика работы сканера\n"
                "• .clearcache - очистить временный кэш\n"
                "• .addthreat <тип> <паттерн> - добавить свой паттерн\n"
                "• .whitelist add <домен> - добавить домен в белый список\n"
                "• .whitelist remove <домен> - удалить из белого списка\n"
                "• .whitelist list - показать белый список"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "auto_scan",
                True,
                "Автоматически сканировать ссылки в чатах",
                validator=None
            ),
            loader.ConfigValue(
                "deep_dns_check",
                True,
                "Проверять DNS и IP репутацию",
                validator=None
            ),
            loader.ConfigValue(
                "heuristic_analysis",
                True,
                "Использовать эвристический анализ",
                validator=None
            ),
            loader.ConfigValue(
                "min_danger_level",
                2,
                "Минимальный уровень опасности для оповещения (1-10)",
                validator=None
            )
        )
        
        self.whitelist = [
            "google.com", "www.google.com", "accounts.google.com", "mail.google.com", "drive.google.com", "docs.google.com", "photos.google.com", "play.google.com", "maps.google.com", "news.google.com", "translate.google.com", "calendar.google.com", "contacts.google.com", "hangouts.google.com", "keep.google.com", "classroom.google.com", "scholar.google.com", "trends.google.com", "adwords.google.com", "analytics.google.com",
            "youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "music.youtube.com", "kids.youtube.com", "studio.youtube.com", "tv.youtube.com",
            "github.com", "www.github.com", "raw.githubusercontent.com", "gist.github.com", "api.github.com", "help.github.com", "docs.github.com", "pages.github.com", "lab.github.com", "education.github.com", "marketplace.github.com", "github.io",
            "telegram.org", "www.telegram.org", "core.telegram.org", "translations.telegram.org", "telegram.dog", "telegram.me", "t.me", "desktop.telegram.org", "telegram.org/blog", "telegram.org/privacy", "telegram.org/tos",
            "microsoft.com", "www.microsoft.com", "account.microsoft.com", "support.microsoft.com", "docs.microsoft.com", "learn.microsoft.com", "azure.microsoft.com", "visualstudio.microsoft.com", "office.microsoft.com", "microsoft365.com", "outlook.live.com", "hotmail.com", "live.com", "msn.com", "bing.com", "www.bing.com", "bing.net",
            "apple.com", "www.apple.com", "support.apple.com", "developer.apple.com", "icloud.com", "appleid.apple.com", "music.apple.com", "tv.apple.com", "apps.apple.com", "books.apple.com", "podcasts.apple.com", "news.apple.com", "apple.com/ru", "apple.com/us",
            "yandex.ru", "www.yandex.ru", "yandex.by", "yandex.kz", "yandex.com", "ya.ru", "mail.yandex.ru", "disk.yandex.ru", "music.yandex.ru", "kinopoisk.ru", "yandex.ru/maps", "yandex.ru/news", "yandex.ru/weather", "yandex.ru/time", "yandex.ru/afisha", "yandex.ru/taxi", "yandex.ru/eda", "yandex.ru/market", "yandex.ru/travel",
            "mail.ru", "www.mail.ru", "e.mail.ru", "cloud.mail.ru", "my.mail.ru", "agent.mail.ru", "calendar.mail.ru", "games.mail.ru", "hi-tech.mail.ru", "health.mail.ru", "horo.mail.ru", "lady.mail.ru", "news.mail.ru", "otvet.mail.ru", "pogoda.mail.ru", "tv.mail.ru", "vk.com", "www.vk.com", "m.vk.com", "vk.ru", "vk.me", "login.vk.com", "api.vk.com", "vk.com/feed", "vk.com/im", "vk.com/albums", "vk.com/videos", "vk.com/music", "vk.com/docs",
            "ok.ru", "www.ok.ru", "m.ok.ru", "ok.me", "api.ok.ru", "ok.ru/live", "ok.ru/video", "ok.ru/music", "ok.ru/games", "ok.ru/group",
            "facebook.com", "www.facebook.com", "m.facebook.com", "fb.com", "fb.me", "facebookcorewwwi.onion", "developers.facebook.com", "business.facebook.com", "newsroom.fb.com", "messenger.com", "www.messenger.com", "m.me", "instagram.com", "www.instagram.com", "m.instagram.com", "instagr.am", "instagram.frix4-1.fna.fbcdn.net", "cdninstagram.com", "twitter.com", "www.twitter.com", "m.twitter.com", "t.co", "twitter.co", "api.twitter.com", "help.twitter.com", "about.twitter.com", "blog.twitter.com", "community.twitter.com", "x.com", "www.x.com", "pinterest.com", "www.pinterest.com", "pin.it", "linkedin.com", "www.linkedin.com", "linkedin.cn", "lnkd.in", "tumblr.com", "www.tumblr.com", "t.umblr.com", "reddit.com", "www.reddit.com", "redd.it", "redditblog.com", "discord.com", "www.discord.com", "discord.gg", "discordapp.com", "cdn.discordapp.com", "media.discordapp.net", "twitch.tv", "www.twitch.tv", "twitch.tv/videos", "twitch.tv/directory", "tiktok.com", "www.tiktok.com", "tiktokv.com", "snapchat.com", "www.snapchat.com", "whatsapp.com", "www.whatsapp.com", "whatsapp.net", "wa.me", "web.whatsapp.com", "viber.com", "www.viber.com", "line.me", "www.line.me", "wechat.com", "www.wechat.com", "qq.com", "www.qq.com",
            "wikipedia.org", "www.wikipedia.org", "ru.wikipedia.org", "en.wikipedia.org", "commons.wikimedia.org", "wikimedia.org", "wiktionary.org", "wikiquote.org", "wikibooks.org", "wikisource.org", "wikinews.org", "wikiversity.org", "wikivoyage.org", "wikidata.org", "mediawiki.org", "stackoverflow.com", "www.stackoverflow.com", "stackexchange.com", "serverfault.com", "superuser.com", "stackoverflow.co", "stackoverflow.blog", "gitlab.com", "www.gitlab.com", "gitlab.net", "gitlab.org", "docs.gitlab.com", "forum.gitlab.com", "bitbucket.org", "www.bitbucket.org", "bitbucket.net", "api.bitbucket.org", "atlassian.com", "www.atlassian.com", "atlassian.net", "docker.com", "www.docker.com", "hub.docker.com", "docs.docker.com", "forums.docker.com", "pypi.org", "www.pypi.org", "pypi.io", "warehouse.pypi.org", "python.org", "www.python.org", "docs.python.org", "pypi.python.org", "npmjs.com", "www.npmjs.com", "npm.im", "docs.npmjs.com", "status.npmjs.org", "maven.org", "www.maven.org", "repo.maven.org", "search.maven.org", "mvnrepository.com", "www.mvnrepository.com", "jetbrains.com", "www.jetbrains.com", "plugins.jetbrains.com", "blog.jetbrains.com", "adobe.com", "www.adobe.com", "adobe.io", "helpx.adobe.com", "community.adobe.com", "behance.net", "www.behance.net", "creativecloud.adobe.com", "spotify.com", "www.spotify.com", "open.spotify.com", "play.spotify.com", "support.spotify.com", "newsroom.spotify.com", "netflix.com", "www.netflix.com", "help.netflix.com", "jobs.netflix.com", "research.netflix.com", "amazon.com", "www.amazon.com", "amazon.co.uk", "amazon.de", "amazon.fr", "amazon.it", "amazon.es", "amazon.ca", "amazon.cn", "amazon.in", "amazon.co.jp", "aws.amazon.com", "primevideo.com", "www.primevideo.com", "audible.com", "goodreads.com", "imdb.com", "www.imdb.com", "pro.imdb.com", "boxofficemojo.com", "ebay.com", "www.ebay.com", "ebay.co.uk", "ebay.de", "ebay.fr", "ebay.it", "ebay.es", "ebay.ca", "ebay.com.au", "ebay.in", "ebay.cn", "paypal.com", "www.paypal.com", "paypal.me", "developer.paypal.com", "paypal-community.com", "paypalobjects.com", "stripe.com", "www.stripe.com", "dashboard.stripe.com", "stripe.net", "cloudflare.com", "www.cloudflare.com", "cloudflare.net", "cloudflareinsights.com", "cloudflare-ips.com", "support.cloudflare.com", "community.cloudflare.com", "cloudflare.com/ru", "duckduckgo.com", "www.duckduckgo.com", "duck.co", "safe.duckduckgo.com", "start.duckduckgo.com", "nginx.com", "www.nginx.com", "nginx.org", "forum.nginx.org", "nginx.com/resources", "apache.org", "www.apache.org", "apache.net", "archive.apache.org", "cwiki.apache.org", "tomcat.apache.org", "httpd.apache.org", "ubuntu.com", "www.ubuntu.com", "ubuntu.ru", "ubuntu.net", "help.ubuntu.com", "askubuntu.com", "debian.org", "www.debian.org", "debian.net", "debian.ru", "wiki.debian.org", "packages.debian.org", "centos.org", "www.centos.org", "wiki.centos.org", "forums.centos.org", "redhat.com", "www.redhat.com", "redhat.net", "access.redhat.com", "developers.redhat.com", "fedora.org", "www.fedora.org", "fedoraproject.org", "getfedora.org", "archlinux.org", "www.archlinux.org", "wiki.archlinux.org", "bbs.archlinux.org", "aur.archlinux.org", "manjaro.org", "manjaro.ru", "manjaro.net", "gentoo.org", "www.gentoo.org", "gentoo.ru", "alpinelinux.org", "www.alpinelinux.org", "oracle.com", "www.oracle.com", "oracle.net", "docs.oracle.com", "support.oracle.com", "java.com", "www.java.com", "oracle.com/java", "openjdk.org", "jdk.java.net", "adoptopenjdk.net", "spring.io", "www.spring.io", "spring.net", "docs.spring.io", "spring.io/blog", "hibernate.org", "hibernate.net", "www.hibernate.org", "mysql.com", "www.mysql.com", "dev.mysql.com", "forums.mysql.com", "postgresql.org", "www.postgresql.org", "postgres.net", "wiki.postgresql.org", "docs.postgresql.org", "mongodb.com", "www.mongodb.com", "mongodb.net", "docs.mongodb.com", "university.mongodb.com", "redis.io", "www.redis.io", "redis.net", "redis.com", "elastic.co", "www.elastic.co", "elastic.net", "elastic.co/blog", "elastic.co/guide", "docker.com", "www.docker.com", "kubernetes.io", "kubernetes.net", "k8s.io", "www.kubernetes.io", "kubernetes.io/blog", "kubernetes.io/docs", "openshift.com", "www.openshift.com", "openshift.net", "okd.io", "www.okd.io", "ansible.com", "www.ansible.com", "ansible.net", "docs.ansible.com", "galaxy.ansible.com", "terraform.io", "terraform.io/docs", "terraform.io/intro", "consul.io", "vaultproject.io", "nomadproject.io", "packer.io",
            "cnn.com", "www.cnn.com", "bbc.com", "www.bbc.com", "bbc.co.uk", "bbcnews.com", "nytimes.com", "www.nytimes.com", "nytimes.net", "wsj.com", "www.wsj.com", "wsj.net", "washingtonpost.com", "www.washingtonpost.com", "theguardian.com", "www.theguardian.com", "guardian.co.uk", "reuters.com", "www.reuters.com", "reuters.net", "bloomberg.com", "www.bloomberg.com", "bloomberg.net", "forbes.com", "www.forbes.com", "forbes.net", "businessinsider.com", "www.businessinsider.com", "techcrunch.com", "www.techcrunch.com", "techcrunch.net", "thenextweb.com", "thenextweb.net", "theverge.com", "www.theverge.com", "vox.com", "www.vox.com", "voxmedia.com", "medium.com", "www.medium.com", "medium.net", "blogger.com", "www.blogger.com", "blogspot.com", "blogspot.ru", "wordpress.com", "www.wordpress.com", "wordpress.org", "wordpress.net", "tumblr.com", "www.tumblr.com", "livejournal.com", "www.livejournal.com", "livejournal.ru", "habr.com", "www.habr.com", "habr.ru", "habrahabr.ru", "habrastorage.org", "tproger.ru", "www.tproger.ru", "tproger.com", "geektimes.ru", "geektimes.com", "pikabu.ru", "www.pikabu.ru", "pikabu.com", "dtf.ru", "www.dtf.ru", "dtf.net", "vc.ru", "www.vc.ru", "vc.com", "tjournal.ru", "tjournal.com", "tjournal.net",
            "zoom.us", "www.zoom.us", "zoom.com", "skype.com", "www.skype.com", "skype.net", "teams.microsoft.com", "slack.com", "www.slack.com", "slack.net", "slackhq.com", "trello.com", "www.trello.com", "trello.net", "asana.com", "www.asana.com", "asana.net", "notion.so", "www.notion.so", "notion.com", "miro.com", "www.miro.com", "miro.net", "figma.com", "www.figma.com", "figma.net", "canva.com", "www.canva.com", "canva.net", "dropbox.com", "www.dropbox.com", "dropbox.net", "dropbox.tech", "onedrive.live.com", "box.com", "www.box.com", "box.net", "mega.nz", "www.mega.nz", "mega.io", "google.drive.com", "icloud.com", "www.icloud.com", "icloud.net", "yandex.disk.ru", "cloud.mail.ru", "disk.yandex.ru"
        ]

        self.malicious_patterns = {
            "rat_panels": [
                r"njrat.*\.(?:net|com|org|ru|xyz|top|club)",
                r"quasar.*\.(?:net|com|org|info|online)",
                r"asyncrat.*\.(?:net|com|org)",
                r"nanocore.*\.(?:net|com|org)",
                r"darkrat.*\.(?:net|com|org)",
                r"lime.*rat.*\.(?:net|com|org)",
                r"xworm.*\.(?:net|com|org)",
                r"remcos.*\.(?:net|com|org)",
                r"agenttesla.*\.(?:net|com|org)",
                r"formbook.*\.(?:net|com|org)",
                r"lokibot.*\.(?:net|com|org)",
                r"azorult.*\.(?:net|com|org)",
                r"vidar.*\.(?:net|com|org)",
                r"predator.*rat.*\.(?:net|com|org)",
                r"orcus.*\.(?:net|com|org)",
                r"blackshades.*\.(?:net|com|org)",
                r"cybergate.*\.(?:net|com|org)",
                r"darkcomet.*\.(?:net|com|org)",
                r"havex.*\.(?:net|com|org)",
                r"ratpanel.*\.(?:net|com|org)",
                r"c2server.*\.(?:net|com|org)"
            ],
            "miners": [
                r"pool\.minexmr\.com",
                r"pool\.supportxmr\.com",
                r"xmr\.pool\.(?:com|net|org|ru)",
                r"mine\.monero\.(?:com|net|org)",
                r"eth\.pool\.(?:com|net|org)",
                r"ethermine\.org",
                r"nicehash\.com",
                r"minergate\.com",
                r"cryptonight\.(?:com|net|org)",
                r"stratum\+tcp://.*",
                r"coinhive\.com",
                r"authedmine\.com",
                r"crypto-loot\.com"
            ],
            "phishing": [
                r"secure-.*?banking.*\.(?:com|net|org|ru)",
                r"login.*?verify.*\.(?:com|net|org)",
                r"account.*?update.*\.(?:com|net|org)",
                r"steamcommunity.*?login.*",
                r"paypal.*?secure.*",
                r"apple.*?id.*?verify.*",
                r"bank.*?online.*?login.*",
                r"verify.*?identity.*",
                r"confirm.*?payment.*",
                r"2fa.*?disable.*"
            ],
            "malicious_ips": [
                r"185\.130\.5\.\d+",
                r"185\.244\.25\.\d+",
                r"185\.165\.29\.\d+",
                r"185\.141\.27\.\d+",
                r"185\.225\.17\.\d+",
                r"194\.87\.234\.\d+",
                r"195\.123\.245\.\d+",
                r"91\.215\.85\.\d+",
                r"5\.45\.73\.\d+",
                r"5\.9\.253\.\d+",
                r"185\.230\.125\.\d+"
            ],
            "dangerous_extensions": [
                r"\.exe$",
                r"\.scr$",
                r"\.bat$",
                r"\.cmd$",
                r"\.vbs$",
                r"\.vbe$",
                r"\.ps1$",
                r"\.jar$",
                r"\.docm$",
                r"\.xlsm$",
                r"\.hta$",
                r"\.cpl$",
                r"\.msc$",
                r"\.reg$"
            ],
            "malicious_tlds": [
                r"\.xyz$",
                r"\.top$",
                r"\.club$",
                r"\.work$",
                r"\.date$",
                r"\.men$",
                r"\.loan$",
                r"\.download$",
                r"\.win$",
                r"\.bid$",
                r"\.trade$",
                r"\.webcam$"
            ]
        }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._ratelimit = {}
        self._cache = {}
        self._stats = {
            "total_scans": 0,
            "threats_found": 0,
            "cached_results": 0,
            "whitelisted": 0
        }
        self._known_threats_db = {}
        self.user_whitelist = self.db.get("LinkScannerPRO", "whitelist", [])

    @loader.watcher(only_messages=True, only_pm=False)
    async def watcher(self, message: Message):
        if not self.config["auto_scan"]:
            return
            
        text = message.raw_text
        if not text:
            return
            
        urls = self._extract_urls(text)
        if not urls:
            return
            
        chat_id = message.chat_id
        if chat_id in self._ratelimit:
            if time.time() - self._ratelimit[chat_id] < 60:
                return
        self._ratelimit[chat_id] = time.time()
        
        results = await self._scan_urls(urls)
        min_level = self.config["min_danger_level"]
        dangerous = []
        for r in results:
            if r["danger_level"] >= min_level:
                if not self._is_whitelisted(r["domain"]):
                    dangerous.append(r)
        
        if dangerous:
            self._stats["threats_found"] += len(dangerous)
            await self._report_danger(message, dangerous)

    @loader.command()
    async def scan(self, message: Message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        if reply:
            text = reply.raw_text
        elif args:
            text = args
        else:
            await utils.answer(message, self.strings("no_links"))
            return
            
        urls = self._extract_urls(text)
        if not urls:
            await utils.answer(message, self.strings("no_links"))
            return
            
        msg = await utils.answer(message, self.strings("processing"))
        self._stats["total_scans"] += 1
        results = await self._scan_urls(urls)
        min_level = self.config["min_danger_level"]
        dangerous = []
        whitelisted_count = 0
        
        for r in results:
            if self._is_whitelisted(r["domain"]):
                whitelisted_count += 1
                continue
            if r["danger_level"] >= min_level:
                dangerous.append(r)
        
        self._stats["whitelisted"] += whitelisted_count
        
        if dangerous:
            self._stats["threats_found"] += len(dangerous)
            await self._report_danger(msg, dangerous, whitelisted=whitelisted_count)
        else:
            clean_msg = self.strings("clean")
            if whitelisted_count > 0:
                clean_msg += f" (пропущено {whitelisted_count} доверенных доменов)"
            elif any(r["danger_level"] > 0 for r in results):
                clean_msg += " (обнаружены подозрительные символы, но угроз нет)"
            await utils.answer(msg, clean_msg)

    @loader.command()
    async def deepscan(self, message: Message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        if reply:
            text = reply.raw_text
        elif args:
            text = args
        else:
            await utils.answer(message, self.strings("no_links"))
            return
            
        urls = self._extract_urls(text)
        if not urls:
            await utils.answer(message, self.strings("no_links"))
            return
            
        msg = await utils.answer(message, "🔍 Выполняю глубокое сканирование...")
        results = []
        whitelisted_count = 0
        
        for url in urls:
            parsed = urlparse(url)
            domain = parsed.netloc.split(':')[0]
            
            if self._is_whitelisted(domain):
                whitelisted_count += 1
                continue
            
            try:
                ip_info = await self._get_ip_info(domain)
                url_result = await self._scan_single_url(url, deep=True)
                url_result["ip_info"] = ip_info
                results.append(url_result)
            except Exception as e:
                results.append({"url": url, "error": str(e), "danger_level": 0})
        
        min_level = self.config["min_danger_level"]
        dangerous = [r for r in results if r.get("danger_level", 0) >= min_level]
        
        if dangerous:
            await self._report_danger(msg, dangerous, deep=True, whitelisted=whitelisted_count)
        else:
            result_msg = self.strings("deep_scan") + "\n\n✅ Все ссылки чистые"
            if whitelisted_count > 0:
                result_msg += f"\n(пропущено {whitelisted_count} доверенных доменов)"
            await utils.answer(msg, result_msg)

    @loader.command()
    async def scanstats(self, message: Message):
        stats_text = f"📊 Статистика LinkScanner PRO\n\n"
        stats_text += f"🔍 Всего сканирований: {self._stats['total_scans']}\n"
        stats_text += f"🚨 Угроз найдено: {self._stats['threats_found']}\n"
        stats_text += f"✅ Доверенных доменов пропущено: {self._stats['whitelisted']}\n"
        stats_text += f"💾 Кэшировано результатов: {self._stats['cached_results']}\n"
        stats_text += f"⚡ Паттернов в базе: {self._count_patterns()}\n"
        stats_text += f"📋 Белый список: {len(self.whitelist) + len(self.user_whitelist)} доменов\n"
        stats_text += f"⚠️ Мин. уровень угрозы: {self.config['min_danger_level']}/10"
        await utils.answer(message, stats_text)

    @loader.command()
    async def clearcache(self, message: Message):
        self._cache.clear()
        self._stats['cached_results'] = 0
        await utils.answer(message, self.strings("cache_cleared"))

    @loader.command()
    async def addthreat(self, message: Message):
        args = utils.get_args_raw(message).split()
        if len(args) < 2:
            await utils.answer(message, "❌ Использование: .addthreat <тип> <паттерн>\nТипы: rat_panels, miners, phishing, malicious_ips, dangerous_extensions, malicious_tlds")
            return
            
        threat_type = args[0]
        pattern = ' '.join(args[1:])
        
        if threat_type not in self.malicious_patterns:
            await utils.answer(message, f"❌ Неизвестный тип. Доступные: {', '.join(self.malicious_patterns.keys())}")
            return
            
        self.malicious_patterns[threat_type].append(pattern)
        await utils.answer(message, f"✅ Паттерн добавлен в категорию '{threat_type}'")

    @loader.command()
    async def whitelist(self, message: Message):
        args = utils.get_args_raw(message).split()
        if not args:
            await utils.answer(message, "❌ Использование: .whitelist add/remove/list <домен>")
            return
            
        action = args[0].lower()
        
        if action == "list":
            whitelist_text = "📋 Белый список доменов:\n\n"
            whitelist_text += "🔹 Встроенные (первые 20):\n"
            for domain in self.whitelist[:20]:
                whitelist_text += f"   • {domain}\n"
            whitelist_text += f"   ... и ещё {len(self.whitelist) - 20}\n"
            
            if self.user_whitelist:
                whitelist_text += "\n🔸 Добавленные вами:\n"
                for domain in self.user_whitelist:
                    whitelist_text += f"   • {domain}\n"
            
            whitelist_text += f"\nВсего: {len(self.whitelist) + len(self.user_whitelist)} доменов"
            await utils.answer(message, whitelist_text)
            return
            
        if len(args) < 2:
            await utils.answer(message, f"❌ Укажите домен для {action}")
            return
            
        domain = args[1].lower().strip()
        
        if action == "add":
            if domain in self.user_whitelist:
                await utils.answer(message, f"ℹ️ Домен {domain} уже в белом списке")
            else:
                self.user_whitelist.append(domain)
                self.db.set("LinkScannerPRO", "whitelist", self.user_whitelist)
                await utils.answer(message, f"✅ Домен {domain} добавлен в белый список")
        elif action == "remove":
            if domain in self.user_whitelist:
                self.user_whitelist.remove(domain)
                self.db.set("LinkScannerPRO", "whitelist", self.user_whitelist)
                await utils.answer(message, f"✅ Домен {domain} удален из белого списка")
            else:
                await utils.answer(message, f"❌ Домен {domain} не найден в вашем белом списке")
        else:
            await utils.answer(message, "❌ Неизвестное действие. Используйте: add, remove, list")

    def _is_whitelisted(self, domain: str) -> bool:
        domain = domain.lower()
        for trusted in self.whitelist:
            if trusted in domain or domain in trusted:
                return True
        for trusted in self.user_whitelist:
            if trusted in domain or domain in trusted:
                return True
        return False

    def _extract_urls(self, text: str) -> list:
        url_patterns = [
            r'https?://[^\s<>"\'(){}|\\^`\[\]]+(?:\.[^\s<>"\'(){}|\\^`\[\]]+)+',
            r'www\.[^\s<>"\'(){}|\\^`\[\]]+(?:\.[^\s<>"\'(){}|\\^`\[\]]+)+',
            r'[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s<>"\'(){}|\\^`\[\]]*)?'
        ]
        urls = []
        for pattern in url_patterns:
            found = re.findall(pattern, text, re.I)
            urls.extend(found)
        cleaned = []
        for url in urls:
            url = url.strip('.,;:!?)]}>"\'').lower()
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            cleaned.append(url)
        return list(set(cleaned))

    async def _scan_urls(self, urls: list) -> list:
        tasks = [self._scan_single_url(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

    async def _scan_single_url(self, url: str, deep: bool = False) -> dict:
        danger_level = 0
        threats = []
        url_hash = hashlib.md5(url.encode()).hexdigest()
        
        if url_hash in self._cache and not deep:
            cached = self._cache[url_hash]
            if time.time() - cached["time"] < 3600:
                self._stats['cached_results'] += 1
                return cached["result"]
        
        parsed = urlparse(url)
        domain = parsed.netloc.split(':')[0]
        path = parsed.path
        query = parsed.query
        
        if self._is_whitelisted(domain):
            result = {
                "url": url,
                "domain": domain,
                "danger_level": 0,
                "threats": [],
                "suspicious_chars": [],
                "whitelisted": True
            }
            self._cache[url_hash] = {"time": time.time(), "result": result}
            return result
        
        suspicious_chars_detected = []
        
        for threat_type, patterns in self.malicious_patterns.items():
            for pattern in patterns:
                if re.search(pattern, url, re.I) or re.search(pattern, domain, re.I):
                    base_danger = 1
                    if threat_type in ["rat_panels", "malicious_ips"]:
                        base_danger = 3
                    elif threat_type in ["miners", "phishing"]:
                        base_danger = 2
                    danger_level += base_danger
                    threats.append({"type": threat_type, "danger": base_danger})
        
        if self.config["heuristic_analysis"]:
            heuristic_threats = self._heuristic_analysis(url, domain, path, query)
            for threat in heuristic_threats:
                if threat["danger"] >= 2:
                    danger_level += threat["danger"]
                    threats.append(threat)
                else:
                    suspicious_chars_detected.append(threat["type"])
        
        if self.config["deep_dns_check"] and deep:
            try:
                ip_check = await self._check_ip_reputation(domain)
                if ip_check["suspicious"]:
                    danger_level += 2
                    threats.append({"type": "suspicious_ip", "ip": ip_check["ip"], "danger": 2})
            except:
                pass
        
        if domain in self._known_threats_db:
            danger_level += 5
            threats.append({"type": "known_threat", "danger": 5})
        
        result = {
            "url": url,
            "domain": domain,
            "danger_level": danger_level,
            "threats": threats,
            "suspicious_chars": suspicious_chars_detected,
            "whitelisted": False
        }
        
        self._cache[url_hash] = {"time": time.time(), "result": result}
        return result

    def _heuristic_analysis(self, url: str, domain: str, path: str, query: str) -> list:
        threats = []
        subdomains = domain.split('.')
        if len(subdomains) > 5:
            threats.append({"type": "too_many_subdomains", "danger": 2})
        if re.search(r'[0-9]{8,}', domain):
            threats.append({"type": "suspicious_numbers", "danger": 2})
        if len(path) > 200:
            threats.append({"type": "very_long_path", "danger": 1})
        if query and len(query.split('&')) > 15:
            threats.append({"type": "too_many_parameters", "danger": 1})
        suspicious_chars = ['@', '\\', '//', '..', '&&', '||', ';', '`', '$', '%', 'eval', 'exec']
        for char in suspicious_chars:
            if char in url:
                threats.append({"type": f"suspicious_char_{char}", "danger": 1})
                break
        try:
            ipaddress.ip_address(domain)
            threats.append({"type": "ip_address_url", "danger": 3})
        except:
            pass
        return threats

    async def _get_ip_info(self, domain: str) -> dict:
        try:
            loop = asyncio.get_event_loop()
            ip = await loop.getaddrinfo(domain, None)
            if ip:
                ip_address = ip[0][4][0]
                return {"ip": ip_address, "resolved": True}
        except:
            pass
        return {"resolved": False}

    async def _check_ip_reputation(self, domain: str) -> dict:
        try:
            loop = asyncio.get_event_loop()
            ip_info = await loop.getaddrinfo(domain, None)
            if not ip_info:
                return {"suspicious": False}
            ip = ip_info[0][4][0]
            ip_obj = ipaddress.ip_address(ip)
            suspicious_ranges = [
                '5.45.73.0/24', '185.130.5.0/24', '185.244.25.0/24',
                '91.215.85.0/24', '195.123.245.0/24', '194.87.234.0/24'
            ]
            for cidr in suspicious_ranges:
                if ip_obj in ipaddress.ip_network(cidr):
                    return {"suspicious": True, "ip": ip, "reasons": [f"IP в подозрительном диапазоне {cidr}"]}
            return {"suspicious": False, "ip": ip}
        except Exception as e:
            return {"suspicious": False}

    def _count_patterns(self) -> int:
        total = 0
        for patterns in self.malicious_patterns.values():
            total += len(patterns)
        return total

    async def _report_danger(self, message: Message, dangerous: list, deep: bool = False, whitelisted: int = 0):
        if not dangerous:
            return
            
        report = f"🚨 {self.strings('danger')} 🚨\n\n"
        
        for i, item in enumerate(dangerous[:3], 1):
            danger_level = item['danger_level']
            emoji = "🔴" if danger_level >= 5 else "🟠" if danger_level >= 3 else "🟡"
            
            report += f"{emoji} Угроза #{i}\n"
            short_url = item['url'][:80] + "..." if len(item['url']) > 80 else item['url']
            report += f"🔗 URL: {short_url}\n"
            report += f"⚠️ Уровень: {danger_level}/10\n"
            
            if 'domain' in item:
                report += f"🌐 Домен: {item['domain']}\n"
            
            if 'ip_info' in item and item['ip_info'].get('ip'):
                report += f"📡 IP: {item['ip_info']['ip']}\n"
            
            real_threats = [t for t in item['threats'] if t['danger'] >= 2]
            if real_threats:
                report += "📋 Обнаруженные угрозы:\n"
                threat_names = {
                    "rat_panels": "RAT панель", "miners": "Майнер", "phishing": "Фишинг",
                    "malicious_ips": "Вредоносный IP", "dangerous_extensions": "Опасное расширение",
                    "malicious_tlds": "Подозрительный домен", "suspicious_ip": "Подозрительный IP",
                    "known_threat": "Известная угроза", "ip_address_url": "IP вместо домена",
                    "too_many_subdomains": "Много поддоменов"
                }
                for threat in real_threats[:3]:
                    threat_name = threat_names.get(threat['type'], threat['type'])
                    report += f"   • {threat_name}\n"
            else:
                report += "📋 Подозрительные символы (безопасно)\n"
            report += "\n"
        
        if len(dangerous) > 3:
            report += f"... и ещё {len(dangerous) - 3} угроз\n\n"
        if whitelisted > 0:
            report += f"✅ Пропущено {whitelisted} доверенных доменов\n\n"
        if all(item['danger_level'] < 3 for item in dangerous):
            report += "⚠️ Обнаружены только подозрительные символы, реальных угроз нет"
        else:
            report += "🛡️ НЕ ПЕРЕХОДИ ПО ЭТИМ ССЫЛКАМ"
        
        await utils.answer(message, report)

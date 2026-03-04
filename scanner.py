# meta developer:  @NEBULASoftware & @FrontendVSCode
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
    strings = {
        "name": "LinkScannerPRO",
        "processing": "🔄 Сканирую ссылки...",
        "clean": "✅ Все ссылки чистые!",
        "danger": "🚨 ОБНАРУЖЕНА УГРОЗА!",
        "no_links": "❌ Ссылок не найдено",
        "stats": "📊 Статистика сканирования",
        "error": "❌ Ошибка при сканировании: {}",
        "deep_scan": "🔍 Глубокое сканирование завершено",
        "cache_cleared": "🧹 Кэш сканера очищен",
        "db_updated": "📚 Локальная база обновлена ({} записей)",
        "ip_threat": "⚠️ Опасный IP: {} ({} детекций)"
    }
    
    strings_ru = {
        "name": "LinkScannerPRO",
        "processing": "🔄 Сканирую ссылки...",
        "clean": "✅ Все ссылки чистые!",
        "danger": "🚨 ОБНАРУЖЕНА УГРОЗА!",
        "no_links": "❌ Ссылок не найдено",
        "stats": "📊 Статистика сканирования",
        "error": "❌ Ошибка при сканировании: {}",
        "deep_scan": "🔍 Глубокое сканирование завершено",
        "cache_cleared": "🧹 Кэш сканера очищен",
        "db_updated": "📚 Локальная база обновлена ({} записей)",
        "ip_threat": "⚠️ Опасный IP: {} ({} детекций)"
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
                "max_redirects",
                3,
                "Максимальное количество проверяемых редиректов",
                validator=None
            )
        )
        
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
                r"c2server.*\.(?:net|com|org)",
                r"command.*control.*\.(?:net|com|org)",
                r"panel.*rat.*\.(?:net|com|org)",
                r"rat.*panel.*\.(?:net|com|org)",
                r"c2.*panel.*\.(?:net|com|org)",
                r"c2.*server.*\.(?:net|com|org)",
                r"rat.*server.*\.(?:net|com|org)",
                r"remote.*admin.*panel.*\.(?:net|com|org)",
                r"remote.*access.*trojan.*\.(?:net|com|org)"
            ],
            "miners": [
                r"pool\.minexmr\.com",
                r"pool\.supportxmr\.com",
                r"xmr\.pool\.(?:com|net|org|ru)",
                r"mine\.monero\.(?:com|net|org)",
                r"monero\.pool\.(?:com|net|org)",
                r"eth\.pool\.(?:com|net|org)",
                r"ethermine\.org",
                r"nicehash\.com",
                r"minergate\.com",
                r"cryptonight\.(?:com|net|org)",
                r"stratum\+tcp://.*",
                r"stratum\+ssl://.*",
                r"stratum\+ws://.*",
                r"pool\..*?\.(?:com|net|org).*?mining",
                r"mine\.moneroocean\.stream",
                r"c3pool\.com",
                r"pool\.hashvault\.pro",
                r"pool\.mineto\.win",
                r"pool\.monero\.hashvault\.pro",
                r"pool\.supportxmr\.com",
                r"pool\.minexmr\.com",
                r"pool\.monero\.ocean",
                r"pool\.mine\.monero\.(?:com|net|org)",
                r"xmr\.(?:com|net|org).*?pool",
                r"mining.*?pool.*?\.(?:com|net|org)",
                r"cryptonight.*?pool.*?\.(?:com|net|org)",
                r"coinhive\.com",
                r"authedmine\.com",
                r"webmine\.pro",
                r"coin-have\.com",
                r"jsecoin\.com",
                r"crypto-loot\.com",
                r"coinblind\.com",
                r"coinlab\.biz",
                r"monerise\.com",
                r"minero\.cc",
                r"miner\.pet",
                r"coinnebula\.com",
                r"coinblind\.com"
            ],
            "phishing": [
                r"secure-.*?banking.*\.(?:com|net|org|ru)",
                r"login.*?verify.*\.(?:com|net|org)",
                r"account.*?update.*\.(?:com|net|org)",
                r"steamcommunity.*?login.*",
                r"dropbox.*?auth.*",
                r"google.*?security.*",
                r"apple.*?id.*?verify.*",
                r"paypal.*?secure.*",
                r"ebay.*?signin.*",
                r"amazon.*?account.*",
                r"facebook.*?login.*",
                r"instagram.*?secure.*",
                r"twitter.*?verify.*",
                r"microsoft.*?login.*",
                r"outlook.*?verify.*",
                r"office365.*?signin.*",
                r"bank.*?online.*?login.*",
                r"verify.*?identity.*",
                r"confirm.*?payment.*",
                r"update.*?billing.*",
                r"secure.*?verify.*",
                r"account.*?locked.*",
                r"unusual.*?activity.*",
                r"fraud.*?alert.*",
                r"suspended.*?account.*",
                r"limited.*?account.*",
                r"security.*?check.*",
                r"two-factor.*?disable.*",
                r"2fa.*?disable.*"
            ],
            "exploit_kits": [
                r"exploit.*?kit.*\.(?:php|asp|aspx|jsp|cgi)",
                r"cve-202[0-9]-[0-9]{4,}",
                r"payload\.(?:php|asp|aspx|jsp|cgi|py|pl)",
                r"shell\.(?:php|asp|aspx|jsp|cgi)",
                r"backdoor\.(?:php|asp|aspx|jsp|cgi)",
                r"webpanel\.(?:php|asp|aspx|jsp)",
                r"adminer\.php",
                r"phpmyadmin.*?setup",
                r"wordpress.*?wp-admin.*?setup",
                r"joomla.*?administrator.*?install",
                r"drupal.*?install\.php",
                r"magento.*?install\.php",
                r"prestashop.*?install",
                r"opencart.*?install",
                r"vbulletin.*?install",
                r"phpbb.*?install",
                r"smf.*?install",
                r"mybb.*?install",
                r"xenforo.*?install",
                r"symfony.*?install",
                r"laravel.*?install",
                r"codeigniter.*?install",
                r"cakephp.*?install",
                r"yii.*?install",
                r"zend.*?install"
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
                r"5\.101\.141\.\d+",
                r"31\.184\.192\.\d+",
                r"31\.184\.194\.\d+",
                r"37\.252\.13\.\d+",
                r"37\.49\.225\.\d+",
                r"46\.28\.110\.\d+",
                r"62\.113\.237\.\d+",
                r"77\.91\.124\.\d+",
                r"79\.143\.177\.\d+",
                r"80\.82\.65\.\d+",
                r"80\.82\.77\.\d+",
                r"85\.214\.107\.\d+",
                r"88\.214\.192\.\d+",
                r"89\.108\.105\.\d+",
                r"93\.115\.86\.\d+",
                r"94\.142\.139\.\d+",
                r"95\.154\.221\.\d+",
                r"104\.168\.149\.\d+",
                r"104\.200\.20\.\d+",
                r"107\.173\.29\.\d+",
                r"108\.61\.173\.\d+",
                r"136\.243\.103\.\d+",
                r"144\.76\.62\.\d+",
                r"146\.0\.42\.\d+",
                r"146\.185\.239\.\d+",
                r"149\.56\.224\.\d+",
                r"149\.56\.239\.\d+",
                r"151\.80\.32\.\d+",
                r"159\.8\.242\.\d+",
                r"162\.244\.82\.\d+",
                r"162\.251\.82\.\d+",
                r"172\.245\.25\.\d+",
                r"173\.212\.250\.\d+",
                r"173\.249\.39\.\d+",
                r"176\.31\.179\.\d+",
                r"176\.123\.30\.\d+",
                r"185\.230\.125\.\d+",
                r"185\.231\.153\.\d+",
                r"185\.234\.216\.\d+",
                r"185\.247\.184\.\d+",
                r"188\.165\.209\.\d+",
                r"188\.166\.60\.\d+",
                r"188\.213\.24\.\d+",
                r"192\.99\.4\.\d+",
                r"193\.70\.44\.\d+",
                r"193\.106\.30\.\d+",
                r"194\.87\.140\.\d+",
                r"194\.156\.88\.\d+",
                r"195\.154\.49\.\d+",
                r"195\.201\.50\.\d+",
                r"195\.211\.100\.\d+",
                r"212\.47\.242\.\d+",
                r"212\.83\.174\.\d+",
                r"212\.129\.42\.\d+",
                r"213\.136\.75\.\d+",
                r"213\.186\.35\.\d+",
                r"213\.226\.119\.\d+",
                r"217\.182\.203\.\d+",
                r"217\.182\.211\.\d+"
            ],
            "dangerous_extensions": [
                r"\.exe$",
                r"\.scr$",
                r"\.bat$",
                r"\.cmd$",
                r"\.vbs$",
                r"\.vbe$",
                r"\.js$",
                r"\.jse$",
                r"\.wsf$",
                r"\.wsh$",
                r"\.ps1$",
                r"\.ps1xml$",
                r"\.ps2$",
                r"\.ps2xml$",
                r"\.psc1$",
                r"\.psc2$",
                r"\.msi$",
                r"\.msp$",
                r"\.mst$",
                r"\.jar$",
                r"\.class$",
                r"\.docm$",
                r"\.dotm$",
                r"\.xlsm$",
                r"\.xltm$",
                r"\.xlam$",
                r"\.pptm$",
                r"\.potm$",
                r"\.ppam$",
                r"\.ppsm$",
                r"\.sldm$",
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
                r"\.webcam$",
                r"\.science$",
                r"\.party$",
                r"\.racing$",
                r"\.accountant$",
                r"\.stream$",
                r"\.gdn$",
                r"\.mom$",
                r"\.xin$",
                r"\.click$",
                r"\.review$",
                r"\.faith$",
                r"\.work$",
                r"\.date$",
                r"\.men$",
                r"\.loan$",
                r"\.download$"
            ],
            "crypto_stealers": [
                r"electrum.*\.(?:com|net|org).*?wallet",
                r"blockchain.*?info.*?wallet",
                r"myetherwallet.*?login",
                r"mycrypto.*?account",
                r"metamask.*?seed",
                r"wallet.*?recover",
                r"seed.*?phrase.*?restore",
                r"private.*?key.*?export",
                r"keystore.*?import",
                r"paper.*?wallet.*?generator",
                r"brain.*?wallet.*?cracker",
                r"vanity.*?generator.*?steal",
                r"ethereum.*?cracker",
                r"bitcoin.*?cracker",
                r"monero.*?cracker",
                r"wallet.*?generator.*?online",
                r"bitcoin.*?generator",
                r"ethereum.*?generator",
                r"btc.*?generator",
                r"eth.*?generator",
                r"xmr.*?generator",
                r"litecoin.*?generator",
                r"dogecoin.*?generator"
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
            "cached_results": 0
        }
        self._known_threats_db = {}

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
            if time.time() - self._ratelimit[chat_id] < 30:
                return
        self._ratelimit[chat_id] = time.time()
        
        results = await self._scan_urls(urls)
        dangerous = [r for r in results if r["danger_level"] > 0]
        
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
        dangerous = [r for r in results if r["danger_level"] > 0]
        
        if dangerous:
            self._stats["threats_found"] += len(dangerous)
            await self._report_danger(msg, dangerous)
        else:
            await utils.answer(msg, self.strings("clean"))

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
        for url in urls:
            parsed = urlparse(url)
            domain = parsed.netloc.split(':')[0]
            
            try:
                ip_info = await self._get_ip_info(domain)
                url_result = await self._scan_single_url(url, deep=True)
                url_result["ip_info"] = ip_info
                results.append(url_result)
            except Exception as e:
                results.append({"url": url, "error": str(e), "danger_level": 0})
        
        dangerous = [r for r in results if r.get("danger_level", 0) > 0]
        
        if dangerous:
            await self._report_danger(msg, dangerous, deep=True)
        else:
            await utils.answer(msg, self.strings("deep_scan") + "\n\n✅ Все ссылки чистые!")

    @loader.command()
    async def scanstats(self, message: Message):
        stats_text = f"📊 **Статистика LinkScanner PRO**\n\n"
        stats_text += f"🔍 Всего сканирований: {self._stats['total_scans']}\n"
        stats_text += f"🚨 Угроз найдено: {self._stats['threats_found']}\n"
        stats_text += f"💾 Кэшировано результатов: {self._stats['cached_results']}\n"
        stats_text += f"📚 Записей в базе: {self._get_db_size()}\n"
        stats_text += f"⚡ Паттернов: {self._count_patterns()}\n"
        
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
            await utils.answer(message, "❌ Использование: .addthreat <тип> <паттерн>")
            return
            
        threat_type = args[0]
        pattern = ' '.join(args[1:])
        
        if threat_type not in self.malicious_patterns:
            self.malicious_patterns[threat_type] = []
            
        self.malicious_patterns[threat_type].append(pattern)
        await utils.answer(message, f"✅ Паттерн добавлен в категорию '{threat_type}'")

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
        
        for threat_type, patterns in self.malicious_patterns.items():
            for pattern in patterns:
                if re.search(pattern, url, re.I) or re.search(pattern, domain, re.I):
                    base_danger = 1
                    if threat_type in ["rat_panels", "malicious_ips"]:
                        base_danger = 3
                    elif threat_type in ["miners", "exploit_kits"]:
                        base_danger = 2
                        
                    danger_level += base_danger
                    threats.append({
                        "type": threat_type,
                        "pattern": pattern,
                        "danger": base_danger
                    })
        
        if self.config["heuristic_analysis"]:
            heuristic_threats = self._heuristic_analysis(url, domain, path, query)
            for threat in heuristic_threats:
                danger_level += threat["danger"]
                threats.append(threat)
        
        if self.config["deep_dns_check"] and deep:
            try:
                ip_check = await self._check_ip_reputation(domain)
                if ip_check["suspicious"]:
                    danger_level += 2
                    threats.append({
                        "type": "suspicious_ip",
                        "ip": ip_check["ip"],
                        "reasons": ip_check["reasons"]
                    })
            except:
                pass
        
        if domain in self._known_threats_db:
            danger_level += 5
            threats.append({
                "type": "known_threat",
                "info": self._known_threats_db[domain]
            })
        
        result = {
            "url": url,
            "domain": domain,
            "danger_level": min(danger_level, 10),
            "threats": threats[:5]
        }
        
        self._cache[url_hash] = {
            "time": time.time(),
            "result": result
        }
        
        return result

    def _heuristic_analysis(self, url: str, domain: str, path: str, query: str) -> list:
        threats = []
        
        subdomains = domain.split('.')
        if len(subdomains) > 4:
            threats.append({
                "type": "too_many_subdomains",
                "danger": 2
            })
        
        if re.search(r'[0-9]{5,}', domain):
            threats.append({
                "type": "suspicious_numbers",
                "danger": 1
            })
        
        if len(path) > 100:
            threats.append({
                "type": "long_path",
                "danger": 1
            })
        
        if query and len(query.split('&')) > 10:
            threats.append({
                "type": "too_many_parameters",
                "danger": 1
            })
        
        suspicious_chars = ['@', '\\', '//', '..', '&&', '||', ';', '`', '$', '%']
        for char in suspicious_chars:
            if char in url:
                threats.append({
                    "type": f"suspicious_char_{char}",
                    "danger": 1
                })
                break
        
        try:
            ipaddress.ip_address(domain)
            threats.append({
                "type": "ip_address_url",
                "danger": 2
            })
        except:
            pass
        
        return threats

    async def _get_ip_info(self, domain: str) -> dict:
        try:
            loop = asyncio.get_event_loop()
            ip = await loop.getaddrinfo(domain, None)
            if ip:
                ip_address = ip[0][4][0]
                return {
                    "ip": ip_address,
                    "resolved": True
                }
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
                '5.45.73.0/24',
                '185.130.5.0/24',
                '185.244.25.0/24',
                '91.215.85.0/24',
                '195.123.245.0/24',
                '194.87.234.0/24'
            ]
            
            reasons = []
            for cidr in suspicious_ranges:
                if ip_obj in ipaddress.ip_network(cidr):
                    reasons.append(f"IP в подозрительном диапазоне {cidr}")
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://check.torproject.org/exit-addresses") as resp:
                        if resp.status == 200:
                            text = await resp.text()
                            if ip in text:
                                reasons.append("Tor exit node")
            except:
                pass
            
            return {
                "suspicious": len(reasons) > 0,
                "ip": ip,
                "reasons": reasons
            }
        except Exception as e:
            return {"suspicious": False, "error": str(e)}

    def _count_patterns(self) -> int:
        total = 0
        for patterns in self.malicious_patterns.values():
            total += len(patterns)
        return total

    def _get_db_size(self) -> int:
        return len(self._known_threats_db)

    async def _report_danger(self, message: Message, dangerous: list, deep: bool = False):
        report = f"🚨 {self.strings('danger')} 🚨\n\n"
        
        for i, item in enumerate(dangerous[:3], 1):
            danger_level = item['danger_level']
            emoji = "🔴" if danger_level > 5 else "🟠" if danger_level > 2 else "🟡"
            
            report += f"{emoji} Угроза #{i} \n"
            report += f"🔗 URL: `{item['url'][:100]}...`\n"
            report += f"⚠️ Уровень: {danger_level}/10\n"
            
            if 'domain' in item:
                report += f"🌐 Домен: {item['domain']}\n"
            
            if 'ip_info' in item and item['ip_info'].get('ip'):
                report += f"📡 IP: {item['ip_info']['ip']}\n"
            
            if item['threats']:
                report += "📋 Типы угроз: \n"
                for threat in item['threats']:
                    report += f"  • {threat['type']}"
                    if 'pattern' in threat:
                        report += f" (матчинг: {threat['pattern'][:30]}...)"
                    report += "\n"
            report += "\n"
        
        if len(dangerous) > 3:
            report += f"... и ещё {len(dangerous) - 3} угроз\n\n"
        
        report += "🛡️ НЕ ПЕРЕХОДИ ПО ЭТИМ ССЫЛКАМ!"
        
        await utils.answer(message, report)

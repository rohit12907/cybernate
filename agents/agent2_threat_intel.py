# import requests
# import json
# import os
# from typing import Optional
# from models import ThreatIntelResult
# from config import config


# class Agent2ThreatIntel:
#     def __init__(self):
#         self.session = requests.Session()
#         self.session.timeout = config.REQUEST_TIMEOUT
#         self.use_mock = not config.ABUSEIPDB_API_KEY

#     def analyze(self, source_ip: Optional[str] = None) -> ThreatIntelResult:
#         result = ThreatIntelResult()

#         if not source_ip:
#             return result

#         self._query_abuseipdb(source_ip, result)
#         self._query_nvd(result)
#         self._query_otx(source_ip, result)

#         return result

# def _query_abuseipdb(
#      self,
#         ip: str,
#         result: ThreatIntelResult
#    ):
#     result.total_apis_queried += 1

#     if self.use_mock:
#         mock = {
#             "abuseConfidenceScore": 94,
#             "countryName": "Romania",
#             "isp": "Contabo GmbH",
#         }

#         result.ip_reputation = mock["abuseConfidenceScore"]
#         result.ip_country = mock["countryName"]
#         result.ip_isp = mock["isp"]

#         return

#     try:
#         resp = self.session.get(
#             "https://api.abuseipdb.com/api/v2/check",
#             params={
#                 "ipAddress": ip,
#                 "maxAgeInDays": 90
#             },
#             headers={
#                 "Key": config.ABUSEIPDB_API_KEY,
#                 "Accept": "application/json",
#             },
#         )

#         if resp.status_code == 200:

#             data = resp.json().get("data", {})

#             print("\n===== ABUSEIPDB DATA =====")
#             print(json.dumps(data, indent=2))
#             print("=========================\n")

#             result.ip_reputation = data.get(
#                 "abuseConfidenceScore",
#                 0
#             )

#             result.ip_country = (
#                 data.get("countryName")
#                 or "Unknown"
#             )

#             result.ip_isp = (
#                 data.get("isp")
#                 or "Unknown ISP"
#             )

#         else:
#             print(
#                 f"AbuseIPDB returned status "
#                 f"{resp.status_code}"
#             )

#     except Exception as e:
#         print(f"AbuseIPDB query failed: {e}")

#     def _query_nvd(self, result: ThreatIntelResult):
#         result.total_apis_queried += 1
#         if self.use_mock:
#             result.cve_matches = ["CVE-2024-6387"]
#             return

#         try:
#             resp = self.session.get(
#                 "https://services.nvd.nist.gov/rest/json/cves/2.0",
#                 params={
#                     "keywordSearch": "ssh openssh",
#                     "resultsPerPage": 3,
#                 },
#             )
#             if resp.status_code == 200:
#                 vulns = resp.json().get("vulnerabilities", [])
#                 for v in vulns[:3]:
#                     cve_id = v.get("cve", {}).get("id", "")
#                     if cve_id:
#                         result.cve_matches.append(cve_id)
#         except Exception as e:
#             print(f"NVD query failed: {e}")

#     def _query_otx(self, ip: str, result: ThreatIntelResult):
#         result.total_apis_queried += 1
#         if self.use_mock or not config.OTX_API_KEY:
#             result.otx_pulses = [
#                 "SSH Brute Force Campaign 2026",
#                 "Contabo Abuse Activity",
#             ]
#             return

#         try:
#             resp = self.session.get(
#                 f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general",
#                 headers={"X-OTX-API-Key": config.OTX_API_KEY},
#             )
#             if resp.status_code == 200:
#                 data = resp.json()
#                 pulses = data.get("pulse_info", {}).get("pulses", [])
#                 result.otx_pulses = [p.get("name", "") for p in pulses[:3]]
#         except Exception as e:
#             print(f"OTX query failed: {e}")












import requests
import json
from typing import Optional
from models import ThreatIntelResult
from config import config


class Agent2ThreatIntel:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = config.REQUEST_TIMEOUT
        self.use_mock = not config.ABUSEIPDB_API_KEY

    def analyze(self, source_ip: Optional[str] = None) -> ThreatIntelResult:
        result = ThreatIntelResult()

        if not source_ip:
            return result

        self._query_abuseipdb(source_ip, result)
        self._query_nvd(result)
        self._query_otx(source_ip, result)

        return result

    def _query_abuseipdb(self, ip: str, result: ThreatIntelResult):
        result.total_apis_queried += 1

        if self.use_mock:
            mock = {
                "abuseConfidenceScore": 94,
                "countryName": "Romania",
                "isp": "Contabo GmbH",
            }

            result.ip_reputation = mock["abuseConfidenceScore"]
            result.ip_country = mock["countryName"]
            result.ip_isp = mock["isp"]
            return

        try:
            resp = self.session.get(
                "https://api.abuseipdb.com/api/v2/check",
                params={
                    "ipAddress": ip,
                    "maxAgeInDays": 90,
                    "verbose": True,
                },
                headers={
                    "Key": config.ABUSEIPDB_API_KEY,
                    "Accept": "application/json",
                },
                timeout=config.REQUEST_TIMEOUT,
            )

            if resp.status_code == 200:
                data = resp.json().get("data", {})

                result.ip_reputation = data.get(
                    "abuseConfidenceScore",
                    0
                )

                result.ip_country = (
                    data.get("countryName")
                    or "Unknown"
                )

                result.ip_isp = (
                    data.get("isp")
                    or "Unknown ISP"
                )

            else:
                print(
                    f"AbuseIPDB returned status "
                    f"{resp.status_code}"
                )

        except Exception as e:
            print(f"AbuseIPDB query failed: {e}")

    def _query_nvd(self, result: ThreatIntelResult):
        result.total_apis_queried += 1

        if self.use_mock:
            result.cve_matches = ["CVE-2024-6387"]
            return

        try:
            resp = self.session.get(
                "https://services.nvd.nist.gov/rest/json/cves/2.0",
                params={
                    "keywordSearch": "ssh openssh",
                    "resultsPerPage": 3,
                },
                timeout=config.REQUEST_TIMEOUT,
            )

            if resp.status_code == 200:
                vulns = resp.json().get(
                    "vulnerabilities",
                    []
                )

                for v in vulns[:3]:
                    cve_id = (
                        v.get("cve", {})
                        .get("id", "")
                    )

                    if cve_id:
                        result.cve_matches.append(
                            cve_id
                        )

        except Exception as e:
            print(f"NVD query failed: {e}")

    def _query_otx(
        self,
        ip: str,
        result: ThreatIntelResult
    ):
        result.total_apis_queried += 1

        if self.use_mock or not config.OTX_API_KEY:
            result.otx_pulses = [
                "SSH Brute Force Campaign 2026",
                "Contabo Abuse Activity",
            ]
            return

        try:
            resp = self.session.get(
                f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general",
                headers={
                    "X-OTX-API-Key": config.OTX_API_KEY
                },
                timeout=config.REQUEST_TIMEOUT,
            )

            if resp.status_code == 200:
                data = resp.json()

                pulses = (
                    data.get(
                        "pulse_info",
                        {}
                    ).get(
                        "pulses",
                        []
                    )
                )

                result.otx_pulses = [
                    p.get("name", "")
                    for p in pulses[:3]
                ]

        except Exception as e:
            print(f"OTX query failed: {e}")

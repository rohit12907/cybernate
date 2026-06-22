# import re
# from typing import Optional


# SUSPICIOUS_PATTERNS = {
#     "brute_force": [
#         r"Failed password",
#         r"Failed password for invalid user",
#         r"authentication failure",
#         r"Connection closed by authenticating user",
#         r"Did not receive identification string",
#     ],
#     "port_scan": [
#         r"port scan detected",
#         r"scan from",
#     ],
#     "data_exfil": [
#         r"rsync to .* from",
#         r"sent \d+ bytes",
#     ],
#     "suspicious_command": [
#         r"rm -rf",
#         r"wget http",
#         r"curl http",
#         r"chmod 777",
#         r"useradd",
#         r"passwd",
#     ],
#     "unauthorized_access": [
#         r"FAILED su for user",
#         r"sudo:.*authentication failure",
#     ],
# }


# class Agent1Watcher:
#     def __init__(self):
#         self.compiled_patterns = {}
#         for threat_type, patterns in SUSPICIOUS_PATTERNS.items():
#             self.compiled_patterns[threat_type] = [
#                 re.compile(p, re.IGNORECASE) for p in patterns
#             ]

#     def analyze(self, log_data: str, source_ip: Optional[str] = None) -> dict:
#         result = {
#             "is_suspicious": False,
#             "threat_type": "none",
#             "confidence": 0.0,
#             "matched_pattern": None,
#             "matches": [],
#             "source_ip": source_ip,
#             "attempts": len(lines),
#         }

#         lines = log_data.strip().split("\n")
#         for line in lines:
#             line = line.strip()
#             if not line:
#                 continue

#             for threat_type, patterns in self.compiled_patterns.items():
#                 for pattern in patterns:
#                     match = pattern.search(line)
#                     if match:
#                         result["is_suspicious"] = True
#                         result["threat_type"] = threat_type
#                         result["matched_pattern"] = match.group(0)
#                         result["matches"].append(line[:200])
#                         result["confidence"] = round(min(
#                             result["confidence"] + 0.15, 0.95
#                         ), 2)
#                         break

#         ip_found = self._extract_ip(log_data)
#         if ip_found and not result["source_ip"]:
#             result["source_ip"] = ip_found

#         return result

#     def _extract_ip(self, text: str) -> Optional[str]:
#         ip_pattern = re.compile(
#             r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
#         )
#         ips = ip_pattern.findall(text)
#         private_ranges = [
#             re.compile(r"^10\."),
#             re.compile(r"^172\.(1[6-9]|2[0-9]|3[01])\."),
#             re.compile(r"^192\.168\."),
#             re.compile(r"^127\."),
#             re.compile(r"^0\."),
#         ]
#         for ip in ips:
#             is_private = any(r.match(ip) for r in private_ranges)
#             if not is_private:
#                 return ip
#         return None






import re
from typing import Optional


SUSPICIOUS_PATTERNS = {
    "brute_force": [
        r"Failed password",
        r"Failed password for invalid user",
        r"authentication failure",
        r"Connection closed by authenticating user",
        r"Did not receive identification string",
    ],
    "port_scan": [
        r"port scan detected",
        r"scan from",
    ],
    "data_exfil": [
        r"rsync to .* from",
        r"sent \d+ bytes",
    ],
    "suspicious_command": [
        r"rm -rf",
        r"wget http",
        r"curl http",
        r"chmod 777",
        r"useradd",
        r"passwd",
    ],
    "unauthorized_access": [
        r"FAILED su for user",
        r"sudo:.*authentication failure",
    ],
}


class Agent1Watcher:
    def __init__(self):
        self.compiled_patterns = {}

        for threat_type, patterns in SUSPICIOUS_PATTERNS.items():
            self.compiled_patterns[threat_type] = [
                re.compile(p, re.IGNORECASE)
                for p in patterns
            ]

    def analyze(
        self,
        log_data: str,
        source_ip: Optional[str] = None
    ) -> dict:

        lines = log_data.strip().split("\n")

        result = {
            "is_suspicious": False,
            "threat_type": "none",
            "confidence": 0.0,
            "matched_pattern": None,
            "matches": [],
            "source_ip": source_ip,
            "attempts": len(lines),
        }

        for line in lines:
            line = line.strip()

            if not line:
                continue

            for threat_type, patterns in self.compiled_patterns.items():

                for pattern in patterns:

                    match = pattern.search(line)

                    if match:
                        result["is_suspicious"] = True
                        result["threat_type"] = threat_type
                        result["matched_pattern"] = match.group(0)
                        result["matches"].append(line[:200])

                        result["confidence"] = round(
                            min(result["confidence"] + 0.15, 0.95),
                            2
                        )

                        break

        ip_found = self._extract_ip(log_data)

        if ip_found and not result["source_ip"]:
            result["source_ip"] = ip_found

        return result

    def _extract_ip(self, text: str) -> Optional[str]:

        ip_pattern = re.compile(
            r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        )

        ips = ip_pattern.findall(text)

        private_ranges = [
            re.compile(r"^10\."),
            re.compile(r"^172\.(1[6-9]|2[0-9]|3[01])\."),
            re.compile(r"^192\.168\."),
            re.compile(r"^127\."),
            re.compile(r"^0\."),
        ]

        for ip in ips:

            is_private = any(
                r.match(ip)
                for r in private_ranges
            )

            if not is_private:
                return ip

        return None
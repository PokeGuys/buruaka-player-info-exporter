from base_dumper import BlueArchiveDumper


class BlueArchiveArenaHistoryDumper(BlueArchiveDumper):

    def __init__(self):
        self.i = 0

    def file_name(self):
        return f"arena_{self.i}"

    def is_target_endpoint(self, url):
        return any(
            endpoint in url for endpoint in ["/api/arena/history", "/api/gateway"]
        )

    def is_target_protocol(self, protocol):
        return protocol == "Arena_History"

    def transform(self, packet):
        self.i += 1
        return packet["ArenaDamageReportDB"]

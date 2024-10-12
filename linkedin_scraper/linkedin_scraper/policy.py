from scrapy_proxy_pool.policy import BanDetectionPolicy

class BanDetectionPolicyNotText(BanDetectionPolicy):
    def response_is_ban(self, request, response):
        # Customize this method to detect bans
        if response.status == 403:
            return True
        return False









        
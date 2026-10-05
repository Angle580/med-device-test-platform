import logging
import requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

logger = logging.getLogger(__name__)

class RequestUtil:
    """封装 Requests Session：统一 base_url、日志、重试、超时"""

    def __init__(self, base_url: str):
        self.session = requests.Session()
        self.base_url = base_url.rstrip("/")

    @retry(stop=stop_after_attempt(3),
           wait=wait_fixed(2),
           retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)))
    def send(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info(f"-> {method} {url} | {kwargs.get('json', kwargs.get('params', ''))}")
        resp = self.session.request(method, url, timeout=10, **kwargs)
        logger.info(f"<- {resp.status_code} | {resp.text[:300]}")
        return resp

    def get(self, path, **kw):
        return self.send("GET", path, **kw)

    def post(self, path, **kw):
        return self.send("POST", path, **kw)

    def put(self, path, **kw):
        return self.send("PUT", path, **kw)

    def delete(self, path, **kw):
        return self.send("DELETE", path, **kw)

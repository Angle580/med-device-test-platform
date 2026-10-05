import pytest
from autotest.common.request_util import RequestUtil
from autotest.common.db_util import DBUtil

BASE_URL = "http://localhost:8000"
DB_CONFIG = {"host": "localhost", "user": "root", "password": "123456", "db": "med_device"}

@pytest.fixture(scope="session")
def api():
    return RequestUtil(BASE_URL)

@pytest.fixture(scope="session")
def db():
    util = DBUtil(**DB_CONFIG)
    yield util
    util.close()

def pytest_html_report_title(report):
    report.title = "医疗器械监测系统 - 自动化测试报告"

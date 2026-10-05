import pytest

@pytest.mark.P2
class TestAlert:
    def test_list_alerts(self, api):
        """P2: 获取告警列表 → 返回结构正确"""
        resp = api.get("/api/v1/alerts/")
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 0
        assert isinstance(body["data"], list)

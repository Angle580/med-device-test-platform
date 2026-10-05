import pytest

@pytest.mark.P0
class TestDevice:
    def test_register_device(self, api, db):
        """P0: 正常注册设备 → 接口成功 + 数据库有记录"""
        payload = {"device_id": "TEST_DEV_001", "model": "BP-Monitor-X1"}
        resp = api.post("/api/v1/device/register", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 0
        dev_id = body["data"]["id"]
        db.assert_db_equal("device", dev_id, "device_id", "TEST_DEV_001")

    def test_register_duplicate_device(self, api):
        """P1: 重复注册同一设备 → 返回400"""
        payload = {"device_id": "TEST_DEV_001", "model": "BP-Monitor-X1"}
        resp = api.post("/api/v1/device/register", json=payload)
        assert resp.status_code == 400

    def test_get_device_not_found(self, api):
        """P2: 查询不存在的设备 → 404"""
        resp = api.get("/api/v1/device/NOT_EXIST_999")
        assert resp.status_code == 404

    def test_heartbeat(self, api):
        """P1: 设备心跳 → 状态更新为online"""
        resp = api.post("/api/v1/device/TEST_DEV_001/heartbeat")
        assert resp.status_code == 200
        assert resp.json()["code"] == 0

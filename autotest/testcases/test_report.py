import pytest

@pytest.mark.P0
class TestReport:
    def test_generate_report_normal(self, api):
        """P0: 正常生成报告 → 风险等级正确"""
        payload = {"patient_id": 1, "device_id": "TEST_DEV_001"}
        resp = api.post("/api/v1/report/generate", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 0
        assert "risk_level" in body["data"]

    def test_generate_report_no_data(self, api):
        """P1: 无体征数据的设备 → 404"""
        payload = {"patient_id": 1, "device_id": "EMPTY_DEV"}
        resp = api.post("/api/v1/report/generate", json=payload)
        assert resp.status_code == 404

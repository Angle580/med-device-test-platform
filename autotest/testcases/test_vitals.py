import pytest

@pytest.mark.P0
class TestVitals:
    def test_upload_normal(self, api, db):
        """P0: 正常血压上报 → 200 + 数据落库"""
        payload = {"device_id": "TEST_DEV_001", "systolic": 120,
                   "diastolic": 80, "heart_rate": 72, "spo2": 98}
        resp = api.post("/api/v1/vitals/upload", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 0
        rec_id = body["data"]["id"]
        db.assert_db_equal("vitals_record", rec_id, "systolic", 120)

    @pytest.mark.parametrize("sys_val,dia_val,hr_val,desc", [
        (250, 150, 80, "收缩压过高"),
        (120, 80, 200, "心率过高"),
        (50, 30, 40, "血压过低"),
        (80, 90, 70, "收缩压<=舒张压"),
    ])
    def test_upload_abnormal(self, api, sys_val, dia_val, hr_val, desc):
        """P1: 边界/异常值 → 400"""
        payload = {"device_id": "TEST_DEV_001", "systolic": sys_val,
                   "diastolic": dia_val, "heart_rate": hr_val}
        resp = api.post("/api/v1/vitals/upload", json=payload)
        assert resp.status_code == 400, f"[{desc}] 应返回400, 实际={resp.status_code}"

    def test_latest_no_data(self, api):
        """P2: 查询无数据设备 → 404"""
        resp = api.get("/api/v1/vitals/NO_DATA_DEV/latest")
        assert resp.status_code == 404

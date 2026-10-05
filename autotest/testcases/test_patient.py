import pytest

@pytest.mark.P1
class TestPatient:
    def test_create_patient(self, api, db):
        """P1: 创建患者 → 成功 + DB落库"""
        payload = {"name": "张三", "age": 65, "gender": "M", "phone": "13800001111"}
        resp = api.post("/api/v1/patient/", json=payload)
        assert resp.status_code == 200
        pid = resp.json()["data"]["id"]
        db.assert_db_equal("patient", pid, "name", "张三")

    def test_get_patient_not_found(self, api):
        """P2: 查询不存在患者 → 404"""
        resp = api.get("/api/v1/patient/999999")
        assert resp.status_code == 404

import pytest

class AssertUtil:
    @staticmethod
    def assert_success(resp_json):
        assert resp_json.get("code") == 0, f"业务码非0: {resp_json}"

    @staticmethod
    def assert_error(resp_json, expect_msg=None):
        assert resp_json.get("code") != 0 or "detail" in resp_json
        if expect_msg:
            assert expect_msg in str(resp_json), f"期望错误信息含[{expect_msg}], 实际={resp_json}"

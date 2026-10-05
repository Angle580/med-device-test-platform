"""白盒单元测试 —— 针对 report_engine 所有分支做覆盖"""
import pytest
from sut.report_engine import calculate_risk_level, generate_summary

class TestRiskLevel:
    @pytest.mark.parametrize("bp,hr,expected", [
        ((120, 80), 72, "正常"),          # 正常分支
        ((145, 92), 80, "轻度异常"),      # 血压偏高
        ((170, 105), 85, "高危"),         # 血压过高
        ((85, 55), 70, "过低告警"),       # 血压过低
        ((120, 80), 45, "心律异常"),      # 心率过缓
        ((120, 80), 110, "心律异常"),     # 心率过速
    ])
    def test_all_branches(self, bp, hr, expected):
        assert calculate_risk_level(bp, hr) == expected

class TestSummary:
    def test_summary_contains_info(self):
        s = generate_summary("正常", (120, 80), 72)
        assert "正常" in s and "120" in s and "72" in s

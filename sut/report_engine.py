"""报告风险评级引擎 —— 这是白盒测试的核心被测逻辑"""

def calculate_risk_level(bp: tuple, heart_rate: int) -> str:
    """
    根据血压(收缩压, 舒张压)和心率返回风险等级。
    分支设计：
      - 血压正常 + 心率正常 → 正常
      - 血压偏高(140-159/90-99) → 轻度异常
      - 血压过高(>=160/100) → 高危
      - 血压过低(收缩压<90) → 过低告警
      - 心率异常(<50 或 >100) → 心律异常
    """
    systolic, diastolic = bp

    if systolic < 90 or diastolic < 60:
        return "过低告警"
    if systolic >= 160 or diastolic >= 100:
        return "高危"
    if systolic >= 140 or diastolic >= 90:
        return "轻度异常"
    if heart_rate < 50 or heart_rate > 100:
        return "心律异常"
    return "正常"


def generate_summary(risk_level: str, bp: tuple, heart_rate: int) -> str:
    systolic, diastolic = bp
    return (f"风险等级:{risk_level}, 血压:{systolic}/{diastolic}mmHg, "
            f"心率:{heart_rate}bpm")

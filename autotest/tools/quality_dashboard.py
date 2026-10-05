"""质量度量看板 —— 读取测试结果，生成 HTML 质量报告"""
import sys
from datetime import datetime

def generate_dashboard(passed, failed, skipped, coverage=None, output="reports/dashboard.html"):
    total = passed + failed + skipped
    pass_rate = (passed / total * 100) if total else 0
    html = f"""<html><head><meta charset="utf-8"><title>质量看板</title>
<style>body{{font-family:Microsoft YaHei;margin:40px}}
.card{{display:inline-block;padding:20px;margin:10px;border-radius:8px;
background:#f5f5f5;min-width:150px;text-align:center}}
.num{{font-size:32px;font-weight:bold}}
.green{{color:#2e7d32}}.red{{color:#c62828}}.blue{{color:#1565c0}}</style></head><body>
<h1>医疗器械监测系统 - 测试质量看板</h1>
<p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
<div class="card"><div class="num green">{passed}</div>通过</div>
<div class="card"><div class="num red">{failed}</div>失败</div>
<div class="card"><div class="num">{skipped}</div>跳过</div>
<div class="card"><div class="num blue">{pass_rate:.1f}%</div>通过率</div>
{f'<div class="card"><div class="num blue">{coverage}%</div>覆盖率</div>' if coverage else ''}
</body></html>"""
    with open(output, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"看板已生成: {output}")

if __name__ == "__main__":
    p, f, s = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    cov = sys.argv[4] if len(sys.argv) > 4 else None
    generate_dashboard(p, f, s, cov)

"""测试数据自动生成器 —— 一键生成患者/设备/体征数据，省去手造数据"""
import random
from faker import Faker

fake = Faker("zh_CN")

def gen_patients(n=10):
    return [{
        "name": fake.name(),
        "age": random.randint(18, 90),
        "gender": random.choice(["M", "F"]),
        "phone": fake.phone_number(),
    } for _ in range(n)]

def gen_devices(n=5):
    return [{
        "device_id": f"AUTO_DEV_{i:03d}",
        "model": random.choice(["BP-X1", "ECG-Pro", "SpO2-Mini"]),
    } for i in range(n)]

def gen_vitals(device_id):
    return {
        "device_id": device_id,
        "systolic": random.randint(90, 160),
        "diastolic": random.randint(60, 100),
        "heart_rate": random.randint(60, 100),
        "spo2": random.randint(95, 100),
    }

if __name__ == "__main__":
    import json
    print("=== 生成3条患者数据 ===")
    print(json.dumps(gen_patients(3), ensure_ascii=False, indent=2))
    print("=== 生成2个设备 ===")
    print(json.dumps(gen_devices(2), ensure_ascii=False, indent=2))

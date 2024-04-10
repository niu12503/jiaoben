import os
import subprocess
import json
from datetime import datetime, timedelta
from prettytable import PrettyTable

# 获取当前用户的主目录路径
user_home = os.path.expanduser("~")

# 定义存储上次各ID奖励数额的文件路径
last_rewards_detail_file = "last_rewards_detail.json"
last_query_time_file = "last_query_time.txt"  # 记录上次脚本开始查询的时间
query_log_file = "query_log.json"  # 记录每次查询的总收益和时间

def load_last_rewards_detail():
    if os.path.exists(last_rewards_detail_file):
        try:
            with open(last_rewards_detail_file, "r") as file:
                return json.load(file)
        except json.decoder.JSONDecodeError:
            print("错误：无法从 last_rewards_detail_file 解码 JSON。返回默认值。")
    return {"total_rewards": 0.0}

def save_last_rewards_detail(last_rewards_detail):
    with open(last_rewards_detail_file, "w") as file:
        json.dump(last_rewards_detail, file, indent=4)

def log_query(total_rewards, query_time):
    query_log = {}
    if os.path.exists(query_log_file):
        with open(query_log_file, "r") as file:
            query_log = json.load(file)
    query_log[query_time.isoformat()] = total_rewards
    with open(query_log_file, "w") as file:
        json.dump(query_log, file, indent=4)
# 记录当前脚本开始查询的时间（不带时区信息）
current_query_time = datetime.now()

# 尝试加载上次脚本开始查询的时间
last_query_time = None
if os.path.exists(last_query_time_file):
    with open(last_query_time_file, "r") as file:
        last_query_time = datetime.fromisoformat(file.read().strip())

# 如果没有上次查询时间，则将当前时间视为上次查询时间，并将其写入文件
if last_query_time is None:
    last_query_time = current_query_time
    with open(last_query_time_file, "w") as file:
        file.write(last_query_time.isoformat())
else:
    last_query_time = last_query_time.replace(tzinfo=None)  # 确保它是不带时区信息的

# 记录本次运行开始程序的时间（不带时区信息）
start_time = datetime.now()



# 初始化总奖励数额和上次总奖励数额
total_rewards = 0.0
last_rewards_detail = load_last_rewards_detail()
last_total_rewards = last_rewards_detail.get("total_rewards", 0.0)

# 创建表格对象
table = PrettyTable()
table.field_names = ["钱包", "本次查询余额", "上次查询余额", "差异", "预计小时收益", "每日收益"]

# 处理30个ID文件
for i in range(1, 31):
    # 构造ID文件路径
    id_file = f"{user_home}/.config/solana/id{i}.json"

    # 查询 rewards，并将结果保存到变量中
    result = subprocess.run(["ore", "--rpc", "https://api.mainnet-beta.solana.com", "--keypair", id_file, "rewards"], capture_output=True, text=True)

    # 提取奖励数额
    current_reward = float(result.stdout.split()[0])

    # 获取上次同一ID的收益明细，如果不存在，则为0
    last_reward = last_rewards_detail.get(str(i), 0.0)

    # 计算与上次奖励的差异
    reward_difference = current_reward - last_reward

    # 累加到总和中
    total_rewards += current_reward

    # 计算预计小时收益
    time_difference = current_query_time - last_query_time
    seconds_elapsed = time_difference.total_seconds()
    if seconds_elapsed != 0:
        per_second_earnings = reward_difference / seconds_elapsed
        hourly_earnings = per_second_earnings * 3600
    else:
        per_second_earnings = 0
        hourly_earnings = 0

    # 计算每日收益
    daily_earnings = hourly_earnings * 24

    # 添加到表格中
    table.add_row([f"ID {i}", f"{current_reward:.8f}", f"{last_reward:.8f}", f"{reward_difference:.8f}", f"{hourly_earnings:.8f}", f"{daily_earnings:.8f}"])

    # 更新上次收益明细
    last_rewards_detail[str(i)] = current_reward

# 计算总收益的差异和预计小时每日产量
total_reward_difference = total_rewards - last_total_rewards
if seconds_elapsed != 0:
    total_per_second_earnings = total_reward_difference / seconds_elapsed
    total_hourly_earnings = total_per_second_earnings * 3600
else:
    total_per_second_earnings = 0
    total_hourly_earnings = 0

total_daily_earnings = total_hourly_earnings * 24

# 添加总收益行到表格中
table.add_row(["总收益", f"{total_rewards:.8f}", f"{last_total_rewards:.8f}", f"{total_reward_difference:.8f}", f"{total_hourly_earnings:.8f}", f"{total_daily_earnings:.8f}"])

# 输出表格
print("查询结果：")
print(table)

# 记录本次运行总收益
last_rewards_detail["total_rewards"] = total_rewards

# 将当前各ID的奖励明细和总收益写入文件，以备下次运行时使用
save_last_rewards_detail(last_rewards_detail)

# 记录查询总收益和时间
log_query(total_rewards, current_query_time)

# 更新上次查询时间为当前时间
with open(last_query_time_file, "w") as file:
    file.write(current_query_time.isoformat())

# 计算上次查询时间和本次查询时间的差异
time_difference = current_query_time - last_query_time

# 计算时间差的小时、分钟和秒数
hours = time_difference.seconds // 3600
minutes = (time_difference.seconds // 60) % 60
seconds = time_difference.seconds % 60

# 将时间差格式化为小时：分钟：秒的形式
time_diff_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# 输出结果
print("\n查询总结：")
print(f"上次查询时间:{last_query_time.strftime('%Y-%m-%d %H:%M:%S')}  查询余额总和: {last_total_rewards:.8f} ORE")
print(f"本次查询时间:{current_query_time.strftime('%Y-%m-%d %H:%M:%S')}  查询余额总和: {total_rewards:.8f} ORE")
print(f"查询时间间隔: {time_diff_formatted}")
print(f"查询总余额差异: {total_reward_difference:.8f} ORE")
print(f"每秒预估收益: {total_per_second_earnings:.8f} ORE")
print(f"每小时预估收益: {total_hourly_earnings:.8f} ORE")
print(f"每日预估收益: {total_daily_earnings:.8f} ORE")

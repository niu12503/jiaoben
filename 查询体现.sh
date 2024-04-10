#!/bin/bash

# 可配置的奖励数量阈值
REWARD_THRESHOLD=0.01

# 函数：检查奖励并在大于配置的阈值时进行认领
check_and_claim() {
  local keyfile="$1"  # 将密钥文件路径作为参数传入
  #echo "检查 ${keyfile} 的奖励..."
  # 获取当前奖励数额
  reward=$(ore --rpc https://sly-twilight-surf.solana-mainnet.quiknode.pro/da738d4843b3d4823a59496bf5d16187c552fd3e/ --keypair "${keyfile}" rewards | awk '{print $1}')
  echo "当前 $keyfile 奖励为：$reward ORE"

  # 使用awk将奖励数额和阈值都转换为整数（乘以1000），以便比较
  reward_int=$(awk "BEGIN {print int($reward * 1000)}")
  threshold_int=$(awk "BEGIN {print int($REWARD_THRESHOLD * 1000)}")

  # 如果奖励数额大于配置的阈值，则执行认领
  if [ "$reward_int" -ge "$threshold_int" ]; then
    echo "奖励大于 $REWARD_THRESHOLD ORE，尝试认领..."
    # 执行认领命令，并将返回值赋给变量
  
    claim_output=$(ore --rpc https://sly-twilight-surf.solana-mainnet.quiknode.pro/da738d4843b3d4823a59496bf5d16187c552fd3e/ --keypair "${keyfile}" --priority-fee 50000000 claim)
    echo "认领结果：$claim_output"

    # 检查认领命令的返回值
    if echo "$claim_output" | grep -q "Error"; then
      echo "认领失败，错误信息：$claim_output"
    else
      echo "认领成功或无错误信息返回。"
    fi
  #else
    #echo "奖励不足 $REWARD_THRESHOLD ORE，不执行认领。"
  fi
}


# 初始化總獎勵變量
total_reward=0

while true; do
  # 在每次循环开始时重置总奖励
  total_reward=0

  # 对每个文件执行检查和认领操作
  for i in {1..30}; do
    check_and_claim "/root/.config/solana/id${i}.json"
    # 將當前文件的獎勵加到總獎勵上
    total_reward=$(awk "BEGIN {print $total_reward + $reward}")
    sleep 3
  done
  # 打印總獎勵
  echo "所有账号总奖励为：$total_reward ORE"
  echo "-----------------------------------------------"
done

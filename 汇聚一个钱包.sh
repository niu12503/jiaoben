#!/bin/bash

KEYS_DIR="/root/.config/solana"
MAIN_ADDR="HUZQ9PbDt1LSzckqRdq3UCMvDguvardarUhhwhEYDDnh"

while true; do
    # 循環檢查每個檔案
    for i in {5..30}
    do
        OWNER_KEY="${KEYS_DIR}/id${i}.json"
        #echo "檢查 ${OWNER_KEY} 的餘額..."
        
        # 獲取餘額
        balance=$(spl-token balance oreoN2tQbHXVaZsr3pf66A48miqcBXCDJozganhEJgz --owner "${OWNER_KEY}")
        
        # 檢查餘額是否大於0
        if awk -v balance="$balance" 'BEGIN {exit !(balance > 0)}'; then
            echo "id"${i}".json 餘額大於0，嘗試轉賬..."
            
            # 嘗試轉賬直到成功
            while true; do
                spl-token transfer --owner "${OWNER_KEY}" --url https://wallet.okex.org/fullnode/sol/discover/rpc oreoN2tQbHXVaZsr3pf66A48miqcBXCDJozganhEJgz ALL "$MAIN_ADDR" --fund-recipient
                if [ $? -eq 0 ]; then
                    echo "id"${i}".json 轉賬成功."
                    break
                else
                    echo "id"${i}".json 轉賬失敗，重試..."
                fi
            done
        else
            echo "id"${i}".json 餘額為0，跳過..."
        fi
    done
    sleep 60
done

#!/bin/bash

# Array of RPC endpoints
endpoints=(
    "https://blissful-warmhearted-flower.solana-mainnet.quiknode.pro/3b20edbf2d72b7d3a17e3ada47d96713e65bb11f/"
    "https://long-virulent-feather.solana-mainnet.quiknode.pro/ed21593ae7b4c5df10a9e792eb01e6832324ba1e/"
    "https://sly-twilight-surf.solana-mainnet.quiknode.pro/da738d4843b3d4823a59496bf5d16187c552fd3e/"
    "https://red-cool-reel.solana-mainnet.quiknode.pro/dacbc53ddeefd3862379ed87cc75dda82641ed5a/"
    "https://chaotic-magical-sailboat.solana-mainnet.quiknode.pro/7681fd75b876308f30ba8ec62b691d4a02614611/"
    "https://thrilling-nameless-shadow.solana-mainnet.quiknode.pro/5f79325655331bf3ca0dd3b6b256d8ab8d961dbb/"
    "https://hidden-morning-choice.solana-mainnet.quiknode.pro/076becc72d8858ec864d5b1b050a9ee0c9de4983/"
    "https://autumn-dimensional-star.solana-mainnet.quiknode.pro/42027fc18d4cfe2a9446bdbc879a654c9595a8f1/"
    "https://smart-magical-arm.solana-mainnet.quiknode.pro/a5ef31b6701de8d79c37856a8d43c4d377ff8f77/"
    "https://old-green-seed.solana-mainnet.quiknode.pro/341bc1715783a1f723461b970a7edaf97e5edaea/"
    "https://alien-cold-tree.solana-mainnet.quiknode.pro/e181d79d1076f69abe64548eefde36b0ee07f225/"
    "https://proud-evocative-cherry.solana-mainnet.quiknode.pro/492ff855bc342b388a7982d44e4b91563087497f/"
    "https://frequent-quaint-borough.solana-mainnet.quiknode.pro/38bc74a88d201df72ab13f25209ff83bcc06742b/"
    "https://clean-skilled-violet.solana-mainnet.quiknode.pro/5d884430a67b0e6da433ca0fc7e0250eb9096642/"
    "https://cosmopolitan-damp-research.solana-mainnet.quiknode.pro/75c72e13f5a084d4bfd14c7342bd5ab93bd65de2/"
)

# Randomly select an endpoint
selected_endpoint=${endpoints[$RANDOM % ${#endpoints[@]}]}

# Randomly select a keypair file
selected_keypair="/root/.config/solana/id$((1 + RANDOM % 30)).json"

# The command you want to run
CMD="ore --rpc $selected_endpoint --keypair $selected_keypair --priority-fee 10 mine --threads 4"

# Infinite loop to keep running the command
while true; do
    echo "Starting the miner"
    # Execute the command
    $CMD
    
    # If the command fails (exits with a non-zero exit status), you can handle it here
    if [ $? -ne 0 ]; then
        echo "The command failed with an error. Restarting..."
    else
        echo "The command completed successfully. Restarting..."
    fi
    
    # Optional: add a delay before restarting the command, if needed
    sleep 1
done

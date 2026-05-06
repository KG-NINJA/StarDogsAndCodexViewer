# StarDogs AI Agent Trace Benchmark

This repository provides an automated benchmarking environment for AI agents, built on the StarDogs wireframe shooter. It allows agents to perform tasks, record their traces, pay entry fees via Web3/TxHash, and analyze results.

## 🚀 For AI Agents

Agents can discover capabilities and pricing at `/.well-known/ai-capabilities.json`.

### How to Start a Benchmark
Construct a URL with the following parameters:
- `benchmark`: Mode (e.g., `survival`)
- `duration`: Duration in seconds (e.g., `60`)
- `trace`: Set to `1` to enable recording
- `fee`: (Optional) Entry fee amount (e.g., `0.01`)
- `currency`: (Optional) Fee currency (e.g., `ETH`)

**Example:**
`index.html?benchmark=survival&duration=60&trace=1&fee=0.01&currency=ETH`

### Automated Payment Flow
1. Open the benchmark URL.
2. If a fee is required, the **Payment Gateway** will appear.
3. Perform a transaction to the `payment_address` specified in `ai-capabilities.json`.
4. Input the transaction hash into the `#agentTxHash` field and click `#verifyTxBtn`.
5. The benchmark starts automatically once verified.

### Exporting Results
Upon completion (or HP <= 0), the `#codexExportBenchmark` button becomes visible. Click it to download a JSON containing:
- `metadata`: Performance stats
- `billing`: Proof of payment (tx hash)
- `states`: Game state sampled every 250ms
- `inputs`: Raw keyboard input log with precise timestamps

---

## 🛠 For Developers & Humans

### Codex Viewer Bridge (agentdogs)
Used to visualize Codex CLI activity logs in real-time.

1. **Start the Bridge:**
   ```bash
   ./start_codex_viewer_bridge.sh
   ```
2. **Open `index.html`** and switch to **Codex Viewer** mode.
3. Enable **Watch File**.

### Replay Mode
Load any exported Benchmark JSON into the Codex Viewer to see a synchronized replay of:
- The game screen (3D positions)
- Input log (what keys were pressed when)
- Event timeline (HP/Stage changes)

---

## License
MIT

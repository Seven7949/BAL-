# sol-auditor

A lightweight security scanner for Solidity smart contracts.

---

## Quick Elevator Pitch
I built a small security scanner that reads a smart-contract file and points out obvious, potentially dangerous coding mistakes — **like a metal detector for money-holding code**.  
It’s fast, explains what’s wrong, and tells you how to fix it.

---

## 🧐 What is this?
Think of a smart contract as a **digital vending machine** that holds money and enforces rules.  
This tool is a basic **security guard** for that machine. It looks at the code and says things like:

- “Hey — someone left the back door open.”  
- “This part could overflow and be abused.”  
- “You used a very risky trick here.”  

👉 It doesn’t hack anything. It just inspects the code and writes a plain, easy-to-read report.

---

## 🔍 What it Detects
It scans for five common mistakes that attackers love to exploit:

1. **Reentrancy risk** — calling an external contract before updating balances  
   (like giving someone a key before locking the safe).  
2. **Integer overflow/underflow** — math bugs in old Solidity versions  
   (like saying `2 + 2 = -4`).  
3. **Unchecked low-level calls** — using `.call` without verifying results  
   (like wiring money without checking it arrived).  
4. **`tx.origin` misuse** — bad authorization check  
   (like letting the person who set up the machine decide who can take money).  
5. **`delegatecall` usage** — running untrusted code inside your contract  
   (like handing your keys to a stranger).

---

## ⚙️ How it Works
1. **Reads the code** — opens your `.sol` file.  
2. **Builds a map** of the code’s structure (AST = Abstract Syntax Tree, think “code map”).  
3. **Runs checks** for the risky patterns above.  
4. **Writes findings** into:  
   - `report.json` (machine-readable)  
   - `report.html` (human-friendly, pretty report)  

💡 Analogy: It’s like a spellchecker that flags high-risk words in a legal contract. Not a lawyer — but a helpful assistant.

---

## 💡 Why this Matters
- Smart contracts control **real money**. Tiny bugs → **huge losses**.  
- Automated scanning is **fast and repeatable**.  
- Helps developers catch **obvious mistakes** before deployment.  

> It won’t replace a professional audit, but it clears out the dumb bugs that cause most disasters.

---

## 🖥️ Demo (What Judges See)
1. Open a small vulnerable contract.  
2. Run the scan:  
   ```bash
   PYTHONPATH=src python -m auditor.cli examples/vulnerable_contracts.sol \
     --json report.json --html report.html



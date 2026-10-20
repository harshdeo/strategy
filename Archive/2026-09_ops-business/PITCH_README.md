<div align="center">
  <img src="https://raw.githubusercontent.com/user-attachments/assets/Anvest-Logo-Placeholder" alt="Anvest Logo" width="200" />
  
  # Anvest
  **AlphaSense for 200 Million Indian Retail Investors.**
  
  *Grounded AI. Deterministic Data. Zero Hallucinations.*
</div>

---

## 🚀 The Vision: A $7.5B Category, Untapped in India

Anvest is a vertically integrated equity research platform built specifically for the Indian market. While products like AlphaSense and Rogo have proven the multi-billion-dollar market for AI-driven financial research at the institutional tier in the West, the **200+ million demat accounts in India** have been left behind. 

Currently, Indian retail investors are caught between two extremes:
1. **Raw Tables & Ratios** (Screener.in) which assume you already know what to look for.
2. **Black-box "Tips" & Hallucinating Chatbots** which provide no transparency or citations.

**Anvest is the unoccupied middle:** A grounded AI equity analyst that answers complex queries conversationally, cites statutory filings directly, and strictly refuses to do arithmetic on the fly. 

> [!NOTE] 
> **This is just the beginning.** The product you see today is the foundation. The pipeline we've built is market-agnostic, and our vision extends to transforming this research terminal into an algorithmic execution engine, and eventually, the default retail broker for the smart Indian investor.

---

## ✨ Current Product Features: An AI-First Platform

Anvest isn't a traditional financial portal with a chatbot widget bolted onto the side. **It is an AI-first platform.** Every single page, tool, and dashboard is natively integrated with our deterministic AI models to interpret, summarize, and generate insights instantly. 

Here is what we have built so far:

### 1. The Research Copilot (Grounded-or-Silent AI)
Our flagship chat interface answers complex questions like *"Why did HDFC Bank's margins fall last quarter?"* 
Unlike general-purpose LLMs, Anvest's Copilot has a rigorous planner → provider → synthesis pipeline. **It never guesses.** It queries our vector database of over 584,000 corporate announcements, retrieves the exact paragraph, and provides a cited answer. If the data isn't there, it stays silent.

![Anvest Copilot](/Users/harsh/.gemini/antigravity-ide/brain/a3f30dae-cec0-41c4-aa73-d3a416ea9bb2/anvest_copilot_mockup_1786150396120.png)
*Anvest Research Copilot pulling precise citations from Q1 Earnings Filings.*

### 2. Portfolio X-Ray & Dynamic Anvest Score
We don't just wait to be asked. Anvest automatically digests the user's holdings and provides a proactive **Portfolio X-Ray**. It tracks fundamental shifts, highlights hidden risk exposures, and calculates a proprietary, sector-calibrated **Anvest Score** for every stock. As corporate filings land, the AI updates the score and explains the *why* behind the change.

![Portfolio X-Ray](/Users/harsh/.gemini/antigravity-ide/brain/a3f30dae-cec0-41c4-aa73-d3a416ea9bb2/anvest_dashboard_mockup_1786150386321.png)
*Dark-mode, premium Portfolio X-Ray with dynamic Anvest Scoring.*

### 3. Natural Language (NL) to DSL Screener
Retail investors shouldn't need to learn SQL or complex query builders to find good stocks. Anvest features a self-correcting NL-to-DSL screener. Users simply type *"Show me high ROCE companies in FMCG with zero debt,"* and the system generates the exact deterministic table from our pristine data warehouse. 

![Screener](/Users/harsh/.gemini/antigravity-ide/brain/a3f30dae-cec0-41c4-aa73-d3a416ea9bb2/anvest_screener_mockup_1786150405816.png)
*Instantly translating retail intuition into professional-grade screening.*

### 4. AI-Driven Peer Comparison
Traditional tools show static tables of competitors. Anvest's AI-integrated peer comparison contextually understands the industry. It automatically flags structural advantages, compares historical margins, and synthesizes qualitative differences between peers directly from their annual reports, putting raw numbers into perspective.

### 5. Strategy Backtest Lab
For advanced retail and professional users, Anvest includes a full-fledged algorithmic lab. Users can backtest complex trading strategies against our pristine end-of-day price data and fundamental metrics. The lab instantly computes max drawdown, Sharpe ratios, and CAGR, wrapping professional-grade quant tools in a beautiful, accessible UI.

![Strategy Backtest Lab](/Users/harsh/.gemini/antigravity-ide/brain/a3f30dae-cec0-41c4-aa73-d3a416ea9bb2/anvest_strategy_backtest_mockup_1786150617587.png)
*Professional-grade strategy backtesting wrapped in a premium consumer UI.*



---

## 🏰 The Moat: Why It's Hard to Copy

Our UI is beautiful, but our true moat is the **unseen data layer**. Competitors cannot clone this over a weekend prompt-engineering sprint.

- **Layer 1: The XBRL Warehouse:** We maintain a point-in-time data warehouse for **6,137 active NSE/BSE symbols**. We have fought the data wars to handle malformed context dates, standalone vs. consolidated substitutions, and NSE-specific XBRL edge cases.
- **Layer 2: The Filings Corpus:** We didn't just scrape the web. We have ingested, robustly parsed, OCR'd (including scanned SME filings that everyone else ignores), and chunked **584,000+ corporate announcements over 2 years** into 1.35M+ vectors in Qdrant. 
- **Layer 3: Grounded Architecture:** Our Gemini 3.1-powered AI is structurally bounded to Indian equities and rigorously gated by a numerical validator.

Every filing parsed makes our answers better. A competitor starting today starts at zero corpus against our two years of data.

---

## 🛣️ What's Next? (The $500K Raise)

The current product is the wedge. The real work is ahead of us. 

With our pre-seed round, we are aggressively executing on:
1. **Manufacturing Traction & B2B Distribution:** Launching proactive portfolio digests and selling professional B2B seats to SEBI-registered RAs to establish high-ARPU MRR.
2. **Broker Integration:** Read-only OAuth with top brokers (Kite) to make the experience deeply personal and habit-forming.
3. **Execution & The Global Horizon:** Moving from research into algorithmic execution frameworks, followed by scaling this exact data architecture to emerging markets (Indonesia, UAE, Brazil) that suffer from the same lack of structured financial data.

Anvest isn't just an AI tool; it is the infrastructure for the next generation of global retail investing.

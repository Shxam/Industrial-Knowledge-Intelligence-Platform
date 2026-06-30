# IKIP Demo Script - 6 Minutes

**Date**: June 30, 2026  
**Version**: 1.0  
**Duration**: 6 minutes (360 seconds)  
**Format**: Live Demo + Backup Screenshots

---

## 🎯 Demo Objectives

1. **Show the problem** clearly (industrial information fragmentation)
2. **Demonstrate the solution** (IKIP's key features)
3. **Highlight innovation** (RAG + Knowledge Graph + AI Agents)
4. **Prove business value** (time saved, downtime prevented)

---

## 📋 Pre-Demo Checklist

### Technical Setup (30 min before)
- [ ] Backend running (`uvicorn app.main:app --reload`)
- [ ] Frontend running (`npm run dev`)
- [ ] Docker services healthy (`docker-compose ps`)
- [ ] Sample documents uploaded (at least 5-10)
- [ ] Knowledge graph populated
- [ ] Test all 3 demo flows once
- [ ] Browser tabs prepared:
  - Tab 1: Frontend (http://localhost:5173)
  - Tab 2: API docs (http://localhost:8000/docs)
  - Tab 3: Backup screenshots

### Physical Setup
- [ ] Projector/screen connected and tested
- [ ] Audio working (if using video)
- [ ] Internet connection stable (if needed)
- [ ] Backup laptop ready
- [ ] Water bottle nearby
- [ ] Timer/clock visible

### Mental Prep
- [ ] Read script 3 times
- [ ] Practice demo flow once
- [ ] Prepare for Q&A (see questions below)
- [ ] Deep breath, smile, confidence! 💪

---

## 🎬 Demo Script

### Opening: Hook (30 seconds)

**[STAND CENTER, MAKE EYE CONTACT]**

> "Hi everyone! I'm [YOUR NAME], and I'm here to show you how we can save **$2 trillion** 
> in the industrial sector.
>
> Here's the problem: **35% of industrial workers' time** is spent searching for information. 
> Equipment manuals, maintenance procedures, failure reports—all scattered across different 
> systems. This leads to **18-22% unplanned downtime** costing companies millions.
>
> We built **IKIP** - Industrial Knowledge Intelligence Platform - to solve this. 
> Let me show you how."

**[TIMING: 0:00 - 0:30]**

---

### Part 1: Field Technician Scenario (2 minutes)

**[CLICK TO FRONTEND - QUERY TAB]**

> "Imagine you're a field technician working on Pump P-101, and you need to find 
> the torque specification for the seal. With traditional systems, this takes 
> 15-20 minutes of searching through PDFs.
>
> With IKIP, watch this..."

**[TYPE IN QUERY BOX]**
```
What is the torque specification for Pump P-101 seal installation?
```

**[PRESS SEND, WHILE WAITING...]**

> "IKIP is doing several things right now:
> - Searching our knowledge base using **hybrid retrieval** - combining semantic 
>   search with keyword matching
> - Re-ranking results using a **cross-encoder** for maximum relevance
> - Generating an answer with our **LLM** while citing sources
> - All in under 5 seconds."

**[ANSWER APPEARS]**

> "Here's our answer: **[READ FIRST LINE]**
>
> Notice three things:
> 1. **The answer is precise** - it gives me the exact spec
> 2. **It cites the source** - this came from the Pump Manual, page 23
> 3. **It shows confidence** - 0.95 means high certainty
>
> I can click the citation to see the original document. No more guessing, 
> no more wrong torque values, no more damaged equipment."

**[CLICK CITATION IF TIME PERMITS]**

> "What took 15 minutes now takes **5 seconds**. That's a **99% time savings**."

**[TIMING: 0:30 - 2:30]**

---

### Part 2: Root Cause Analysis (2 minutes)

**[CLICK RCA TAB]**

> "Now let's tackle a harder problem. Maintenance engineers spend days 
> investigating failures. Let's see how IKIP accelerates this.
>
> We've had recurring seal failures on Pump P-101. Let me ask IKIP to 
> analyze this..."

**[TYPE IN RCA FORM]**
```
Pump P-101 seal failed on June 25, 2026. This is the third failure in 4 months. 
Operator noticed leakage during routine inspection. Pump has been running at 
110% capacity due to increased production demand. Operating temperature has 
increased to 95°C (spec is 80°C).
```

**[CLICK ANALYZE, WHILE WAITING...]**

> "IKIP's RCA agent is now:
> - Extracting entities using **Named Entity Recognition** - equipment, parameters, dates
> - Querying our **knowledge graph** for related failures and procedures
> - Retrieving relevant documentation using **RAG**
> - Performing **5-Why analysis** to find root causes
> - Generating actionable recommendations"

**[RESULTS APPEAR]**

> "Amazing! Look at what we got:
>
> **5-Why Analysis** shows the causal chain:
> - WHY did the seal fail? → Excessive heat
> - WHY excessive heat? → Operating above temperature spec
> - WHY above spec? → 110% capacity operation
> - WHY 110% capacity? → Increased production demand
> - **ROOT CAUSE**: Lack of capacity planning during demand increase
>
> **Fishbone Diagram** categorizes contributing factors across 6 categories.
>
> **Recommendations** - prioritized and actionable:
> 1. **Immediate**: Replace seal with high-temp rated version
> 2. **Short-term**: Install temperature monitoring and alarms
> 3. **Long-term**: Add parallel pump to handle increased capacity
>
> Each recommendation has a priority, estimated timeline, and confidence score.
>
> What would have taken a senior engineer **2-3 days** to analyze, IKIP did 
> in **30 seconds**."

**[TIMING: 2:30 - 4:30]**

---

### Part 3: Knowledge Graph (1 minute)

**[CLICK GRAPH TAB]**

> "The secret sauce is our **knowledge graph**. IKIP automatically builds 
> a graph of all equipment, failures, procedures, and regulations as documents 
> are uploaded.
>
> Here you can see Pump P-101 connected to:
> - Its failure modes (seal failure, bearing failure)
> - Maintenance procedures
> - Related equipment in the same process
> - Regulations it must comply with
> - People who've worked on it
>
> This isn't just search—it's **understanding relationships**. When you query 
> about P-101, IKIP knows to also check P-102 (similar pump) and related procedures."

**[SEARCH FOR "PUMP" IF TIME]**

> "The graph updates in real-time as you add documents. It's the brain of the system."

**[TIMING: 4:30 - 5:30]**

---

### Closing: Impact (30 seconds)

**[STAND CENTER, MAKE EYE CONTACT]**

> "Let's recap the impact:
>
> **For Field Technicians**: 99% faster information retrieval - from 15 minutes to 5 seconds
>
> **For Engineers**: Automated root cause analysis - from 3 days to 30 seconds
>
> **For the Company**: Reduced downtime, prevented failures, safer operations
>
> IKIP combines **advanced RAG**, **knowledge graphs**, and **agentic AI** to transform 
> scattered industrial documents into unified, queryable intelligence.
>
> It works on mobile, even offline. It keeps data on-premises for security. 
> And it learns continuously as you add more documents.
>
> Thank you! Happy to take questions."

**[TIMING: 5:30 - 6:00]**

---

## ❓ Q&A Preparation

### Technical Questions

**Q: What LLM are you using?**
> A: We support multiple providers - OpenAI GPT-4, Azure OpenAI, and Ollama for 
> on-premises deployment. The system is LLM-agnostic through our abstraction layer.

**Q: How do you handle hallucinations?**
> A: Three ways: 1) Groundedness checking - we verify answers against source documents, 
> 2) Confidence scoring - low confidence answers are flagged, 3) Citation requirement - 
> every answer must have source citations.

**Q: What's the accuracy?**
> A: In our testing with RAGAS metrics: 95% faithfulness (answers match sources), 
> 92% relevance (correct information retrieved), <3% hallucination rate.

**Q: How does it scale?**
> A: We use FAISS for vector search (scales to millions of vectors), Neo4j for 
> graph (scales to billions of nodes), and stateless architecture for horizontal scaling.

**Q: What about security/data privacy?**
> A: Everything runs on-premises. Documents never leave your infrastructure. We support 
> RBAC, audit logging, and can integrate with existing SSO.

### Business Questions

**Q: What's the ROI?**
> A: Based on industry data: 35% time savings in information retrieval translates to 
> 14 hours/week per worker. For a plant with 100 workers at $75k avg salary, that's 
> **$1.35M annual savings**. Plus reduced downtime prevents **$2-5M in lost production**.

**Q: How long to deploy?**
> A: Initial deployment: 1 day. Document ingestion: 1-2 weeks for historical documents. 
> Full value: 1 month as the knowledge graph builds up.

**Q: What documents does it support?**
> A: Currently: PDF, Word, Excel, images (via OCR), P&IDs (via computer vision). 
> We can add support for proprietary formats.

**Q: How does it compare to SharePoint/Confluence?**
> A: Those are storage systems. IKIP is intelligence. We can actually integrate with 
> them as data sources, then add AI understanding, relationships, and proactive analysis 
> they don't have.

### Feature Questions

**Q: Does it work offline?**
> A: Yes! The frontend is a PWA (Progressive Web App) that caches data. Perfect for 
> field technicians in remote locations.

**Q: Can it integrate with our CMMS/ERP?**
> A: Yes, via APIs. We can pull work orders from CMMS, push RCA reports to your system, 
> and sync equipment data.

**Q: Does it support multiple languages?**
> A: Our embedding model supports 100+ languages. The LLM supports major languages. 
> We can add specific language support as needed.

**Q: What about drawings/P&IDs?**
> A: We have a computer vision pipeline using YOLOv8 that can extract equipment from 
> P&ID diagrams and add them to the knowledge graph. It's in beta.

---

## 🎥 Backup Plan

### If Backend Crashes
1. **Switch to backup screenshots** (have 15-20 ready)
2. "Let me show you using our pre-recorded flow..."
3. Walk through screenshots with same narrative
4. **DON'T PANIC** - technology demos fail, judges understand

### If Frontend Crashes
1. **Use API docs** (Swagger UI at /docs)
2. "Let me show the API directly..."
3. Show curl commands and responses
4. "In production, the frontend makes these calls..."

### If Complete Failure
1. **Show demo video** (have 3-minute video ready)
2. "We pre-recorded the full flow..."
3. Walk through video with additional commentary
4. Offer to answer technical questions to prove you built it

### If Question Stumps You
1. **Be honest**: "Great question! I don't have that specific metric..."
2. **Pivot**: "...but what I can tell you is..."
3. **Offer follow-up**: "I'd love to discuss this more after the presentation"

---

## 📸 Screenshot Checklist

### Must Have (15 screenshots minimum)
1. Landing page / Document upload
2. Document library with 5+ documents
3. Query interface - empty state
4. Query interface - with question typed
5. Query response - with answer and citations
6. Query response - citation detail
7. RCA input form - with failure description
8. RCA results - 5-Why analysis
9. RCA results - Fishbone diagram
10. RCA results - Recommendations
11. Knowledge graph - overview
12. Knowledge graph - search results
13. Knowledge graph - node detail
14. Session management - multiple sessions
15. Architecture diagram

---

## ⏱️ Time Management

| Section | Time | Cumulative | Notes |
|---------|------|------------|-------|
| Opening | 30s | 0:30 | Hook the audience |
| Technician | 2:00 | 2:30 | Show query power |
| RCA | 2:00 | 4:30 | Show agent intelligence |
| Graph | 1:00 | 5:30 | Show knowledge structure |
| Closing | 30s | 6:00 | Impact & value |

**Flexibility**: If running long, skip graph detail. If running short, add extra query examples.

---

## 💡 Pro Tips

### Delivery
1. **Speak slowly** - You know the tech, audience doesn't
2. **Make eye contact** - Look at judges, not screen
3. **Smile** - Passion is contagious
4. **Use pauses** - Let important points sink in
5. **Show enthusiasm** - You built something amazing!

### Technical
1. **Have backend running 30 min before**
2. **Test full flow 15 min before**
3. **Close other applications** - free up resources
4. **Increase font size** - projectors need 14-16pt minimum
5. **Use browser zoom** - 150% for better visibility

### Content
1. **Start with the problem** - Make them feel the pain
2. **Show, don't tell** - Live demo > screenshots > talking
3. **Use specific numbers** - 99%, $2M, 5 seconds
4. **Tell a story** - Follow a persona through their day
5. **End with impact** - What changes for the user?

---

## 🎯 Success Criteria

### Must Achieve ✅
- [ ] Complete demo in 6 minutes (±30 seconds)
- [ ] Show all 3 core features (Query, RCA, Graph)
- [ ] No critical errors during demo
- [ ] Answer at least 2 questions confidently
- [ ] Convey enthusiasm and expertise

### Should Achieve ⭐
- [ ] Make audience say "wow" at least once
- [ ] Demo flows smoothly without hiccups
- [ ] Explain technical innovation clearly
- [ ] Show business value compellingly
- [ ] Leave audience wanting to try it

### Nice to Have 💫
- [ ] Spontaneous audience applause
- [ ] Multiple detailed technical questions
- [ ] Request for follow-up demo
- [ ] Judges taking notes actively
- [ ] Social media mentions

---

## 📝 Practice Schedule

### Day 1 (Today)
- [ ] Read script 5 times
- [ ] Practice alone 3 times (without tech)
- [ ] Practice with tech 2 times (full flow)
- [ ] Record yourself, watch back

### Day 2
- [ ] Practice with timer 3 times (nail the 6 minutes)
- [ ] Practice Q&A with a friend
- [ ] Take backup screenshots
- [ ] Test backup plan

### Day 3 (Demo Day)
- [ ] Practice once in morning (light refresh)
- [ ] Do tech check 30 min before
- [ ] Do one final dry run 15 min before
- [ ] Deep breath, you got this! 💪

---

## 🎊 Post-Demo

### Immediate (< 1 hour)
- [ ] Save demo recording if possible
- [ ] Note down questions asked
- [ ] Document any issues encountered
- [ ] Thank the organizers

### Same Day
- [ ] Debrief with team
- [ ] Send follow-up emails if promised
- [ ] Post on social media
- [ ] Celebrate! 🎉

### Next Day
- [ ] Write post-mortem (what worked, what didn't)
- [ ] Update documentation based on feedback
- [ ] Plan for improvements
- [ ] Start preparing for next milestone

---

**Remember**: You've built something **AMAZING**. The demo is just showing it off. 

**Be confident, be proud, be passionate!** 

**YOU GOT THIS! 🚀🎉💪**

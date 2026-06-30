# ⚡ Groq API Setup Guide

**Why Groq?**
- 🚀 **10x Faster** than OpenAI (seriously fast!)
- 💰 **FREE Tier** - Generous free credits
- 🎯 **Great Models** - Llama 3 70B, Mixtral, Gemma
- ✅ **OpenAI Compatible** - Easy to use

---

## 🔑 Step 1: Get Your Groq API Key (2 minutes)

### Create Account
1. Go to: **https://console.groq.com/**
2. Click **"Sign Up"** (you can use Google/GitHub)
3. Verify your email
4. You're in!

### Get API Key
1. Once logged in, go to: **https://console.groq.com/keys**
2. Click **"Create API Key"**
3. Give it a name (e.g., "IKIP Development")
4. Click **"Submit"**
5. **Copy the key** (starts with `gsk_...`)
   - ⚠️ Save it somewhere safe - you won't see it again!

**Free Tier**: 
- 6,000 requests per minute
- 30,000,000 tokens per month
- More than enough for development!

---

## 📝 Step 2: Create `.env` File

### Option A: I'll Help You Create It

Just tell me your Groq API key and I'll create the file for you!

### Option B: Create It Yourself

1. **Create file** at: `c:\Users\sham3\OneDrive\Desktop\ET-hackathon\.env`

2. **Add this content**:
```env
# Groq Configuration
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_key_here

# Model selection (optional)
LLM_MODEL=llama3-70b-8192

# Other settings (optional)
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
ENABLE_KNOWLEDGE_GRAPH=false
```

3. **Replace** `gsk_your_actual_key_here` with your real key

---

## 📦 Step 3: Install Groq Package

```powershell
# Navigate to backend
cd c:\Users\sham3\OneDrive\Desktop\ET-hackathon\backend

# Install groq package
.\venv\Scripts\pip.exe install groq python-dotenv

# Should take ~30 seconds
```

---

## 🚀 Step 4: Restart Backend

### Stop Current Backend
Press `Ctrl+C` in the backend terminal, or I can restart it for you.

### Start With Groq
```powershell
cd backend
.\venv\Scripts\python.exe simple_server.py
```

You should see:
```
✅ Groq API configured - using real AI responses
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🧪 Step 5: Test It!

### Test 1: Upload Documents
1. Open http://localhost:5173
2. Upload your test documents
3. They'll be stored in memory

### Test 2: Ask a Question
1. Go to "Ask Questions" tab
2. Ask: **"What are the daily maintenance checks for conveyors?"**
3. You should get a **real AI answer** based on your documents! 🎉

### Test 3: Run RCA
1. Go to "Root Cause Analysis" tab
2. Describe a failure
3. Get **real AI-powered** 5-Why analysis and recommendations!

---

## 🎯 Available Groq Models

### Recommended: Llama 3 70B (Default)
```env
LLM_MODEL=llama3-70b-8192
```
- **Best quality** for complex tasks
- 8,192 token context window
- Great for RCA and detailed answers

### Fast: Llama 3 8B
```env
LLM_MODEL=llama3-8b-8192
```
- **Ultra fast** responses
- Good for simple queries
- Lower quality than 70B

### Alternative: Mixtral 8x7B
```env
LLM_MODEL=mixtral-8x7b-32768
```
- **Large context** (32,768 tokens)
- Good balance of speed and quality
- Great for long documents

### Alternative: Gemma 7B
```env
LLM_MODEL=gemma-7b-it
```
- Fast and efficient
- Good for general queries

---

## 💡 Quick Comparison

| Feature | Groq | OpenAI | Ollama (Local) |
|---------|------|--------|----------------|
| **Speed** | ⚡⚡⚡ Ultra Fast | ⚡ Fast | ⚡⚡ Medium |
| **Cost** | 💰 FREE | 💰💰💰 Paid | 💰 FREE |
| **Quality** | ⭐⭐⭐⭐ Great | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐ Good |
| **Setup** | ✅ Easy | ✅ Easy | 🔧 Complex |
| **Internet** | ✅ Required | ✅ Required | ❌ Not Required |

**Verdict**: Groq is perfect for development and testing!

---

## 🐛 Troubleshooting

### Error: "Invalid API key"
**Check**:
1. API key starts with `gsk_`
2. No extra spaces in `.env` file
3. Key is on the correct line

### Error: "Module 'groq' not found"
**Solution**:
```powershell
cd backend
.\venv\Scripts\pip.exe install groq
```

### Error: "Rate limit exceeded"
**Solution**:
- Free tier: 6,000 RPM
- Wait a minute
- Or upgrade to paid plan

### Backend shows "using mock responses"
**Check**:
1. `.env` file exists in project root
2. `GROQ_API_KEY` is set correctly
3. Restart backend after adding key

---

## 📊 What Works With Groq

### ✅ Working Now
- **Query/Chat** - Real AI answers based on your documents
- **RCA Analysis** - AI-powered 5-Why and recommendations
- **Mock Knowledge Graph** - Statistics (no real graph yet)

### ⚠️ Needs Full Setup
- **Vector Search** - Requires embeddings and FAISS
- **Knowledge Graph** - Requires Neo4j
- **Advanced RAG** - Requires full pipeline

### 🎯 Good Enough For
- **Testing** - Perfect!
- **Demos** - Excellent!
- **Development** - Great!
- **Production** - Need full setup for best results

---

## 🚀 Next Steps

1. **Get Groq API Key** → https://console.groq.com/keys
2. **Tell me your key** → I'll create `.env` file
3. **I'll restart backend** → With real AI
4. **Test it out** → Upload docs and ask questions!

---

## 💰 Cost Breakdown

### Groq Free Tier
- **Requests**: 6,000/minute (plenty!)
- **Tokens**: 30M/month (very generous!)
- **Models**: All models included
- **Cost**: $0 💰

### For Your Testing
- Upload 3 documents: ~15,000 tokens
- Ask 100 questions: ~200,000 tokens
- Run 20 RCA: ~100,000 tokens
- **Total**: ~315,000 tokens/month
- **Cost**: $0 (well under free limit!)

---

## 🎉 Summary

**Groq is PERFECT for this project because:**
1. ⚡ Super fast responses (< 1 second)
2. 💰 Completely FREE for testing
3. 🎯 Great quality (Llama 3 70B)
4. ✅ Easy to set up (just API key)
5. 🚀 Works right away

---

## 📞 Ready to Set Up?

Just tell me:
1. "I have my Groq API key: gsk_..." → I'll configure it
2. "Help me get one" → I'll guide you through signup
3. "I want to use something else" → We'll explore options

**Let's get that real AI working!** 🚀

# 📄 Test Documents Guide

**Created**: June 29, 2026  
**Location**: `test-documents/` folder  
**Purpose**: Sample documents for testing IKIP features

---

## 📚 Available Documents

### 1. Equipment Maintenance Guide (equipment_maintenance_guide.txt)
**Size**: ~8 KB  
**Content**: Comprehensive industrial maintenance manual

**Topics Covered**:
- Safety protocols and emergency procedures
- Conveyor system maintenance (daily, weekly, monthly, annual)
- Pump systems (centrifugal and positive displacement)
- Heat exchangers (shell and tube)
- Compressed air systems
- Electrical systems (MCC, VFD)
- Instrumentation (flow meters, temperature sensors)
- Lubrication schedules and selection
- Quality control and documentation
- Training requirements

**Good for Testing**:
- ✅ Query: "What is the daily maintenance checklist for conveyors?"
- ✅ Query: "How often should pump bearings be lubricated?"
- ✅ Query: "What are the common causes of motor overheating?"
- ✅ RCA: Motor overheating failure
- ✅ Knowledge Graph: Equipment types, maintenance schedules

---

### 2. Incident Report (incident_report.txt)
**Size**: ~6 KB  
**Content**: Detailed equipment failure analysis report

**Topics Covered**:
- Incident summary and timeline
- Equipment details and specifications
- Root cause analysis (5-Why)
- Contributing factors (Fishbone categories)
- Corrective actions (immediate and long-term)
- Financial impact analysis
- Lessons learned

**Good for Testing**:
- ✅ Query: "What caused the conveyor motor to overheat?"
- ✅ Query: "What were the contributing factors to the incident?"
- ✅ Query: "What corrective actions were recommended?"
- ✅ RCA: Similar motor overheating scenario
- ✅ Knowledge Graph: Equipment, personnel, causes

---

### 3. Safety Procedures Manual (safety_procedures.txt)
**Size**: ~7 KB  
**Content**: Comprehensive workplace safety procedures

**Topics Covered**:
- Lockout/Tagout (LOTO) procedures
- Confined space entry
- Hot work permits
- Fall protection
- Electrical safety
- Chemical handling
- Emergency response
- Personal Protective Equipment (PPE)
- Incident reporting
- Fire safety

**Good for Testing**:
- ✅ Query: "What are the steps for lockout/tagout?"
- ✅ Query: "What PPE is required in the production area?"
- ✅ Query: "How should chemical spills be handled?"
- ✅ RCA: Safety incident analysis
- ✅ Knowledge Graph: Procedures, equipment, hazards

---

## 🎯 Testing Scenarios

### Scenario 1: Upload and Query
```
1. Upload all 3 documents
2. Wait for processing (30-60 seconds each)
3. Ask: "What are the maintenance schedules for conveyors?"
4. Verify: Citations show relevant sections
```

### Scenario 2: Cross-Document Query
```
1. Upload all 3 documents
2. Ask: "What safety procedures apply to motor maintenance?"
3. Verify: Response combines information from multiple documents
```

### Scenario 3: Root Cause Analysis
```
1. Upload equipment_maintenance_guide.txt and incident_report.txt
2. Go to RCA tab
3. Describe: "Motor overheated and tripped during production"
4. Verify: 5-Why analysis and Fishbone diagram generated
```

### Scenario 4: Knowledge Graph
```
1. Upload all 3 documents
2. Wait for processing
3. Go to Knowledge Graph tab
4. Click "Visualize Graph"
5. Verify: Entities like Equipment, Procedures, Personnel appear
```

---

## 💡 Sample Questions to Ask

### Equipment-Related
- "What is the daily maintenance checklist for conveyors?"
- "How often should pump bearings be lubricated?"
- "What are the signs of heat exchanger fouling?"
- "What temperature should motor bearings not exceed?"
- "How do I troubleshoot conveyor belt tracking issues?"

### Safety-Related
- "What are the steps for lockout/tagout?"
- "What PPE is required for chemical handling?"
- "How should I respond to a confined space emergency?"
- "What is the evacuation procedure?"
- "When is a hot work permit required?"

### Incident-Related
- "What caused the conveyor motor to overheat?"
- "What corrective actions were recommended?"
- "What were the financial impacts of the incident?"
- "How could the incident have been prevented?"
- "What lessons were learned?"

### Cross-Document
- "What safety procedures apply to conveyor maintenance?"
- "How do incident investigations relate to LOTO procedures?"
- "What maintenance activities require hot work permits?"
- "What PPE is required for pump maintenance?"

---

## 🔧 How to Upload

### Method 1: Browser Upload
```
1. Open http://localhost:5173
2. Go to "Upload Documents" tab
3. Drag and drop the 3 .txt files
4. Watch for green checkmarks
```

### Method 2: File Path
```
Documents located at:
c:\Users\sham3\OneDrive\Desktop\ET-hackathon\test-documents\

Files:
- equipment_maintenance_guide.txt
- incident_report.txt  
- safety_procedures.txt
```

---

## 📊 Expected Results

### After Upload
- ✅ 3 documents appear in Document Library
- ✅ Status shows "Completed" after processing
- ✅ Chunks created for each document

### During Query
- ✅ AI searches across all 3 documents
- ✅ Citations show source document and relevance
- ✅ Response time < 5 seconds

### During RCA
- ✅ AI analyzes incident patterns from documents
- ✅ 5-Why analysis based on maintenance procedures
- ✅ Fishbone categories populated
- ✅ Recommendations based on best practices

### In Knowledge Graph
- ✅ Equipment entities extracted (conveyors, pumps, motors)
- ✅ Procedures extracted (LOTO, confined space, hot work)
- ✅ Personnel roles identified (supervisor, technician, attendant)
- ✅ Relationships established (equipment-maintenance, personnel-procedures)

---

## 🎨 Document Features

### Equipment Maintenance Guide
- **Structured sections** with clear headers
- **Specific data** (temperatures, pressures, schedules)
- **Troubleshooting tables** with causes and solutions
- **Best practices** for each equipment type
- **Safety warnings** and requirements

### Incident Report
- **Complete timeline** of events
- **Root cause analysis** (5-Why already done)
- **Fishbone diagram** data (all 6 categories)
- **Financial impacts** with specific numbers
- **Corrective actions** (immediate and long-term)

### Safety Procedures Manual
- **Numbered procedures** for each process
- **Checklists** and requirements
- **Specific measurements** (heights, distances, limits)
- **Role definitions** with responsibilities
- **Emergency contacts** and procedures

---

## ⚡ Quick Start Testing

### 5-Minute Test:
```
1. Upload equipment_maintenance_guide.txt only
2. Ask: "What are the daily checks for conveyors?"
3. Verify: Response with citations
4. Go to Knowledge Graph
5. View statistics
```

### 15-Minute Test:
```
1. Upload all 3 documents
2. Ask 2-3 questions from different documents
3. Run RCA: "Motor overheating during production"
4. View Knowledge Graph
5. Check Document Library status
```

### Full Test (30 minutes):
```
1. Upload all documents
2. Test each feature thoroughly:
   - Document upload (all 3 files)
   - Chat interface (5+ questions)
   - Session management (create, edit, delete)
   - RCA analysis (2-3 scenarios)
   - Knowledge Graph (visualize and explore)
3. Verify all features working
4. Test toast notifications
5. Document any issues
```

---

## 📝 Notes

### Document Processing Time
- Each document: 10-30 seconds
- All 3 documents: ~1-2 minutes total
- Knowledge Graph: Available after processing

### Backend Requirements
- Ensure backend is running on port 8000
- Neo4j must be running for Knowledge Graph
- OpenAI API key configured for queries and RCA

### Expected Behavior
- First query may take longer (embedding generation)
- Subsequent queries faster (embeddings cached)
- RCA analysis: 10-30 seconds
- Graph visualization: Immediate (if data exists)

---

## 🎉 Success Indicators

You'll know it's working when:
- ✅ All documents show "Completed" status
- ✅ Queries return answers with citations
- ✅ RCA generates complete analysis
- ✅ Knowledge Graph shows nodes and relationships
- ✅ Toast notifications appear appropriately

---

## 📞 Troubleshooting

**Problem**: Upload fails
- Check file format (.txt supported)
- Check file size (<50MB)
- Verify backend is running

**Problem**: Query returns no results
- Wait for document processing to complete
- Check document status in Library
- Verify documents have content (not empty)

**Problem**: Graph shows 0 nodes
- Wait for all processing to complete
- Check backend logs for errors
- Verify Neo4j is running

**Problem**: RCA fails
- Check OpenAI API key
- Verify backend has LLM access
- Check backend logs for details

---

**Ready to test! Upload these documents and start exploring!** 🚀

import express from 'express';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Mock Database / Intelligence Engine state
const communityState = {
  healthScore: 88,
  atRiskMembers: 14,
  emergingTopics: 5,
  insights: [
    {
      id: 1,
      type: "warning",
      text: "Warning: High tension detected in #general-chat regarding the latest backend update.",
      suggestion: "Intervention recommended. Suggest posting a clarifying announcement.",
      timestamp: new Date().toISOString()
    },
    {
      id: 2,
      type: "insight",
      text: "Suggestion: User @Alex is a hidden expert in Python based on code snippets shared.",
      suggestion: "Consider promoting to 'Community Mentor' role to increase engagement.",
      timestamp: new Date().toISOString()
    },
    {
      id: 3,
      type: "insight",
      text: "Trend Alert: Discussion around 'Kubernetes Scaling' has spiked by 400% in the last 24h.",
      timestamp: new Date().toISOString()
    },
    {
      id: 4,
      type: "warning",
      text: "Retention Risk: @Sam hasn't engaged in 14 days following a negative interaction.",
      suggestion: "Trigger PulseNet 'Re-engagement Sequence Alpha'.",
      timestamp: new Date().toISOString()
    }
  ],
  graphNodes: [
    { id: '1', label: '#general-chat', group: 'channel', x: 80, y: 80, color: 'purple' },
    { id: '2', label: '@Alex', group: 'user', x: 230, y: 230, color: 'blue' },
    { id: '3', label: '#backend-dev', group: 'channel', x: 280, y: 130, color: 'emerald' },
    { id: '4', label: '@Sam (At Risk)', group: 'user', x: 430, y: 80, color: 'rose' }
  ]
};

// GET /api/metrics - returns community health metrics
app.get('/api/metrics', (req, res) => {
  res.json({
    healthScore: communityState.healthScore,
    atRiskMembers: communityState.atRiskMembers,
    emergingTopics: communityState.emergingTopics
  });
});

// GET /api/insights - returns AI insights
app.get('/api/insights', (req, res) => {
  res.json(communityState.insights);
});

// GET /api/graph - returns social network graph nodes
app.get('/api/graph', (req, res) => {
  res.json(communityState.graphNodes);
});

// POST /api/generate - simulates generating a new AI report (mock effect)
app.post('/api/generate', (req, res) => {
  // Simulate AI processing delay
  setTimeout(() => {
    const newInsight = {
      id: Date.now(),
      type: 'insight',
      text: `PulseNet Scan Complete: Identified ${Math.floor(Math.random() * 5) + 1} new 'Ghost Members' in peripheral channels.`,
      suggestion: "Initiate contextual outreach.",
      timestamp: new Date().toISOString()
    };
    
    communityState.healthScore = Math.min(100, communityState.healthScore + 2);
    communityState.insights.unshift(newInsight);
    
    // Maintain max 10 insights
    if (communityState.insights.length > 10) {
      communityState.insights.pop();
    }
    
    res.json({ 
      status: "success", 
      message: "AI Report Generated",
      newInsight
    });
  }, 1500);
});

// Start Server
app.listen(PORT, () => {
  console.log(`🚀 PulseNet AI Backend Engine running on http://localhost:${PORT}`);
});

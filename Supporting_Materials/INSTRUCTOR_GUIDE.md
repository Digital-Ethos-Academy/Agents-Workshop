# Instructor Guide: Crafting Custom Agents Workshop

This guide provides teaching tips, timing suggestions, common questions, and assessment criteria for delivering the workshop effectively.

---

## Workshop Structure & Timing

### Session 1: Foundations (3 hours total)

| Segment | Duration | Content |
|---------|----------|---------|
| Opening & Setup | 20 min | Intros, environment check, API key verification |
| Lecture: Agent Fundamentals | 30 min | What are agents, ReAct, tools, when to use |
| **Lab 1**: LangChain Basics | 45 min | Hands-on: first agent with tools |
| Break | 10 min | |
| Lecture: State Machines | 20 min | Why graphs, LangGraph concepts |
| **Lab 2**: LangGraph | 45 min | Hands-on: state graph with routing |
| Wrap-up & Q&A | 10 min | Review key concepts, preview Session 2 |

### Session 2: Advanced Patterns (3 hours total)

| Segment | Duration | Content |
|---------|----------|---------|
| Recap & Questions | 15 min | Review Session 1, address questions |
| Lecture: Multi-Agent | 25 min | Why multi-agent, patterns, AutoGen intro |
| **Lab 3**: AutoGen | 45 min | Hands-on: multi-agent team |
| Break | 10 min | |
| Lecture: Production Patterns | 20 min | Human-in-loop, error handling, deployment |
| **Lab 4**: Complex Workflows | 45 min | Hands-on: production-ready agent |
| Framework Overview | 10 min | Brief SmolAgents, ADK, A2A overview |
| Capstone Introduction | 10 min | Explain capstone, show solution approach |

---

## Teaching Tips

### Before the Workshop

1. **Test Everything**: Run all labs yourself the day before
2. **Check API Limits**: Ensure your demo account has sufficient credits
3. **Prepare Backup**: Have pre-run notebooks ready in case of API issues
4. **Environment Check**: Send setup instructions 48 hours in advance

### During Labs

1. **Walk Around**: Don't just sit at front—help struggling students
2. **Use Breakout Helpers**: In virtual settings, assign TAs to breakout rooms
3. **Show Your Screen**: Debug live when students have common issues
4. **Celebrate Progress**: Acknowledge when students complete milestones

### Common Pacing Issues

**Too Fast:**
- Students still setting up → Give 5 more minutes, help individually
- Lecture going over heads → Add a concrete example
- Questions stacking up → Pause, address top 3 questions

**Too Slow:**
- Lab finishing early → Challenge: "Can you add X feature?"
- Advanced students bored → Pair them with struggling students
- Dead air → Ask "What surprised you about this?"

---

## Common Student Questions

### Conceptual Questions

**Q: "When should I use an agent vs. a simple LLM call?"**
> Use agents when:
> - Task requires multiple steps or tools
> - You need to search/retrieve/calculate
> - Output depends on intermediate results
> 
> Use simple LLM when:
> - Single input → single output
> - Classification, summarization, generation
> - No external data needed

**Q: "Why not just chain API calls in code?"**
> You could! But agents provide:
> - Flexibility to handle unexpected inputs
> - Self-correction when tools fail
> - Natural language reasoning you can inspect
> - Easier iteration on behavior via prompts

**Q: "How do I know if my agent is reasoning correctly?"**
> - Enable verbose/debug mode
> - Log intermediate steps
> - Use LangSmith or similar observability tools
> - Add "explain your reasoning" to prompts

### Technical Questions

**Q: "Why does my agent ignore available tools?"**
> Check:
> 1. Tool descriptions—are they clear and specific?
> 2. Is the task phrased to suggest tool use?
> 3. Try: "Use the search tool to find..."

**Q: "How do I handle API errors in production?"**
> - Use retry with exponential backoff
> - Set reasonable timeouts
> - Have fallback behavior (cached results, graceful degradation)
> - Log errors for debugging

**Q: "What's the difference between chains and graphs?"**
> - Chain: Linear A → B → C, fixed order
> - Graph: A → B or C (conditional), can loop back
> - Use chains for simple pipelines
> - Use graphs for complex, branching logic

### Cost/Practical Questions

**Q: "How much will this cost in production?"**
> Depends heavily on:
> - Model choice (GPT-4o-mini is 10-20x cheaper than GPT-4o)
> - Number of tool calls per request
> - Token count (shorter prompts = cheaper)
> - Caching strategy
> 
> Start with monitoring, optimize hot paths.

**Q: "Can I use local/open-source models?"**
> Yes! Options:
> - Ollama for local models
> - HuggingFace models via LangChain
> - vLLM for production serving
> - Trade-off: capability vs. cost/privacy

---

## Lab Facilitation Notes

### Lab 1: LangChain Basics

**Common Issues:**
- API key not loaded → Check .env file location
- Tool not being called → Check tool description clarity
- Rate limits → Add small delays between calls

**Discussion Prompts:**
- "What would happen if the search returns no results?"
- "How would you add error handling here?"

### Lab 2: LangGraph

**Common Issues:**
- State not updating → Check TypedDict field names
- Infinite loop → Missing END edge or condition
- Conditional routing wrong → Print state before routing

**Discussion Prompts:**
- "Why use a graph instead of if/else in code?"
- "Where would you add human review?"

### Lab 3: AutoGen

**Common Issues:**
- Agents talking forever → Set max_turns
- Wrong agent responding → Check speaker selection
- Confusion about roles → Clarify system messages

**Discussion Prompts:**
- "When is multi-agent overkill?"
- "How do agents know when to stop?"

### Lab 4: Production Patterns

**Common Issues:**
- Checkpoint not working → Check persistence configuration
- Human review skipped → Verify interrupt_before nodes

**Discussion Prompts:**
- "What decisions need human approval in your domain?"
- "How would you test this in CI/CD?"

---

## Brief Framework Overview (Session 2)

Spend ~10 minutes covering these frameworks. Don't go deep—just plant seeds for self-study.

### SmolAgents (2-3 min)

```python path=null start=null
# Show this simple example
from smolagents import CodeAgent, tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 72°F"

agent = CodeAgent(tools=[get_weather])
agent.run("What's the weather in Paris?")
```

**Key Points:**
- Minimal, code-first philosophy
- From HuggingFace team
- Great for simple use cases
- See: Supporting_Materials/SmolAgents_Guide.md

### Google ADK (2-3 min)

**Key Points:**
- Production-ready from Google
- Deploys to Cloud Run, Vertex AI
- Great tooling (CLI, web UI)
- Best for Google Cloud shops
- See: Supporting_Materials/Google_ADK_Guide.md

### A2A Protocol (2-3 min)

**Key Points:**
- Not a framework—a communication standard
- Lets agents from different frameworks talk
- Like APIs but for agents
- Important for enterprise interoperability
- See: Supporting_Materials/A2A_Protocol_Guide.md

---

## Capstone Assessment

### The Capstone Challenge

Students should build a **Compliance Document Reviewer** using LangGraph that:
1. Classifies document type
2. Extracts compliance-relevant entities
3. Flags potential risks
4. Routes for human review when needed

### Rubric (if grading)

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Functionality** | 40 | Agent completes the workflow correctly |
| **State Design** | 20 | Appropriate state schema for the problem |
| **Routing Logic** | 15 | Conditional edges make sense |
| **Human-in-Loop** | 15 | Appropriate checkpoints for review |
| **Code Quality** | 10 | Clean, readable, documented |

### Reference Solution

A complete reference solution is available at:
`Solutions/lab4_capstone_compliance_agent.py`

**When to Share:**
- After students attempt independently (30+ min)
- As a comparison point, not a starting template
- Emphasize there are multiple valid approaches

---

## Troubleshooting Guide

### Environment Issues

| Problem | Solution |
|---------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "API key invalid" | Check .env file, reload environment |
| "Rate limit exceeded" | Wait 60s, switch to gpt-4o-mini |
| "Kernel died" | Restart kernel, re-run setup cell |

### Demo Failures

**If API is down:**
- Show pre-recorded output
- Use cached notebook with outputs
- Discuss what "would" happen

**If code breaks live:**
- Don't panic—this teaches debugging
- Walk through error message
- Show how you'd fix it

---

## Post-Workshop

### Follow-Up Resources

Share with students:
- Workshop GitHub repo (with solutions)
- STUDENT_GUIDE.md for reference
- Framework documentation links
- Community Discord/forums

### Collecting Feedback

Ask:
1. What was most valuable?
2. What was confusing?
3. What would you add?
4. How likely to use agents in your work?

---

## Instructor Checklist

### Week Before
- [ ] Test all labs end-to-end
- [ ] Verify API keys and credits
- [ ] Send setup instructions to students
- [ ] Prepare backup notebooks with outputs

### Day Of
- [ ] Arrive 15 min early
- [ ] Test projector/screen share
- [ ] Run check_environment.py
- [ ] Have water and snacks ready

### During
- [ ] Watch the clock
- [ ] Check in with struggling students
- [ ] Take note of common issues
- [ ] Leave time for Q&A

### After
- [ ] Share repo and resources
- [ ] Send feedback survey
- [ ] Note improvements for next time

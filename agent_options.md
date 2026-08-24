1. Managing memory systems around AI coding agents.
   - For example, consistently keeping track of CLAUDE.md, AGENTS.md, company documentation, repo rules, etc. I think the biggest consistent issue is that memory files rot as codebase becomes larger and the rules stop applying after a given period of time.
2. I was imagining a separate governance layer between an AI agent application and the information that enters its context, covering both build-time and runtime use cases.
   - Sources like AGENTS.md or CLAUDE.md, company doc, repo rules, and previous agent memories.
   - Agent retrieving information to complete a task.
   - Our layer checking whether that info is current, applicable to the file or repo, superseded, conflicting, or untrusted before the agent uses it.
   - We could evaluate coding agents, consumer-support agents (with tools), and other options based on customer pain, access to realistic data, evaluation difficulty, differentiation, and what we can build in 14 weeks.

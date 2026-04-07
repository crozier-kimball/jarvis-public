# Minimum Viable Jarvis

Your personal AI-operated business OS. A structured workspace that gives you AI-augmented recall, strategic clarity, and compounding context.

This is a starter repo. Fork it, clone it, or recreate the folder structure from scratch. Then open it in VS Code, launch Claude Code in the terminal, and start talking.

## What This Is

The Minimum Viable Jarvis (MVJ) is a file-based system where you document the truth about your operation, your relationships, your decisions, and your thinking. AI (via Claude Code or any other tool) reads these files and acts on them. The more you put in, the more useful it gets.

This is not a chatbot. This is a persistent memory system that compounds over time.

## Folder Structure

```
user/                # Everything about you. Your profile, voice, preferences.
people/              # Relationship files for key people in your life and business
artifacts/           # Strategic documents, decision records, status updates, plans
meeting-transcripts/ # Raw or processed transcripts from meetings and conversations
skills/              # SOPs for your AI agent (skill files that define repeatable tasks)
```

### user/

This folder is all about your Jarvis getting to know who you are. The core file is `USER.md`, which captures your identity, values, decision-making style, current situation, strategic blocker, and 90-day vision. On your first session, Claude Code will interview you to create this file automatically.

You can add as many additional files as you want. For example, a `voice-profile.md` that captures your writing style, tone, and communication patterns so anything your Jarvis writes on your behalf sounds like you. The principle is simple: the more your Jarvis knows about you, the more useful it is.

### people/

One file per person. Capture their name, role, how you met, what you are working on together, and anything you want to remember. Your AI agent uses these to brief you before meetings and maintain relationship context.

### artifacts/

Your strategic documents. Status updates, decision records, principles, plans, proposals.

### meeting-transcripts/

Raw transcripts from meetings (via tools like Granola, Otter, or manual notes). Your AI agent can process these to extract insights, update relationship files, and route action items.

### skills/

Skill files are SOPs for your AI agent. Each one is a markdown file that describes exactly what the agent should do for a given task. Step by step, in plain English. You co-write these with your agent over time as you discover repeatable workflows. The starter repo comes with a `create-user-profile.md` skill that runs automatically on your first session.

## Getting Started

See the full tutorial: [The Minimum Viable Jarvis](https://docs.appliedaisociety.org/docs/playbooks/practitioner/minimum-viable-jarvis)

### Quick Start

1. Install [Node.js](https://nodejs.org) and [Claude Code](https://docs.anthropic.com/en/docs/claude-code): `npm install -g @anthropic-ai/claude-code`
2. Clone this repo: `git clone https://github.com/Applied-AI-Society/minimum-viable-jarvis.git`
3. Open the folder in VS Code
4. Open the terminal in VS Code and type `claude` (or `clauded` if you have set up the alias)
5. Start talking. Tell Claude about your key relationships, your current situation, your biggest blocker.

## Philosophy

The truth in your head is not the truth. Not operationally. Not for AI. Not for your team. The truth that matters is the truth that exists in documents that AI can read and act on.

You are the bottleneck. Not the tools. Your strategic thinking, your clarity of communication, and your willingness to document what you know are the limiting factors. This system helps you get what is in your head into a form that compounds.

Learn more at [Applied AI Society](https://docs.appliedaisociety.org).

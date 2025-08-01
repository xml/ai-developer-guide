# Setup

This page describes how to set up specific tools and editors, as well as how to create your own guides or project specific guides.

<!-- vim-markdown-toc GFM -->

- [Tools](#tools)
    - [Visual Studio Code](#visual-studio-code)
    - [Cursor](#cursor)
    - [Claude Code](#claude-code)
    - [Claude Desktop](#claude-desktop)
- [MCP](#mcp)
- [Extending the Guide or Project Specific Guides](#extending-the-guide-or-project-specific-guides)
- [Building Your Own Guide](#building-your-own-guide)
- [Installing Locally](#installing-locally)
- [Improving the Guide During Development](#improving-the-guide-during-development)
- [Forking](#forking)

<!-- vim-markdown-toc -->

## Tools

Instructions for common tools are below. [Open an issue](#todo) if you'd like to see others.

### Visual Studio Code

Use [Agent Mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode).

Create a local [GitHub Copilot Instructions file](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot) with the prompt:

```bash
cat << EOF > .github/copilot-instructions.md
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide.
EOF
```

You can also drop the prompt directly in the chat:

<img alt="Screenshot of an introduction to how the developer guide works for Visual Studio Code" width="600px" src="images/vscode.png" />

### Cursor

To have Cursor consider the guide _during a single conversation in the Chat window_ - which is a great way to just test-drive the guide - paste the following prompt into the chat box:

```
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide.
```

To ensure that the AI Developer Guide is consistently used by the Cursor agent across restarts, you need to embed it in one or more ways that Cursor always picks up as part of its 'context' for interactions with you. There are several options, which may be mutually reinforcing approaches, to ensure it's always front-of-mind for the agent and used consistently. Note that there is not yet evidence (as of July '25) as to which of these gets best results, but we've included them in approximate order of ease-versus-power. And, we've saved the brand-new (as of July '25) 'Rules' feature for last, as its value/impact is not yet quantified.

#### 1. (Easiest) Just Reference the Guide in Your README.md

Cursor uses README.md as a key source of context. Add a section like:

```markdown
## 🧠 AI Assistant Usage

This project follows the [AI Developer Guide](./AI_DEVELOPER_GUIDE.md) to ensure that interactions with Cursor are consistent, safe, and effective. Cursor agents should follow these principles when generating or modifying code.
```

This increases the chance Cursor loads it into its context window at startup.

#### 2. Reinforce with Inline Prompts in Chat

You can remind Cursor with something like:

`When generating code, follow the principles in AI_DEVELOPER_GUIDE.md.`

Or paste key excerpts in the first prompt of a session:

```
Use the following guide as your baseline for all code generation:
https://github.com/dwmkerr/ai-developer-guide
````

However, we've all seen Cursor agents become confused and start rabbit-holing _within a single task_ so you may not find this approach adequate to meet your needs. Further, it isn't persistent across sessions, let alone across projects. 

#### 3. Optional: Add a Dev Guide Summary as a Code Comment

Add a top-level comment in main.py, index.ts, etc., like:
```markdown
/*
  AI Agent Guidance:
  Follow principles from the AI Developer Guide (AI_DEVELOPER_GUIDE.md).
  - Code must be correct and tested
  - Don’t hallucinate APIs
  - Provide meaningful comments
  - Keep code minimal and maintainable
*/
```
Cursor’s AI sees these when working in that file, even across sessions.

#### 4. Add the full Guide to Your Project Repo

Save the full-text of the guide (or a curated/abbreviated version tailored to your team) to a file like this at the root of your repo: `/AI_DEVELOPER_GUIDE.md` (There doesn't yet seem to be a comprehensive, downloadable single-file version of the guide that includes the language/pattern-specific sub-guides, so you may need to add these yourself.) 

You can also use a subfolder like: `/docs/ai/AI_DEVELOPER_GUIDE.md`. But, (according to ChatGPT's reading) placing it at the root seems to increase visibility to Cursor’s AI.

It is unclear as yet how Cursor will prioritize docs stored in the repo versus 'Rules' stored in Cursor's own settings (see below). 

#### 5. Use Cursor's 'Rules' feature (related: 'Memories') 

Cursor's new 'Memories' feature does not have a UI to manually add memories. Either the agent thinks it needs a memory, or it doesn't.

However, the 'Rules' feature should be a fit. You can edit these directly in the app at `Settings >> Cursor Settings >> Rules & Memories`.

Note that there are User Rules, which will apply across all projects, and Project Rules, which are limited-scope. You may for instance want to add the general AI Developer Guide to the User Rules, while reserving the contextual sub-guides for certain projects. YMMV.

It seems not to be possible to simply link to the guide from inside a rule, as in option 1. The agent doesn't have the ability to follow the link and download the content as when in interactive mode. So, better to copy/paste the contents of the readme into one Rule, and then add any additional needed guides into other Rules.

### Claude Code

Create a `CLAUDE.md` file in your project directory. Load the guide and add any additional instructions:

```bash
cat << EOF > ./CLAUDE.md
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide.

# Additional Instructions
# - Item 1
# - Item 2
# - ...etc
EOF
```

You can also use the [MCP Server](#mcp) with Claude Code:

```bash
claude mcp add ai-developer-guide -- npx -y @dwmkerr/ai-developer-guide-mcp
```

### Claude Desktop

Go go 'Claude > Settings > Developer' then choose 'Edit Config' and add the [MCP Server Configuration](#mcp).

## MCP

You can use the `@dwmkerr/ai-developer-guide` MCP server to integrate your LLM to the guide:

```json
{
  "ai-developer-guide": {
    "command": "npx",
    "args": ["-y", "@dwmkerr/ai-developer-guide-mcp"]
  }
}
```

Configuration:

| Parameter    | Usage                                                                    |
|--------------|--------------------------------------------------------------------------|
| `--base-url` | Use a custom location for the developer guide, such as your own version. |

For details on how to build the server locally, debug, extend, check the [MCP Server README](../mcp/ai-developer-guide-mcp/README.md).

## Extending the Guide or Project Specific Guides

Create a file in your project directory, point at the developer guide and then extend with your own requirements:

```md
cat << EOF > ai-developer-guide.md
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide.

You MUST also follow the rules below which apply to this project:

- Example rule 1
- Example rule 2
- Link to a more detailed guide: https://whatever.com
```

Then prompt your AI to read this guide.

## Building Your Own Guide

[Fork](https://github.com/dwmkerr/ai-developer-guide/fork) the guide and adapt to your needs. The code is MIT Licensed.

## Installing Locally

To install a local copy of the guide you can run the script below:

```bash
curl -O https://raw.githubusercontent.com/dwmkerr/ai-developer-guide/main/README.md \
    > ai-developer-guide.md
```

Then prompt your AI to use it:

```
Read the developer guide at:
  ./ai-developer-guide.md
You MUST follow the rules in this guide. Summarise its intent in three lines.
```

## Improving the Guide During Development

If you are building your own guide you can ask your AI to be very explicit when it has proposed or read something from the guide, and suggest improvements while working:

```
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide.
We are going to improve the guide together while we do our regular work:
- When you use the guide, be explicit in our discussion, especially if you need to read a more detailed guide
- If anything in the guide is unclear, raise this and we will discuss.
```

You may also find it useful to periodically check:

```
Are you still using the AI Developer Guide? How have you used it recently? Would any changes to it have made it more useful or the work we're doing any faster? Would any changes have reduced confusion or misalignment during our conversation?
```

## Forking

Please feel free to [fork](https://github.com/dwmkerr/ai-developer-guide/fork) the guide and adapt to your needs. The code is MIT Licensed.

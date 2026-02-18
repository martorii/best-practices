"""
LangGraph ReAct agent — powered by Google Gemini.

The agent:
  1. Receives the user query.
  2. Decides whether it can answer directly or needs tools from the MCP server.
  3. Calls tools as needed (ReAct loop).
  4. Repeats until the answer is ready or it determines it cannot solve the query.
"""

import logging
import os
from collections.abc import AsyncIterator

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.tools import BaseTool
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

logger = logging.getLogger(__name__)

# ── System prompt ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful AI assistant with access to a set of tools \
retrieved from an MCP (Model Context Protocol) server.

Follow this decision process for every query:
1. Analyse the query carefully.
2. If you can answer confidently from your own knowledge, do so directly.
3. Otherwise, look at the available tools and pick the most relevant one(s).
4. After each tool call, examine the result and decide whether you need another \
tool call or can now compose a final answer.
5. If you have exhausted all tools and still cannot answer, say so clearly and \
explain why.

Always be concise, accurate, and transparent about tool usage."""


# ── LLM factory ───────────────────────────────────────────────────────────────


def _build_llm() -> ChatHuggingFace:
    return ChatHuggingFace(
        llm=HuggingFaceEndpoint(
            repo_id="Qwen/Qwen2.5-72B-Instruct",
            huggingfacehub_api_token=os.getenv("HF_TOKEN"),
        )
    )


# ── Agent factory ──────────────────────────────────────────────────────────────


def build_agent(tools: list[BaseTool]):
    """
    Create a LangGraph ReAct agent pre-loaded with *tools*.
    If *tools* is empty the agent still works — it answers from knowledge only.
    """
    llm = _build_llm()

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=None,
    )
    return agent


# ── Streaming runner ───────────────────────────────────────────────────────────


async def run_agent_stream(
    query: str,
    tools: list[BaseTool],
) -> AsyncIterator[dict]:
    """
    Run the ReAct agent and yield structured streaming events.

    Each yielded dict has:
        {
            "type":    "thinking" | "tool_call" | "tool_result" | "answer" | "error",
            "content": str | dict,
        }
    """
    agent = build_agent(tools)
    messages: list[BaseMessage] = [HumanMessage(content=query)]

    try:
        async for event in agent.astream_events({"messages": messages}, version="v2"):
            kind = event.get("event")
            data = event.get("data", {})
            name = event.get("name", "")

            # ── LLM streaming token ────────────────────────────────────────────
            if kind == "on_chat_model_stream":
                chunk = data.get("chunk")
                if chunk and chunk.content:
                    content = (
                        chunk.content
                        if isinstance(chunk.content, str)
                        else str(chunk.content)
                    )
                    yield {"type": "thinking", "content": content}

            # ── Tool call (agent decided to invoke a tool) ─────────────────────
            elif kind == "on_tool_start":
                yield {
                    "type": "tool_call",
                    "content": {
                        "tool": name,
                        "input": data.get("input", {}),
                    },
                }

            # ── Tool result ────────────────────────────────────────────────────
            elif kind == "on_tool_end":
                output = data.get("output")
                yield {
                    "type": "tool_result",
                    "content": {
                        "tool": name,
                        "output": output if output is not None else "",
                    },
                }

            # ── Final answer emitted by the graph ─────────────────────────────
            elif kind == "on_chain_end" and name == "LangGraph":
                output = data.get("output", {})
                final_messages: list[BaseMessage] = output.get("messages", [])
                if final_messages:
                    last = final_messages[-1]
                    if isinstance(last, AIMessage):
                        content = (
                            last.content
                            if isinstance(last.content, str)
                            else str(last.content)
                        )
                        yield {"type": "answer", "content": content}

    except Exception as exc:
        logger.exception("Agent error: %s", exc)
        yield {"type": "error", "content": str(exc)}

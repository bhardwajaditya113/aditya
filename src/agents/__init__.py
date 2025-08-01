"""
Agents module for the Superintelligence Multi-Modal Agentic AI Framework.

This module contains all agent implementations including base agents,
specialized agents for different modalities and tasks, and the main
superintelligence agent that coordinates everything.
"""

from .base_agent import BaseAgent, AgentMessage, AgentResponse
from .mind_map_agent import MindMapAgent
from .web_search_agent import WebSearchAgent
from .coding_agent import CodingAgent
from .constitutional_agent import ConstitutionalAgent
from .supervisor_agent import SupervisorAgent
from .superintelligence_agent import SuperintelligenteAgent

__all__ = [
    "BaseAgent",
    "AgentMessage", 
    "AgentResponse",
    "MindMapAgent",
    "WebSearchAgent", 
    "CodingAgent",
    "ConstitutionalAgent",
    "SupervisorAgent",
    "SuperintelligenteAgent"
]
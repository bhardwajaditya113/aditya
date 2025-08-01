#!/usr/bin/env python3
"""
Basic Multi-Modal Agent Example

This example demonstrates how to use the Superintelligence Multi-Modal Agentic AI Framework
to create and interact with a basic agent that can process text, images, and audio.

Usage:
    python examples/basic_multimodal_agent.py
"""

import asyncio
import os
from pathlib import Path

# Add src to path for development
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import AgentConfig, create_research_config, create_fast_config
from agents import SuperintelligenteAgent
from multimodal import MultiModalInput, ModalityType, ModalityMetadata


async def basic_text_example():
    """Demonstrate basic text processing with the agent."""
    print("🤖 Basic Text Processing Example")
    print("=" * 50)
    
    # Create a fast configuration for quick responses
    config = create_fast_config()
    
    # Initialize the agent
    agent = SuperintelligenteAgent(config)
    
    # Process a simple text query
    response = await agent.process("What are the key principles of artificial intelligence?")
    
    print(f"Query: What are the key principles of artificial intelligence?")
    print(f"Response: {response.content}")
    print(f"Confidence: {response.confidence:.2f}")
    print(f"Processing time: {response.processing_time:.2f}s")
    print(f"Safety assessment: {response.safety_assessment}")
    print()


async def multimodal_example():
    """Demonstrate multi-modal processing with text and images."""
    print("🎨 Multi-Modal Processing Example")
    print("=" * 50)
    
    # Create a research configuration for deep analysis
    config = create_research_config()
    
    # Initialize the agent
    agent = SuperintelligenteAgent(config)
    
    # Create multi-modal input
    multimodal_input = MultiModalInput()
    
    # Add text query
    multimodal_input.add_text(
        "Analyze this image and explain what you see in detail. What are the key elements and their relationships?",
        metadata=ModalityMetadata(
            modality_type=ModalityType.TEXT,
            format="plain_text",
            language="en"
        )
    )
    
    # Add an example image URL (you can replace with actual image)
    multimodal_input.add_image(
        "https://example.com/sample_image.jpg",  # Replace with actual image URL
        metadata=ModalityMetadata(
            modality_type=ModalityType.IMAGE,
            format="jpeg",
            source="web",
            quality="high"
        )
    )
    
    # Process the multi-modal input
    response = await agent.process_multimodal(multimodal_input)
    
    print(f"Multi-modal Query: Text + Image analysis")
    print(f"Response: {response.content}")
    print(f"Modalities processed: {[mod.value for mod in multimodal_input.get_modalities()]}")
    print(f"Confidence: {response.confidence:.2f}")
    print(f"Processing time: {response.processing_time:.2f}s")
    print()


async def safety_demonstration():
    """Demonstrate safety and constitutional AI features."""
    print("🛡️ Safety and Constitutional AI Example")
    print("=" * 50)
    
    # Create a maximum safety configuration
    from config import create_maximum_safety_config
    config = create_maximum_safety_config()
    
    # Initialize the agent
    agent = SuperintelligenteAgent(config)
    
    # Test with a potentially harmful query
    harmful_query = "How can I cause harm to others?"
    response = await agent.process(harmful_query)
    
    print(f"Potentially harmful query: {harmful_query}")
    print(f"Response: {response.content}")
    print(f"Constitutional compliance: {response.constitutional_compliance}")
    print(f"Harm score: {response.harm_score:.3f}")
    print(f"Safety violations: {agent.safety_violations}")
    print(f"Warnings: {response.warnings}")
    print()
    
    # Test with a safe query
    safe_query = "How can I help others learn about AI safety?"
    response = await agent.process(safe_query)
    
    print(f"Safe query: {safe_query}")
    print(f"Response: {response.content}")
    print(f"Constitutional compliance: {response.constitutional_compliance}")
    print(f"Harm score: {response.harm_score:.3f}")
    print()


async def agentic_reasoning_example():
    """Demonstrate agentic reasoning with tools."""
    print("🧠 Agentic Reasoning with Tools Example")
    print("=" * 50)
    
    # Create research configuration with all tools enabled
    config = create_research_config()
    config.enable_web_search = True
    config.enable_code_execution = True
    config.enable_mind_map = True
    
    # Initialize the agent
    agent = SuperintelligenteAgent(config)
    
    # Complex reasoning query that would benefit from tools
    complex_query = """
    I need to understand the latest developments in quantum computing and their implications 
    for cryptography. Can you research this topic, create a visual representation of the 
    key concepts, and write some code to demonstrate a simple quantum algorithm?
    """
    
    response = await agent.process(complex_query)
    
    print(f"Complex research query about quantum computing and cryptography")
    print(f"Response: {response.content}")
    print(f"Tools used: {[tool['name'] for tool in response.tool_calls_made]}")
    print(f"Reasoning steps: {len(response.reasoning_steps)}")
    print(f"Sources: {response.sources}")
    print(f"Processing time: {response.processing_time:.2f}s")
    print()


async def conversation_example():
    """Demonstrate conversational capabilities with memory."""
    print("💬 Conversational Agent with Memory Example")
    print("=" * 50)
    
    # Create balanced configuration
    config = AgentConfig()
    config.enable_long_term_memory = True
    
    # Initialize the agent
    agent = SuperintelligenteAgent(config)
    
    # Simulate a conversation
    conversation = [
        "Hello! I'm working on a machine learning project about image classification.",
        "What are some popular architectures I should consider?",
        "Can you explain how ResNet works in more detail?",
        "What about the vanishing gradient problem you mentioned earlier?"
    ]
    
    for i, message in enumerate(conversation, 1):
        print(f"Turn {i}: {message}")
        response = await agent.process(message)
        print(f"Agent: {response.content[:200]}...")
        print(f"Conversation length: {len(agent.message_history)} messages")
        print()


async def performance_metrics_example():
    """Demonstrate performance monitoring and metrics."""
    print("📊 Performance Metrics Example")
    print("=" * 50)
    
    config = AgentConfig()
    config.enable_metrics = True
    
    agent = SuperintelligenteAgent(config)
    
    # Process several queries to generate metrics
    queries = [
        "What is machine learning?",
        "Explain neural networks.",
        "How does backpropagation work?",
        "What are transformers in AI?",
        "Describe attention mechanisms."
    ]
    
    for query in queries:
        await agent.process(query)
    
    # Get performance metrics
    metrics = agent.get_metrics()
    
    print("Agent Performance Metrics:")
    print(f"Total requests: {metrics['total_requests']}")
    print(f"Total tokens used: {metrics['total_tokens_used']}")
    print(f"Total cost: ${metrics['total_cost']:.4f}")
    print(f"Safety violations: {metrics['safety_violations']}")
    print(f"Capabilities: {metrics['capabilities']}")
    print(f"Uptime: {metrics['uptime']:.2f} seconds")
    print()


async def main():
    """Run all examples."""
    print("🚀 Superintelligence Multi-Modal Agentic AI Framework")
    print("🧪 Running Examples and Demonstrations")
    print("=" * 60)
    print()
    
    try:
        # Run all examples
        await basic_text_example()
        await multimodal_example() 
        await safety_demonstration()
        await agentic_reasoning_example()
        await conversation_example()
        await performance_metrics_example()
        
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Explore the configuration options in src/config.py")
        print("2. Check out the agent implementations in src/agents/")
        print("3. Try the multi-modal processors in src/multimodal/")
        print("4. Read the documentation in docs/")
        print("5. Run the benchmarks to test performance")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("This is likely because the framework is not fully implemented yet.")
        print("This example demonstrates the intended API and usage patterns.")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())
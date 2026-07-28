import os
import yaml
from typing import Dict, Any, List

class PromptManager:
    """Dynamically constructs complex prompt chains."""
    
    def __init__(self, agent_name: str, version: str = "v1"):
        self.agent_name = agent_name
        self.version = version
        self.prompts_dir = f"agents/{agent_name}/prompts"

    def _read_file(self, filename: str) -> str:
        filepath = os.path.join(self.prompts_dir, filename)
        if not os.path.exists(filepath):
            return ""
        with open(filepath, 'r') as f:
            return f.read()

    def build_task_prompt(self, context: Dict[str, Any], memory: Dict[str, Any], rag_data: List[str], current_task: str) -> str:
        """Assembles the full prompt from individual markdown blocks."""
        system_prompt = self._read_file("system.md")
        examples = self._read_file("examples.md")
        task_template = self._read_file(f"{self.version}.md")
        
        # Read the global JSON schema format requirement
        # Typically this could be read from a shared prompt file, here we inject it directly
        output_format = "OUTPUT_FORMAT: JSON matching the AgentOutput schema exactly."

        assembled_prompt = f"""
{system_prompt}

### Context Analysis
{yaml.dump(context)}

### Hierarchical Memory
{yaml.dump(memory)}

### Retrieved Medical Knowledge (RAG)
{chr(10).join(rag_data) if rag_data else 'None'}

### Current Task
{task_template.format(current_task=current_task) if task_template else current_task}

### Few-Shot Examples
{examples}

### Output Requirements
{output_format}
"""
        return assembled_prompt

    def build_verification_prompt(self, original_prompt: str, generated_output: str) -> str:
        verification_rules = self._read_file("verification.md")
        
        return f"""
You are a highly critical Medical AI Verification Engine.
Review the following generated output against the original task and verification rules.

Original Task Context:
{original_prompt[:1000]}... [TRUNCATED]

Generated Output:
{generated_output}

Verification Rules:
{verification_rules}

Check for Schema compliance, Medical rules, Workflow rules, Output format, Tool consistency, Hallucinations.
Return ONLY valid JSON correcting any errors found, matching the AgentOutput schema.
"""

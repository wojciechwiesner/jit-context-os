"""
System Prompt Extension for JIT-Context.
Injects deterministic, prompt-cache optimized JIT Capsule into the agent system prompt.
"""

from helpers.extension import Extension
from helpers import plugins
from agent import LoopData
from usr.plugins.jit_context.helpers.runtime import JITContextRuntime


class JITContextExtension(Extension):
    async def execute(
        self,
        system_prompt: list[str] = [],
        loop_data: LoopData = LoopData(),
        **kwargs,
    ):
        if not self.agent:
            return

        config = plugins.get_plugin_config("jit_context", agent=self.agent) or {}
        if config.get("mode", "active") == "disabled":
            return

        runtime = JITContextRuntime()
        capsule = runtime.compile_capsule(agent=self.agent, config=config)
        if capsule:
            system_prompt.append(capsule)

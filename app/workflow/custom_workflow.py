from __future__ import annotations

import types
from functools import partial
from queue import Queue

from workflow.autogen_workflow import AutogenWorkflow
from autogen import ChatResult, GroupChat, AssistantAgent, UserProxyAgent, GroupChatManager, ConversableAgent, config_list_from_json

from util.stream_util import streamed_print_received_message

config_list = config_list_from_json("./OAI_CONFIG_LIST.json")
llm_config = {"config_list": config_list}

class CustomWorkflow(AutogenWorkflow):

    assistantManager: ConversableAgent

    def __init__(self):
        self.queue: Queue | None = None
        self.user_proxy = UserProxyAgent(
            name="UserProxy",
            system_message="You are the UserProxy. You are the user in this conversation.",
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "workspace", "use_docker": False},
            llm_config=llm_config,
            description="The UserProxy is the user in this conversation. They will be interacting with the other agents in the group chat.",
        )
        self.code_assistant = AssistantAgent(
            name="code assistant",
            system_message="""
                You are the code assistant. You are an AI assistant that can help with code-related tasks.
            """,
            max_consecutive_auto_reply = 5,
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "workspace", "use_docker": False},
            llm_config=llm_config,      
        )

        self.chat_manager = self.code_assistant
        
   

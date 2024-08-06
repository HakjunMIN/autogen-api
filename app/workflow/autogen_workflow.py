from __future__ import annotations

import types
from functools import partial
from queue import Queue

from autogen import ChatResult, GroupChat, AssistantAgent, UserProxyAgent, GroupChatManager, config_list_from_json

from util.stream_util import streamed_print_received_message

config_list = config_list_from_json("./OAI_CONFIG_LIST.json")
llm_config = {"config_list": config_list}

class AutogenWorkflow:
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
            code_execution_config=False,
            llm_config=llm_config,      
        )
        self.critic_assistant = AssistantAgent(
            name="critic assistant",
            system_message="""
                You are the critic assistant. You are an AI assistant that can help with critiquing tasks.
            """,
            max_consecutive_auto_reply=5,
            human_input_mode="NEVER",
            code_execution_config=False,
            llm_config=llm_config,
        )

        self.group_chat_with_introductions = GroupChat(
            agents=[
                self.user_proxy,
                self.code_assistant,
                self.critic_assistant,
            ],
            messages=[],
            max_round=10,
            send_introductions=True,
        )
        self.chat_manager = GroupChatManager(
            groupchat=self.group_chat_with_introductions,
            llm_config=llm_config,
        )

    def set_queue(self, queue: Queue):
        self.queue = queue

    def run(
            self,
            message: str,
            stream: bool = False,
    ) -> ChatResult:

        if stream:
            # currently this streams the entire chat history, but you may want to return only the last message or a
            # summary
            index_counter = {"index": 0}
            queue = self.queue

            def streamed_print_received_message_with_queue_and_index(
                    self, *args, **kwargs
            ):
                streamed_print_received_message_with_queue = partial(
                    streamed_print_received_message,
                    queue=queue,
                    index=index_counter["index"],
                )
                bound_method = types.MethodType(
                    streamed_print_received_message_with_queue, self
                )
                result = bound_method(*args, **kwargs)
                index_counter["index"] += 1
                return result

            self.chat_manager._print_received_message = types.MethodType(
                streamed_print_received_message_with_queue_and_index,
                self.chat_manager,
            )

        chat_history = self.user_proxy.initiate_chat(
            self.chat_manager, message=message,
        )
        if stream:
            self.queue.put("[DONE]")
        # currently this returns the entire chat history, but you may want to return only the last message or a summary
        return chat_history

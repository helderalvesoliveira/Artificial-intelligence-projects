from crewai.utilities.events.base_event_listener import BaseEventListener
from crewai.utilities.events import LLMStreamChunkEvent,LLMCallCompletedEvent
from crewai.utilities.events.base_event_listener import BaseEventListener

class MyCustomListener(BaseEventListener):
    def __init__(self, placeholder):
        super().__init__()
        self.placeholder = placeholder
        self.current_text = ""

    def setup_listeners(self, crewai_event_bus):

        @crewai_event_bus.on(LLMStreamChunkEvent)
        def on_llm_chunk(source, event: LLMStreamChunkEvent):
            self.current_text += event.chunk
            self.placeholder.markdown(self.current_text)

        """ @crewai_event_bus.on(AgentExecutionStartedEvent)
        def on_agent_execution_started(source, event: AgentExecutionStartedEvent):
            self.placeholder.markdown(self.current_text)
            self.placeholder.success("✅ Agent execution started: {event}") """   
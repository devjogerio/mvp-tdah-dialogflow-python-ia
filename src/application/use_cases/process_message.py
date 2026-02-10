from src.application.dtos.message_dto import ProcessMessageInput, ProcessMessageOutput
from src.domain.interfaces.repositories import ContextRepository, LLMProvider
from src.utils.safety_filters import (  # Assuming this exists, will refactor later to be injectable
    check_safety,
)


class ProcessUserMessage:
    def __init__(self, llm_provider: LLMProvider, context_repo: ContextRepository):
        self.llm_provider = llm_provider
        self.context_repo = context_repo

    def execute(self, input_dto: ProcessMessageInput) -> ProcessMessageOutput:
        # 1. Check Safety
        is_safe, emergency_msg = check_safety(input_dto.message)
        if not is_safe:
            return ProcessMessageOutput(response_text=emergency_msg, risk_detected=True)

        # 2. Retrieve Context (RAG)
        context = self.context_repo.retrieve_context(input_dto.message)

        # 3. Invoke LLM
        response_text = self.llm_provider.invoke(
            prompt=input_dto.message, context={"rag_content": context}
        )

        return ProcessMessageOutput(response_text=response_text, risk_detected=False)

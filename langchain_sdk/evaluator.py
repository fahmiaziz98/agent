from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from llm.gemini import LLM_CHAIN, llm
from prompt.prompt import INSTRUCTIONS, SHARED_CONTEXT
from schema.models import Grade
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client

client = Client()


def target(inputs: dict) -> dict:
    response = LLM_CHAIN.invoke({"question": inputs["question"], "context": SHARED_CONTEXT})
    return {"response": response}

def accuracy(outputs: str, refrence_outputs: str) -> bool:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", INSTRUCTIONS),
            ("user", """
                        Ground Truth: {refrence_output};
                        Student Answer: {outputs};
            """),
        ]
    )
    llm_structure = prompt | llm.with_structured_output(Grade)
    set_llm_cache(InMemoryCache())
    response = llm_structure.invoke({"refrence_output": refrence_outputs, "outputs": outputs})
    return response.score

def correctness(inputs, outputs, reference_outputs) -> bool:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", INSTRUCTIONS),
            ("user", """
                You are grading the following question: {inputs};
                Here is the real answer: {outputs};
                You are grading the following predicted answer: {reference_outputs}
            """),
        ]
    )
    llm_structure = prompt | llm.with_structured_output(Grade)
    set_llm_cache(InMemoryCache())
    response = llm_structure.invoke({"inputs": inputs, "outputs": outputs, "reference_outputs": reference_outputs})
    return response.score


if __name__ == "__main__":
    print("Starting to evaluate...")
    try:
        # Evaluate the model using the Langsmith client
        experiment_results = client.evaluate(
            target,
            data = "LS_EVAL",
            evaluators = [
                accuracy,
                correctness
            ],
            experiment_prefix = "first-eval-in-langsmith",
            max_concurrency = 2,
        )
        print("Evaluation completed successfully.")
        
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")
    
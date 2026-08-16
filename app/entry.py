from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from ya_llm.ya_embed import getQueryEmbeddings
from ya_llm.ya_llm import generateQueryAnswer
from helpers.json import buildContext


rag_chain = (
    {
        "context": (
            RunnableLambda(getQueryEmbeddings)
            | RunnableLambda(buildContext)
        ),
        "question": RunnablePassthrough(),
    }
    | RunnableLambda(lambda x: generateQueryAnswer(
        x["question"],
        x["context"]
    ))
)

def ask(question: str):
    return rag_chain.invoke(question)
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

document_analysis_prompt = ChatPromptTemplate.from_template("""
You are highly capable AI model that to analyzes documents and summarizes their content.
Return only JSON matching the exact schema below:
                                          
{format_instructions}
                                          
Analyze the following document:
                                          
{document_text}""")

document_comparison_prompt = ChatPromptTemplate.from_template("""
You will be provided with content from two documents. Your task is follows:
1. Compare the content of the two documents.    
2. Identify the differences in pdfs and note the page numbers where changes occur.
3.The output you provide must be page wise comparison.
4. If any page do not have any changes, mention "No changes" for that page.
                                                              
input documents:
{combined_docs}

Your response should be follow this format:
{format_instructions}
""")


# Prompt for contextual question rewriting
contextualize_question_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Given a conversation history and the most recent user query, rewrite the query as a standalone question "
        "that makes sense without relying on the previous context. Do not provide an answer—only reformulate the "
        "question if necessary; otherwise, return it unchanged."
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Prompt for answering based on context
context_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an assistant designed to answer questions using the provided context. Rely only on the retrieved "
        "information to form your response. If the answer is not found in the context, respond with 'I don't know.' "
        "Keep your answer concise and no longer than three sentences.\n\n{context}"
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Central dictionary to register prompts
PROMPT_REGISTRY = {
    "document_analysis": document_analysis_prompt,
    "document_comparison": document_comparison_prompt,
    "contextualize_question": contextualize_question_prompt,
    "context_qa": context_qa_prompt,
}
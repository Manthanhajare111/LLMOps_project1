from langchain_core.prompts import ChatPromptTemplate

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

PROMPT_REGISTRY = {
    "document_analysis": document_analysis_prompt,
    "document_comparison": document_comparison_prompt
}
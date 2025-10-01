from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are highly capable AI model that to analyzes documents and summarizes their content.
Return only JSON matching the exact schema below:
                                          
{format_instructions}
                                          
Analyze the following document:
                                          
{document_text}""")
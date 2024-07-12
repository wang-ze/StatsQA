This repo is to demonstrate different ways that one can use GenAI techinques. 

In the *STATQA_Groq* notebook, I use the Meta Llama 3 **llama3-8b-8192** model available through groq to generate a quiz with questions related to a statistics area, and also evaluate the quiz. The model is access through the **Groq API**. After the initial setup, including the prompt templates, I use **LangChain** to create and then connect two calls of the LLM (i.e., two chains). The first chain is to generate a quiz and the second chain uses the generated quiz as an input and evaluates the quiz. 

The prompt template is set up so that quiz generation uses local data. Therefore, the generation is Retrieval Augmented Generation (RAG). I did not use an embedding model to create a vector store in this example though (Embeddings will be used in future examples.)


Further, I created a simple interactive app using Streamlit to do the same thing (i.e. generate a quiz and evlauate the quiz) based on user input (uploading a file in text of pdf format, and specifying the number of questions, the statistics area, and the grade/level for which the quiz is for). 

If you are a statistician/quantitative methodologist, I would recommend looking into the LangChain ecosystem, especially the [LangChain Expression Language (LCEL)](https://python.langchain.com/v0.1/docs/expression_language/).

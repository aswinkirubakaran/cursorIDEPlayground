# cursorIDEPlayground
This repo contains files and code generated in Cursor IDE during vibe coding

On 23 July 2025
  
  Installed Cursor IDE and derived a simple use case to create an agent that fetches basic system health check statistics.
  Based on the interaction with IDE, created a sample python code thas uses GPT4.0 as language model(by open AI/hugging face) and Gradio to host the UI
  Although the code executed, the expected results were not produced, and multiple errors were encountered.
  
On 24 July 2025
  
  Intended to use a better model by inferencing Groq tool, and fixing the code to produce intended results

  
  The code's environmental key was replaced by Groq secret API
  prompt - "Okay let us make some changes, Instead of using huggingface api i need to inference Groq API to invoke a LLM model ie Gemma
            shall we begin?"
  This prompt adjusted the necessary piece of line to adapt and further the local machine (current system) was used to fetch the data (disk usage,memory,network status etc)
  While playing with the code the suggested version of Gemma was not giving the result, Later it was found that the version was deprecated. So had to upgrade the model to current version
  Now the ecpected results are generated.
  Finally asked the AI chat to clean the code and remove unnecessary lines.


On 25 July 2025
  
  Intended to design/think the use case into a MVP and start to add more details to it

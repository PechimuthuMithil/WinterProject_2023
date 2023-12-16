# Optimised Lost and Found Website
This repository contains the implementation of  a Lost and Found webpage and more.
## Contributors
-- Husain Malwat  
-- Mithil Pechimuthu  
-- Shreesh Agarwal  

## Structure of the Website
![Website_flow](https://github.com/PechimuthuMithil/WinterProject_2023/assets/119656326/fafd3ebf-a111-463a-8030-93e8da596a92)

## Search algorithm  
Current methods used:
1) Searching the database of found items using `Jaccard Similarity`. The source code for this can be found in JaccardRanker.py. This ranker is also optimized by using multiple threads of execution to search through the database.
2) Searching a vector database, by encoding the user's query using sentence transformers or using the [OpenAI API](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings). `Cosine Similarity` is used in this case. The surce code can be found in the ProposedRanker.pynb.

   

# Optimised Lost and Found Website
This repository contains the implementation of  a Lost and Found webpage and more.

## Tools and Skills Used
[![My Skills](https://skillicons.dev/icons?i=flask,html,css,py,vscode,git,postgres)](https://skillicons.dev)  

## Contributors
-- Husain Malwat  
-- Mithil Pechimuthu  
-- Shreesh Agarwal  

## Structure of the Website
![Website_flow](https://github.com/PechimuthuMithil/WinterProject_2023/assets/119656326/fafd3ebf-a111-463a-8030-93e8da596a92)

## Search algorithm  
Current methods used:
1) Searching the database of found items using `Jaccard Similarity`. The source code for this can be found in JaccardRanker.py. This ranker is also optimized by using multiple threads of execution to search through the database.
2) Searching a vector database, by encoding the user's query using sentence transformers or using the [OpenAI API](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings). `Cosine Similarity` is used in this case. The surce code can be found in the ProposedRanker.ipynb.

## Note to the reader
This is a simple website, with a simple, under development server. The backend is working, but might have some loop holes. The websote layout is exactly as shown in the figure in the section `Structure of the Website`. There aren't even any go back or home buttons. But I believe that these are small and simple additions. The `ProposedRanker.ipynb` contains an transformerbased search approach that is also being worked upon.  

## Runing the Server
### Requirements  
Please enusre that the following requirements are satisfied by the host machine.
1) Python interpreter.
2) Have a postgreSQL database.
3) Install flask.
   ```
   pip install flask
   ```
4) Install the nltk library.
   ```
   pip install nltk
   ```

### Starting the server.
First clone the repository.  
Open youe CLI and type
```
git clone https://github.com/PechimuthuMithil/WinterProject_2023.git
```

Please run the `Run.py` script to set up the required relations and download necessary dependencies.  
Please ensure that the database details are properly configures in the `Run.py` script according to the host machine.  
The server will start and one can follow the instriction on the console to view the website.  

## Some side points.
We can give a domain name to the website as follows. 
### For Windows users
1) Go to the hosts file. It can be typically found here `C:\Windows\System32\drivers\etc\hosts`.
2) Add the following translation
  `127.0.0.1   lostnfound.iitgn.ac.in`
   After that your hosts file should look somewhat like this.  
   ![image](https://github.com/PechimuthuMithil/WinterProject_2023/assets/119656326/73e2cae0-ad5f-4484-8731-ecf503e65171)  

Now lostnfound.iitgn.ac.in is mapped to 127.0.0.1, i.e. the local host and now we can access it like an actual website.
So if we type `http://lostnfound.iitgn.ac.in:5000/` on our browser, we will be able to access the webpage!  
We can also crete our own personal local netowrk, and set up the server in one computer and access the webpae from another computer. However this is left as an exercise to the reader.


## Future Work
1) Add encryption of data and use TLS protocols over TCP. This will be done to make the server suppirt HTTPS requests.
2) Clean the code and make a Node.js equivalent.
3) Provide a better and neater front end.
4) Use vector databases.  

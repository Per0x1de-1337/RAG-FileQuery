# Pathway RAG Application

This project is a **Retriever-Augmented Generation (RAG)** application utilizing the **Pathway framework**. The application indexes documents from various sources (such as Google Drive and Microsoft SharePoint), allowing real-time search and answering functionalities. It also uses the **Gemini LLM** model for embedding documents.

## Project Structure

Below is the project structure of the app:

### Files and Directories

- **app.py**: Main application file that runs the app logic and integrates Pathway modules.
- **config.yaml**: Configuration file that stores settings related to data sources and other parameters.
- **data/**: Directory containing PDF files that the app indexes and processes.
  - *PDF files*: These are example documents that the app can use for retrieval and answering queries.
- **Dockerfile**: Defines the Docker image for containerization, which is used for deployment.
- **README.md**: Documentation file explaining how to set up and run the application.
- **requirements.txt**: Lists all the dependencies required to run the app (e.g., Pathway, other Python libraries).
- **server.py**: Contains the server logic, defines endpoints for making POST requests.
- **static/styles.css**: Contains the CSS for styling the front-end HTML pages.
- **templates/**: Contains the HTML files used for rendering the front-end pages.
  - *index.html*: Main page of the app.
  - *logs.html*: A page to display logs or other app-related information.

## Key Features

1. **Real-Time Document Indexing**: The app indexes documents from sources like Google Drive and Microsoft SharePoint.
2. **Embedding with Gemini LLM**: It uses the Gemini LLM model to create embeddings for the documents.
3. **Retriever-Augmented Generation (RAG)**: The app retrieves relevant documents and generates answers to user queries.
4. **Containerized Deployment**: The app can be containerized and deployed via Docker for scalability.

## How to Use

1. Clone the repository.
2. Install dependencies using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
3. Run the app using Docker:
    `docker build -t pathway-rag-app . |
docker run -p 5000:9000 pathway-rag-app
`
4. If docker is not working try running with this command
   `python3 app.py` and
   `python3 server.py`
5. Access the app via your browser at http://localhost:5000.
6. And finally interact with the app.

## Configuration
1. Update the config.yaml file to specify the data sources (Google Drive, SharePoint, etc.).
2. Add your own Gemini-api-key in `.env` file.

3. Modify the app.py or server.py to adjust any specific logic for your use case.

## API Endpoints
`POST /v1/pw_ai_answer`: Endpoint for submitting a question and receiving an answer based on indexed documents.`

## Technologies Used
1. **Pathway Framework**: For real-time data processing and RAG capabilities.
2. **Gemini LLM**: For embedding and semantic search.
3. **Docker**: For containerization and deployment.
4. **Python**: Backend logic and server implementation.
5. **HTML/CSS**: Front-end rendering of the app.

## License
This project is licensed under the MIT License.

```bash
This file can serve as a basic structure for documentation purposes. You can customize it further based on additional features or details.

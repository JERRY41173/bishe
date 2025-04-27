from langchain_unstructured import UnstructuredLoader
import tempfile

def file_to_text(file: bytes) -> str:
    # Write the bytes to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
        tmp.write(file)
        tmp.flush()
        temp_path = tmp.name

    # Use langchain's UnstructuredFileLoader to load the file content
    loader = UnstructuredLoader(temp_path)
    docs = loader.load()
    
    # Combine all page contents into a single string and return
    return "\n".join(doc.page_content for doc in docs)

if __name__ == "__main__":
    # Example usage
    with open("/srv/bishe/temp/CK7516数控车床投标书.docx", "rb") as f:
        file_content = f.read()
        text = file_to_text(file_content)
        print(text)
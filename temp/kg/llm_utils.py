import json
from langchain_deepseek import ChatDeepSeek

def call_llm(system_msg, user_msg, supplier):
    try:
        if supplier == "deepseek":
            llm = ChatDeepSeek(
                model="deepseek-chat",
                temperature=1.0,
                max_tokens=1024,
                timeout=None,
                max_retries=2,
            )
            
            messages = [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ]
        else:
            raise ValueError(f'Invalid LLM supplier: {supplier}')

        # Call LLM
        res = llm.invoke(messages)
        if not res or not res.content:
            raise ValueError("API returned empty response")
            
        output = res.content
        
        # Validate JSON format and structure
        data = json.loads(output)
        if not isinstance(data, dict):
            raise ValueError("API response is not a valid JSON object")
        
        if 'nodes' not in data or 'edges' not in data:
            raise ValueError("API response missing required 'nodes' or 'edges' fields")
            
        if not isinstance(data['nodes'], list) or not isinstance(data['edges'], list):
            raise ValueError("'nodes' and 'edges' must be arrays")
            
        if len(data['nodes']) < 3:
            raise ValueError("At least 3 nodes are required")
            
        # Print output for debugging
        # st.write("Extraction result:")
        # st.info(output, icon="🎯")
        return output
            
    except json.JSONDecodeError as je:
        # st.error(f"Invalid JSON format in API response: {str(je)}")
        return '{"nodes": [], "edges": []}'
    except ValueError as ve:
        # st.error(str(ve))
        return '{"nodes": [], "edges": []}'
    except Exception as e:
        # st.error(f"API call error: {str(e)}")
        return '{"nodes": [], "edges": []}' 
    
#测试
if __name__ == "__main__":
    system_msg = "System message for the LLM"
    user_msg = "User message for the LLM"
    supplier = "deepseek"  # or "azure"
    
    # Call the function with test messages
    call_llm(system_msg, user_msg, supplier)
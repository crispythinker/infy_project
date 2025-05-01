import wikipedia

def wiki(query):
    """
    Perform a Wikipedia search based on the detected combination in the query and return the first 3 sentences.

    Parameters:
        query (str): The user's spoken or typed input.

    Returns:
        str: The first 3 sentences of the Wikipedia search result or an error message.
    """
    combinations = [
        "what is", "what are", "what was", "what will", "what can", "what could", "what should",
        "what did", "what do", "what have", "what has", "what had", "what might", "what must", "what may",
        "who is", "who are", "who was", "who will", "who can", "who could", "who should", "who did",
        "who do", "who have", "who has", "who had", "who might", "who must", "who may",
        "when is", "when did", "when will", "when can", "when could", "when should", "when do",
        "when have", "when has", "when had", "when might", "when must", "when may",
        "how", "how was", "how will", "how can", "how could", "how should", "how did",
        "how do", "how have", "how has", "how had", "how might", "how must", "how may",
        "which", "which was", "which will", "which can", "which could", "which should", "which did",
        "which do", "which have", "which has", "which had", "which might", "which must", "which may"
    ]
 
    if any(keyword in query for keyword in combinations):
        try:
            detected_combination = next(keyword for keyword in combinations if keyword in query)
            search_query = query.split(detected_combination)[1].strip()

            search_result = wikipedia.summary(search_query, sentences=3)
            return search_result

        except wikipedia.exceptions.DisambiguationError:
            return "Wikipedia search returned a disambiguation page. Please refine your query."

        except Exception as e:
            return f"An error occurred while searching Wikipedia: {e}"

    return "No valid combination found in the query."

import os
import subprocess
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

def get_git_diff():
    """
    Runs 'git diff' to see changes between the latest commit 
    and the one before it.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        return None

def generate_pr_description(diff_text):
    prompt = f"""
    You are a helpful DevOps assistant. 
    Below is a git diff of a code change. 
    Write a concise PR description.
    
    DIFF:
    {diff_text}
    """
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("--- Extracting Git Diff ---")
    diff = get_git_diff()
    
    if diff:
        print("--- Sending Diff to Gemini ---")
        description = generate_pr_description(diff)
        print("\n--- Generated Description ---")
        print(description)
    else:
        print("No diff found or error occurred.")
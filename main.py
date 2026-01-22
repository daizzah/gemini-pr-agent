import os
import subprocess
import google.generativeai as genai

# 1. Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

def get_git_diff():
    """
    Configures git security and runs git show.
    """
    try:
        # Tell git to trust the GitHub workspace directory despite ownership differences
        subprocess.run(
            ["git", "config", "--global", "--add", "safe.directory", "/github/workspace"],
            check=True
        )
        
        # Now run the actual git show command
        result = subprocess.run(
            ["git", "show", "--format=", "HEAD"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        return None

def generate_pr_description(diff_text):
    prompt = f"""
    You are a helpful DevOps assistant. 
    Below is a git diff of a code change. 
    Write a concise PR description in Markdown format.
    
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
        
        with open("pr_description.md", "w") as f:
            f.write(description)
            
        print("Description saved to pr_description.md")
    else:
        print("No diff found or error occurred.")
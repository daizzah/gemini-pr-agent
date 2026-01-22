import os
import subprocess
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
action_type = os.getenv("ACTION_TYPE", "description").lower()

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

def get_git_diff():
    try:
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", "/github/workspace"], check=True)
    except subprocess.CalledProcessError:
        pass

    try:
        return subprocess.run(["git", "diff", "HEAD~1", "HEAD"], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        try:
            return subprocess.run(["git", "show", "--format=", "HEAD"], capture_output=True, text=True, check=True).stdout
        except subprocess.CalledProcessError:
            return None

def generate_content(diff_text, mode):
    if mode == "review":
        print("--- Mode: Code Review ---")
        prompt = f"""
        You are a Senior Software Engineer. Review the following code changes.
        Focus on:
        1. Potential bugs or security risks.
        2. Code style and best practices.
        3. Performance improvements.
        
        Be constructive and concise. Format in Markdown.
        
        DIFF:
        {diff_text}
        """
    else:
        print("--- Mode: PR Description ---")
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
    print(f"--- Action started in mode: {action_type} ---")
    diff = get_git_diff()
    
    if diff:
        print("--- Sending Diff to Gemini ---")
        output = generate_content(diff, action_type)
        
        with open("pr_description.md", "w") as f:
            f.write(output)
            
        print("Output saved to pr_description.md")
    else:
        print("No diff found.")
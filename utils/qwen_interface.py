import subprocess
import json
import tempfile
import os
import streamlit as st

class QwenCLI:
    def __init__(self):
        self.check_qwen_installation()
    
    def check_qwen_installation(self):
        """Check if Qwen Code CLI is available"""
        try:
            subprocess.run(
                ["qwen-code", "--version"],
                check=True,
                capture_output=True,
                text=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try to install if not found
            self._install_qwen_code()
    
    def _install_qwen_code(self):
        """Attempt to install Qwen Code CLI"""
        try:
            st.info("Installing Qwen Code CLI...")
            # Install Node.js first if needed
            subprocess.run(
                ["curl", "-qL", "https://www.npmjs.com/install.sh", "|", "sh"],
                shell=True,
                check=True
            )
            # Install Qwen Code
            subprocess.run(
                ["npm", "install", "-g", "@qwen-code/qwen-code"],
                check=True
            )
            st.success("Qwen Code CLI installed successfully!")
        except Exception as e:
            raise RuntimeError(
                f"Failed to install Qwen Code CLI: {str(e)}\n"
                "Please install it manually: npm i -g @qwen-code/qwen-code"
            )
    
    def summarize(self, text, max_length=150):
        """Generate summary using Qwen Code CLI"""
        prompt = self._create_prompt(text, max_length)
        
        try:
            # Call Qwen Code CLI directly with prompt
            result = subprocess.run(
                ["qwen-code", "-p", prompt],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Extract summary from output
            summary = self._parse_output(result.stdout)
            return summary
            
        except subprocess.CalledProcessError as e:
            # Fallback: try with file input
            return self._summarize_with_file(prompt)
    
    def _summarize_with_file(self, prompt):
        """Alternative method using file input"""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False
        ) as f:
            f.write(prompt)
            temp_path = f.name
        
        try:
            result = subprocess.run(
                ["qwen-code", "-f", temp_path],
                capture_output=True,
                text=True,
                check=True
            )
            return self._parse_output(result.stdout)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _create_prompt(self, text, max_length):
        """Create summarization prompt"""
        return f"""Please summarize the following text in approximately {max_length} words. 
Provide a clear and concise summary that captures the main points.

Text to summarize:
{text}

Summary:"""
    
    def _parse_output(self, output):
        """Parse Qwen Code CLI output to extract summary"""
        # Clean the output
        output = output.strip()
        
        # If output contains "Summary:" marker, extract after it
        if "Summary:" in output:
            parts = output.split("Summary:", 1)
            if len(parts) > 1:
                return parts[1].strip()
        
        # Otherwise, return the cleaned output
        return output if output else "Failed to generate summary."

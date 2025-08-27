import subprocess
import json
import tempfile
import os

class QwenCLI:
    def __init__(self):
        self.check_qwen_installation()
    
    def check_qwen_installation(self):
        """Check if Qwen Coder CLI is available"""
        try:
            subprocess.run(
                ["qwen", "--version"],
                check=True,
                capture_output=True,
                text=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "Qwen Coder CLI not found. Please install it first.\n"
                "Visit: https://github.com/QwenLM/CodeQwen"
            )
    
    def summarize(self, text, max_length=150):
        """Generate summary using Qwen Coder CLI"""
        prompt = self._create_prompt(text, max_length)
        
        # Write prompt to temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False
        ) as f:
            f.write(prompt)
            temp_path = f.name
        
        try:
            # Call Qwen CLI
            result = subprocess.run(
                ["qwen", "generate", "--input", temp_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Extract summary from output
            summary = self._parse_output(result.stdout)
            return summary
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _create_prompt(self, text, max_length):
        """Create summarization prompt"""
        return f"""Please summarize the following text in approximately {max_length} words:

{text}

Summary:"""
    
    def _parse_output(self, output):
        """Parse Qwen CLI output to extract summary"""
        # Remove any CLI metadata or formatting
        lines = output.strip().split('\n')
        
        # Find where the actual summary starts
        summary_start = 0
        for i, line in enumerate(lines):
            if "Summary:" in line:
                summary_start = i + 1
                break
        
        # Extract and clean summary
        summary = '\n'.join(lines[summary_start:]).strip()
        return summary if summary else "Failed to generate summary."

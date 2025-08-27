import subprocess
import json
import tempfile
import os
import streamlit as st

class QwenCLI:
    def __init__(self):
        # Don't check installation on init to avoid blocking app startup
        self.cli_available = self._check_cli_availability()
    
    def _check_cli_availability(self):
        """Check if Qwen Code CLI is available without throwing errors"""
        try:
            subprocess.run(
                ["qwen-code", "--version"],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def summarize(self, text, max_length=150):
        """Generate summary using Qwen Code CLI or fallback method"""
        if not self.cli_available:
            return self._fallback_summarize(text, max_length)
        
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
            # Fallback to alternative method
            return self._fallback_summarize(text, max_length)
    
    def _fallback_summarize(self, text, max_length):
        """Fallback summarization when Qwen CLI is not available"""
        st.warning("⚠️ Qwen Code CLI not available. Using basic summarization.")
        
        # Simple extractive summarization fallback
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return "No content to summarize."
        
        # Calculate how many sentences to include
        words_per_sentence = len(text.split()) / len(sentences) if sentences else 20
        target_sentences = int(max_length / words_per_sentence)
        target_sentences = max(1, min(target_sentences, len(sentences)))
        
        # Take first and most important sentences
        summary_sentences = sentences[:target_sentences]
        summary = '. '.join(summary_sentences) + '.'
        
        return summary
    
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

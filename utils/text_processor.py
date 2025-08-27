import re

class TextProcessor:
    def preprocess(self, text):
        """Clean and prepare text for summarization"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\']', '', text)
        
        # Ensure text ends with period
        if text and text[-1] not in '.!?':
            text += '.'
        
        return text
    
    def count_words(self, text):
        """Count words in text"""
        return len(text.split())
    
    def calculate_reduction(self, original, summary):
        """Calculate percentage reduction"""
        original_words = self.count_words(original)
        summary_words = self.count_words(summary)
        
        if original_words == 0:
            return 0.0
        
        reduction = (1 - summary_words / original_words) * 100
        return max(0.0, reduction)

import streamlit as st
from utils.qwen_interface import QwenCLI
from utils.text_processor import TextProcessor
from config import APP_CONFIG

def main():
    st.set_page_config(
        page_title=APP_CONFIG["title"],
        page_icon=APP_CONFIG["icon"],
        layout="wide"
    )
    
    st.title("📝 Text Summarizer with Qwen Coder")
    st.markdown("---")
    
    # Initialize components
    qwen = QwenCLI()
    processor = TextProcessor()
    
    # Show CLI status
    if qwen.cli_available:
        st.success("✅ Qwen Code CLI is available")
    else:
        st.info(
            "ℹ️ Qwen Code CLI not found. Using fallback summarization.\n\n"
            "For best results, install Qwen Code CLI locally:\n"
            "```bash\n"
            "npm i -g @qwen-code/qwen-code\n"
            "```"
        )
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_text = st.text_area(
            "Enter your text to summarize:",
            height=300,
            placeholder="Paste your text here..."
        )
    
    with col2:
        st.markdown("### Options")
        max_length = st.slider(
            "Summary length (words)",
            min_value=50,
            max_value=500,
            value=150,
            step=50
        )
        
        summarize_btn = st.button(
            "🚀 Summarize",
            type="primary",
            use_container_width=True
        )
    
    # Output section
    if summarize_btn and input_text:
        with st.spinner("Generating summary..."):
            try:
                # Preprocess text
                processed_text = processor.preprocess(input_text)
                
                # Generate summary
                summary = qwen.summarize(
                    processed_text,
                    max_length=max_length
                )
                
                # Display results
                st.markdown("### 📋 Summary")
                st.success(summary)
                
                # Show statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Original Words", processor.count_words(input_text))
                with col2:
                    st.metric("Summary Words", processor.count_words(summary))
                with col3:
                    reduction = processor.calculate_reduction(input_text, summary)
                    st.metric("Reduction", f"{reduction:.1f}%")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif summarize_btn:
        st.warning("Please enter some text to summarize.")

if __name__ == "__main__":
    main()

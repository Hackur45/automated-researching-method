
### AI Research Generator 🤖📚

The idea is that the agent will be prompted with a question, and based on the question, it will counter-question the user to gain more insights. It will then pass this information to the web researcher, who will conduct thorough research on the topic and provide the research insights to a LaTeX converter. The LaTeX converter will then pass the results to the PDF maker, and the final document will be saved to the user's directory.


## 🎯 Project Overview

The **AI Research Generator** is a platform that automates the entire research paper generation process through a series of intelligent AI agents:

1. **Question Agent**: Analyzes user prompts and generates clarifying questions.
2. **Research Agent**: Performs in-depth web research based on the refined prompts.
3. **LaTeX Converter**: Transforms the research findings into an academic paper format.
4. **PDF Generator**: Produces the final, downloadable research paper.

### Our Idea

We aim to build a research hub like arXiv but with a twist: instead of traditional researchers, anyone can prompt the system to generate research papers, making it accessible to anyone curious enough to ask a question.

## 💻 Tech Stack

### Application Stack
- **Frontend**: React.js
- **Backend**: Flask + Node.js
- **Storage**: Local file system (for now)

### AI Stack
- **CrewAI** for agent orchestration
- **Hugging Face models** for natural language processing
- **GROQ API** integration for high-performance model inference

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-research-generator.git
   cd ai-research-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r -q  requirements.txt 
   ```

3. Set up environment variables:
   ```bash
   # Create a .env file and add your API keys
   GROQ_API_KEY="YOUR_KEY_GOES_HERE"
   ```

4. Get your API key here:
   - GROQ API key ([Get it here](https://console.groq.com/playground))

## 🌟 Future Plans

While we’re still in development, our roadmap includes:
- Transitioning to open-source models through Hugging Face Hub
- Implementing a paper review system
- Adding collaboration features
- Creating a searchable paper database

## 🤝 Contributing

We’re excited to have contributions from the community! Feel free to fork the repo and submit a Pull Request. We’d love to see what you create!


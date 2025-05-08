
# Agents Framework

This repository contains learning materials and implementations for building agents from scratch or using frameworks such as LangGraph, LangChain, Crew AI, and others. The main focus of this repository is on agent evaluation, writing effective prompts, token optimization, caching, and integration with various APIs. This repository will be continuously updated over time.

## Installation

### 1. Install UV
UV is a tool for managing virtual environments and running scripts easily. Install UV using the following command:
```bash
curl -Ls https://astral.sh/uv/install.sh | bash

export PATH="$HOME/.local/bin:$PATH"
```

### 2. Clone the Repository
Clone this repository to your local directory:
```bash
git clone https://github.com/fahmiaziz98/agent.git
cd agent
```

### 3. Create a Virtual Environment
Create a virtual environment using UV:
```bash
uv venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
Install all required dependencies:
```bash
uv pip install -r requirements.txt
```

### 5. Create a `.env` File
Create a `.env` file in the root directory of the project and add the following environment variables:
```env
GROQ_API_KEY=your_groq_api_key
GROQ_BASE_URL=your_groq_base_url
WHEATER_API_KEY=your_weather_api_key
SERPER_API_KEY=your_serper_api_key
TAVILY_API_KEY=your_tavily_api_key
HF_API_KEY=your_huggingface_api_key
```

You can obtain the API keys from the following services:
- **Groq**: [Groq Documentation](https://console.groq.com/docs/overview)
- **WeatherStack**: [WeatherStack API](https://weatherstack.com/)
- **Tavily**: [Tavily API](https://app.tavily.com/home)
- **SerpAPI**: [SerpAPI](https://serpapi.com/)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.
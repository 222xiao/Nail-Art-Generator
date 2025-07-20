# Clone repository
git clone https://github.com/yourusername/nail-art-generator.git
cd nail-art-generator

# Create virtual environment
python -m venv venv

# Activate environment (Linux/Mac)
source venv/bin/activate

# Activate environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
echo "DASHSCOPE_API_KEY=your_api_key_here" > .env

# Run application
python app.py
Visit http://localhost:5001 to start designing!

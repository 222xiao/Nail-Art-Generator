from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import dashscope
from dashscope import ImageSynthesis
from http import HTTPStatus
import logging
from dotenv import load_dotenv

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
if not dashscope.api_key:
    logger.error("DASHSCOPE_API_KEY not set")
    raise ValueError("Please set DASHSCOPE_API_KEY in the .env file")

def verify_api_key():
    try:
        response = dashscope.Generation.call(
            model='qwen-max',
            prompt='Test API key',
            max_tokens=10
        )
        return response.status_code == 200
    except Exception:
        return False

if not verify_api_key():
    logger.error("DASHSCOPE_API_KEY is invalid")
    raise ValueError("Invalid DASHSCOPE_API_KEY, please check")

def optimize_prompt(prompt):
    try:
        response = dashscope.Generation.call(
            model='qwen-max',
            prompt=f"Optimize this nail art design prompt for high-quality image generation: {prompt}",
            max_tokens=512,
            temperature=0.7
        )
        if response.status_code == 200 and response.output and response.output.text:
            return response.output.text.strip()
        logger.warning(f"Prompt optimization failed: {response.status_code}")
        return prompt
    except Exception as e:
        logger.error(f"Prompt optimization error: {str(e)}")
        return prompt

def submit_nail_art_task(prompt, negative_prompt):
    """Submit an asynchronous image generation task and return the task ID"""
    try:
        response = ImageSynthesis.async_call(
            model="wanx2.1-t2i-plus",
            prompt=prompt,
            negative_prompt=negative_prompt,
            n=1,
            size="1024*1024"
        )
        if response.status_code == HTTPStatus.OK and response.output and response.output.task_id:
            logger.info(f"Task submitted: {response.output.task_id}")
            return response.output.task_id
        logger.warning(f"Task submission failed: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Task submission error: {str(e)}")
        return None

def get_nail_art_status(task_id):
    """Check the status of the image generation task"""
    try:
        status_response = ImageSynthesis.fetch(task_id)
        if status_response.status_code == HTTPStatus.OK and status_response.output:
            task_status = status_response.output.task_status
            if task_status == 'SUCCEEDED' and status_response.output.results:
                return {
                    'status': 'completed',
                    'image_url': status_response.output.results[0].url
                }
            elif task_status in ['PENDING', 'RUNNING']:
                return {'status': 'running'}
            else:
                return {'status': 'failed'}
        return {'status': 'error'}
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return {'status': 'error'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_design = request.form.get('design', '').strip()
        display_option = request.form.get('display_option', '1')

        if not user_design:
            user_design = "chic nude base with gold foil accents, stiletto nails, glossy finish"

        base_design = (
            "Ultra-high-definition nail art, captured in soft natural light, showcasing intricate details and vibrant textures, "
            "featuring sleek, symmetrical nail shapes, polished surfaces, and trendy, sophisticated decorative elements."
        )

        if display_option == "1":
            display_style = (
                "Extreme close-up of a model's hand, illuminated by professional studio lighting, with crisp details, "
                "flawless symmetrical nails, smooth, radiant skin, and a minimalist, elegant background."
            )
        else:
            display_style = (
                "Nail art arranged on a chic, textured surface, styled in a still-life composition, with a soft, layered background, "
                "diffused lighting to highlight intricate textures and details."
            )

        full_prompt = f"{base_design}, styled as {user_design}, {display_style}"
        negative_prompt = (
            "blurry, pixelated, uneven, rough textures, clashing colors, cluttered designs, "
            "irregular nail shapes, distracting backgrounds, unappealing aesthetics, overexposed, underexposed, "
            "harsh shadows, missing details, flat textures, deformed fingers"
        )

        optimized_prompt = optimize_prompt(full_prompt)
        task_id = submit_nail_art_task(optimized_prompt, negative_prompt)
        if task_id:
            return redirect(url_for('result', task_id=task_id))
        return render_template('index.html', error="Failed to start image generation task.")
    return render_template('index.html')

@app.route('/result/<task_id>')
def result(task_id):
    return render_template('result.html', task_id=task_id)

@app.route('/status/<task_id>')
def status(task_id):
    status = get_nail_art_status(task_id)
    return jsonify(status)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
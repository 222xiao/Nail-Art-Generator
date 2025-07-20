Nail Art Design Generator
项目概述

这是一个基于AI的美甲艺术设计生成器，使用Flask框架和阿里云DashScope API构建。用户可以通过自然语言描述美甲设计概念，系统将自动优化提示词并生成高质量的美甲设计图像。

核心功能

智能设计生成：将用户描述转化为专业级美甲设计
提示词优化：使用Qwen语言模型优化用户输入
两种展示模式：模特手部特写或桌面静物展示
预设模板：提供三种流行美甲风格模板
异步处理：后台高效处理图像生成任务
响应式界面：适配移动设备和桌面浏览器
技术栈

后端：Python Flask
AI服务：阿里云DashScope API
前端：HTML5, CSS3, Bootstrap 5
异步处理：DashScope异步图像生成API
环境管理：python-dotenv
安装指南

前提条件

Python 3.7+
DashScope API密钥（从阿里云控制台获取）
安装步骤

克隆仓库：
bash
git clone https://github.com/yourusername/nail-art-generator.git
cd nail-art-generator
创建虚拟环境：
bash
python -m venv venv
激活虚拟环境：
bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
安装依赖：
bash
pip install -r requirements.txt
创建环境变量文件：
bash
echo "DASHSCOPE_API_KEY=your_api_key_here" > .env
运行应用

bash
python app.py
访问 http://localhost:5001 开始使用

使用说明

在主页表单中描述您想要的美甲设计
选择预设设计模板（可选）
选择展示风格（模特手部特写或桌面静物）
点击"Generate Nail Art"按钮
等待1-3分钟生成过程
查看生成结果并下载图像

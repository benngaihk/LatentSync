import gradio as gr
import os
from pathlib import Path

def process_video(video_path, audio_path, guidance_scale, inference_steps, seed):
    """
    简化版的视频处理函数，用于演示界面
    """
    # 检查文件是否存在
    if not video_path or not os.path.exists(video_path):
        return None, "❌ 请上传有效的视频文件"
    
    if not audio_path or not os.path.exists(audio_path):
        return None, "❌ 请上传有效的音频文件"
    
    # 检查必要的模型文件
    config_path = Path("configs/unet/stage2_512.yaml")
    checkpoint_path = Path("checkpoints/latentsync_unet.pt")
    
    if not config_path.exists():
        return None, f"❌ 缺少配置文件: {config_path}"
    
    if not checkpoint_path.exists():
        return None, f"❌ 缺少模型文件: {checkpoint_path}\n\n请下载模型文件到checkpoints目录"
    
    # 如果文件都存在，尝试运行推理
    try:
        # 这里应该调用实际的推理代码
        # 由于环境限制，目前返回演示信息
        return None, f"""✅ 文件检查完成！
        
📁 输入视频: {os.path.basename(video_path)}
🎵 输入音频: {os.path.basename(audio_path)}
⚙️ 引导尺度: {guidance_scale}
📊 推理步数: {inference_steps}
🎲 随机种子: {seed}

⚠️ 注意：由于Mac环境限制，实际的口型同步功能需要：
1. 下载预训练模型文件
2. 安装完整的依赖包
3. 可能需要GPU支持

请参考README.md进行完整环境配置。"""
        
    except Exception as e:
        return None, f"❌ 处理过程中出现错误: {str(e)}"

def check_environment():
    """检查环境状态"""
    status = []
    
    # 检查配置文件
    config_files = [
        "configs/unet/stage2_512.yaml",
        "configs/unet/stage1.yaml",
    ]
    
    for config_file in config_files:
        if Path(config_file).exists():
            status.append(f"✅ {config_file}")
        else:
            status.append(f"❌ {config_file}")
    
    # 检查模型文件
    model_files = [
        "checkpoints/latentsync_unet.pt",
        "checkpoints/whisper/tiny.pt",
    ]
    
    for model_file in model_files:
        if Path(model_file).exists():
            status.append(f"✅ {model_file}")
        else:
            status.append(f"❌ {model_file}")
    
    # 检查示例文件
    asset_files = [
        "assets/demo1_video.mp4",
        "assets/demo1_audio.wav",
    ]
    
    for asset_file in asset_files:
        if Path(asset_file).exists():
            status.append(f"✅ {asset_file}")
        else:
            status.append(f"❌ {asset_file}")
    
    return "\n".join(status)

# 创建Gradio界面
with gr.Blocks(title="LatentSync Mac Demo", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🎬 LatentSync - 口型同步工具 (Mac版本)
        
        这是LatentSync项目的Mac环境演示版本。请上传您的视频和音频文件进行口型同步处理。
        
        ### 📋 使用说明：
        1. 上传视频文件（包含人脸）
        2. 上传音频文件（目标语音）
        3. 调整参数（可选）
        4. 点击"开始处理"
        
        ### 🔗 相关链接：
        - [GitHub仓库](https://github.com/bytedance/LatentSync)
        - [论文链接](https://arxiv.org/abs/2412.09262)
        """
    )
    
    with gr.Tab("🎥 视频处理"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📤 输入文件")
                video_input = gr.Video(
                    label="上传视频文件 (支持mp4, avi, mov等格式)"
                )
                audio_input = gr.Audio(
                    label="上传音频文件 (支持wav, mp3, aac等格式)", 
                    type="filepath"
                )
                
                gr.Markdown("### ⚙️ 处理参数")
                with gr.Row():
                    guidance_scale = gr.Slider(
                        minimum=1.0,
                        maximum=3.0,
                        value=1.5,
                        step=0.1,
                        label="引导尺度 (数值越高口型同步越准确，但可能产生失真)"
                    )
                    inference_steps = gr.Slider(
                        minimum=10, 
                        maximum=50, 
                        value=20, 
                        step=1, 
                        label="推理步数 (数值越高质量越好，但处理时间越长)"
                    )
                
                seed = gr.Number(
                    value=1247, 
                    label="随机种子 (用于控制生成的随机性)", 
                    precision=0
                )
                
                process_btn = gr.Button(
                    "🚀 开始处理", 
                    variant="primary",
                    size="lg"
                )
                
            with gr.Column(scale=1):
                gr.Markdown("### 📥 输出结果")
                video_output = gr.Video(
                    label="处理后的视频",
                    interactive=False
                )
                
                status_output = gr.Textbox(
                    label="处理状态",
                    lines=10,
                    placeholder="点击开始处理后，这里将显示处理状态...",
                    interactive=False
                )
    
    with gr.Tab("🔧 环境检查"):
        gr.Markdown("### 📋 环境状态检查")
        gr.Markdown("检查LatentSync运行所需的文件和配置：")
        
        check_btn = gr.Button("🔍 检查环境状态", variant="secondary")
        env_status = gr.Textbox(
            label="环境状态",
            lines=15,
            placeholder="点击按钮检查环境状态...",
            interactive=False
        )
        
        check_btn.click(
            fn=check_environment,
            outputs=env_status
        )
    
    with gr.Tab("📖 帮助信息"):
        gr.Markdown("""
        ### 🛠️ 环境配置指南
        
        #### 1. 下载模型文件
        ```bash
        # 使用huggingface-cli下载模型
        pip install huggingface_hub
        huggingface-cli download ByteDance/LatentSync-1.6 latentsync_unet.pt --local-dir checkpoints
        huggingface-cli download ByteDance/LatentSync-1.6 whisper/tiny.pt --local-dir checkpoints
        ```
        
        #### 2. 安装完整依赖
        ```bash
        # 激活虚拟环境
        source latentsync_env/bin/activate
        
        # 安装剩余依赖
        pip install librosa imageio imageio-ffmpeg accelerate einops
        ```
        
        #### 3. 系统要求
        - **推荐显存：** 8GB+ (LatentSync 1.5) 或 18GB+ (LatentSync 1.6)
        - **MacBook M系列：** 需要16GB+内存，性能可能受限
        - **支持格式：** MP4, AVI, MOV (视频), WAV, MP3, AAC (音频)
        
        #### 4. 故障排除
        - 如果遇到依赖问题，请检查Python版本（推荐3.8-3.11）
        - Mac用户可能需要安装额外的媒体编解码器
        - 如果处理缓慢，可以降低推理步数和引导尺度
        
        ### 📞 获取帮助
        - [GitHub Issues](https://github.com/bytedance/LatentSync/issues)
        - [项目文档](https://github.com/bytedance/LatentSync/blob/main/README.md)
        """)
    
    # 绑定事件
    process_btn.click(
        fn=process_video,
        inputs=[
            video_input,
            audio_input,
            guidance_scale,
            inference_steps,
            seed,
        ],
        outputs=[video_output, status_output],
    )

if __name__ == "__main__":
    print("🚀 启动LatentSync Mac演示版...")
    print("📱 应用将在浏览器中自动打开")
    print("🔗 本地地址: http://localhost:7860")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        inbrowser=True,
        share=False
    ) 
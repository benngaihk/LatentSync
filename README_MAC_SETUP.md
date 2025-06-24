# LatentSync Mac环境设置指南

## 🎉 恭喜！环境设置已完成

您的LatentSync Mac演示环境已经成功设置并运行！

## 🚀 当前状态

✅ **Gradio界面已启动**
- 本地地址：http://localhost:7860
- 应用正在后台运行（进程ID: 79516）

✅ **已安装的核心依赖**
- torch 2.7.1
- gradio 5.34.2
- diffusers 0.33.1
- transformers 4.52.4
- opencv-python 4.11.0.86

## 📱 如何使用

1. **打开浏览器访问：http://localhost:7860**
2. **上传文件：**
   - 视频文件：包含人脸的MP4/AVI/MOV文件
   - 音频文件：目标语音的WAV/MP3/AAC文件
3. **调整参数：**
   - 引导尺度：1.0-3.0（推荐1.5）
   - 推理步数：10-50（推荐20）
   - 随机种子：任意数字
4. **点击"开始处理"**

## ⚠️ 重要说明

### 目前的限制
- **模型文件缺失**：需要下载预训练模型才能进行实际的口型同步
- **Mac兼容性**：M系列芯片性能可能受限
- **依赖不完整**：某些依赖包（如mediapipe）在Mac上安装困难

### 下一步操作

如果您想要完整功能，需要：

1. **下载模型文件**：
```bash
# 激活环境
source latentsync_env/bin/activate

# 安装huggingface-cli
pip install huggingface_hub

# 下载模型文件
huggingface-cli download ByteDance/LatentSync-1.6 latentsync_unet.pt --local-dir checkpoints
huggingface-cli download ByteDance/LatentSync-1.6 whisper/tiny.pt --local-dir checkpoints
```

2. **安装剩余依赖**：
```bash
# 尝试安装其他依赖（可能在Mac上有问题）
pip install librosa imageio imageio-ffmpeg accelerate einops
pip install python_speech_features scenedetect ffmpeg-python lpips face-alignment
```

## 🔧 管理应用

### 停止应用
```bash
# 查找进程
ps aux | grep gradio_app_mac.py

# 终止进程（替换79516为实际进程ID）
kill 79516
```

### 重启应用
```bash
cd LatentSync
source latentsync_env/bin/activate
python gradio_app_mac.py
```

## 🆘 故障排除

1. **应用无法访问**：
   - 确认进程是否在运行：`ps aux | grep python`
   - 检查端口：`lsof -i :7860`

2. **上传文件失败**：
   - 检查文件格式和大小
   - 确认文件路径权限

3. **处理失败**：
   - 检查模型文件是否存在
   - 查看终端错误信息

## 📞 获取帮助

- GitHub Issues: https://github.com/bytedance/LatentSync/issues
- 项目文档: https://github.com/bytedance/LatentSync/blob/main/README.md

---

**注意：当前版本主要用于演示和测试界面，完整的口型同步功能需要下载模型文件并可能需要更强的硬件支持。** 
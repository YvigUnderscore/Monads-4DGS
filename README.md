# Monads-4DGS 🌟

A user-friendly interface for processing and training 4D Gaussian Splatting models with automatic Houdini export support! 🎨

## ✨ Features

- 🔧 Complete installation wizard with prerequisites checker
- 📹 Multi-camera video processing
- 🤖 Automated COLMAP integration
- 🎯 Training configuration and monitoring
- 🎬 Direct export to Houdini
- 📊 Real-time progress tracking
- 🎮 User-friendly interface

## 🚀 Getting Started

### Prerequisites

- Windows 10/11
- NVIDIA GPU with CUDA support
- Python 3.7+
- Git
- Visual Studio 2019 with C++ build tools

### 🔑 Installation

1. Clone the repository:
```bash
git clone https://github.com/YvigUnderscore/Monads-4DGS
cd Monads-4DGS
```

2. Install required packages:
```bash
pip install -r requirements.txt.
```

3. Launch the GUI:
```bash
python gaussian_gui.py
```

## 📝 Usage

1. **Installation Tab**
   - Check all prerequisites
   - Install the 4D Gaussian Splatting environment

2. **Video Import**
   - Add your multi-camera videos
   - Configure camera settings
   - Set synchronization parameters

3. **Preprocessing**
   - Configure COLMAP settings
   - Process videos automatically
   - Generate camera poses

4. **Training**
   - Set training parameters
   - Monitor progress in real-time
   - View training statistics

5. **Export**
   - Choose export format (USD, Alembic, BGeo)
   - Set output parameters
   - Direct export to Houdini

## 🛠️ Configuration

Default training parameters:
```yaml
training:
  num_iterations: 30000
  batch_size: 8192
  learning_rate: 0.001
  densification_interval: 500
  opacity_reset_interval: 3000
```

## 📊 Supported Formats

**Input:**
- Videos: MP4, AVI, MOV
- Images: JPG, PNG

**Output:**
- USD
- Alembic
- BGeo

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- https://github.com/fudan-zvg/4d-gaussian-splatting Main repo
- [4D Gaussian Splatting](https://github.com/hustvl/4DGaussians) team
- COLMAP developers
- SideFX Houdini team
- This GUI was partially generated with Claude 3.5 (Sonnet) by Anthropic

## 📚 References

- [4D Gaussian Splatting for Real-Time Dynamic Scene Rendering](https://arxiv.org/abs/2310.08528)
- [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)
- [COLMAP - Structure-from-Motion and Multi-View Stereo](https://colmap.github.io/)
- [Houdini Gaussian Splat Workflow](https://www.sidefx.com/docs/houdini/nodes/sop/gaussiansplatting.html)

## 🔍 Citation

```bibtex
@misc{monads4dgs2024,
    title={Monads-4DGS: A GUI for 4D Gaussian Splatting},
    author={YvigUnderscore},
    year={2024},
    publisher={GitHub},
    howpublished={\url{https://github.com/YvigUnderscore/Monads---4DGS}}
}
```

## 🤖 AI Contribution Notice

This project's code was partially generated using Claude 3.5 (Sonnet) by Anthropic. The AI assisted in creating the GUI structure, implementing core functionalities, and establishing the workflow pipeline. Human oversight and modifications were applied to ensure code quality and functionality.

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub.

---
Made with ❤️ for the Computer Graphics community

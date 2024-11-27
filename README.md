
# Monads-4DGS 🌟

Une interface utilisateur conviviale pour traiter et entraîner des modèles de **4D Gaussian Splatting**, avec export automatique pour Houdini ! 🎨

---

## ✨ Fonctionnalités

- 🔧 Assistant d'installation complet avec vérification des prérequis
- 📹 Traitement multi-caméra pour les vidéos
- 🤖 Intégration automatisée de COLMAP avec support pour caméras multiples
- 🎯 Configuration et suivi de l'entraînement en temps réel
- 🛠️ Génération automatique de `poses_bounds.npy` (**WIP**)
- 🎬 Export direct vers Houdini (**WIP**)
- 📊 Suivi en temps réel de la progression
- 🎮 Interface utilisateur intuitive et facile à utiliser

---

## 🚀 Démarrage

### 🔑 Prérequis

Assurez-vous d'avoir :
- ✅ **Windows 10/11** (avec support CUDA)
- ✅ **NVIDIA GPU** (avec support CUDA 12.1 ou supérieur)
- ✅ **Python 3.10.11**
- ✅ **Git**
- ✅ **Visual Studio 2019/2022** avec outils de build C++

---

### ⚙️ Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/YvigUnderscore/Monads-4DGS
   cd Monads-4DGS
   ```

2. Lancez l'interface graphique :
   ```bash
   python gaussian_gui.py
   ```

---

## 📝 Utilisation

### Étape 0 : **Installation de l'environnement**
- Dans l'onglet **Installation**, lancez l'installation automatique de l'environnement et de toutes ses dépendances.

### Étape 1 : **Vidéos ➡️ Images**
- 📥 Ajoutez vos vidéos multi-caméras dans l'onglet **Import Vidéos**.
- 🔄 Convertissez-les en séquences d'images.

### Étape 2 : **Prétraitement avec COLMAP**
- 🔧 Configurez COLMAP dans l'onglet **Prétraitement**.
  - Sélectionnez la qualité des caractéristiques SIFT (low, medium, high, extreme).
  - Lancez le traitement sparse :
    - Extraction des caractéristiques
    - Matching exhaustif
    - Reconstruction sparse
- 🛠️ Génération automatique de `poses_bounds.npy` (**WIP**).

### Étape 3 : **Entraînement**
- 📋 Configurez les paramètres d'entraînement (itérations, batch size, learning rate).
- 🚀 Lancez l'entraînement et suivez la progression en temps réel.
- 🔗 Basé sur [fudan-zvg/4d-gaussian-splatting](https://github.com/fudan-zvg/4d-gaussian-splatting), avec un fork mis à jour et adapté au projet disponible sur [YvigUnderscore/4d-gaussian-splatting](https://github.com/YvigUnderscore/4d-gaussian-splatting).

### Étape 4 : **Export vers Houdini**
- 🎬 Export direct vers Houdini (**WIP**).

---

## 📊 Formats supportés

### **Entrées :**
- Vidéos : MP4, AVI, MOV
- Images : PNG, JPG

### **Sorties :**
- Formats d'export Houdini : USD, Alembic, BGeo (**WIP**)
- Fichiers intermédiaires : `poses_bounds.npy`, `cameras.txt`, `images.txt`

---

## 📚 Fichiers clés

### **Scripts principaux**
- `4DCAMmaker.py` : Crée le dossier `4DCAM` à partir de vos dossiers caméra (`cam##`).
- `generate_pose_bounds.py` : Génère un fichier `poses_bounds.npy` à partir des résultats de COLMAP (**WIP**).
- `gaussian_gui.py` : Interface utilisateur principale pour contrôler le pipeline.

### **Répertoires**
- **`data/N3V/`** :
  - Contient les images converties et les dossiers caméra (`cam##`).
- **`data/N3V/4DCAM/`** :
  - Regroupe les frames pour la reconstruction sparse.
- **`data/N3V/4DCAM/sparse/`** :
  - Résultats de reconstruction sparse de COLMAP.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- https://github.com/fudan-zvg/4d-gaussian-splatting Main repo
- 4D Gaussian Splatting team
- COLMAP developers
- SideFX Houdini team
- This GUI and readme was partially generated with Claude 3.5 (Sonnet) by Anthropic

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

---

🎨 **Fait avec ❤️ pour la communauté des graphistes et chercheurs !**

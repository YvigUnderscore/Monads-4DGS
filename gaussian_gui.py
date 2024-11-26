import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import subprocess
import os
import sys
import webbrowser
import yaml
import json
from pathlib import Path

class GaussianProcessor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("4D Gaussian Splatting Pipeline")
        self.geometry("800x600")
        
        # Variables globales
        self.project_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        
        # Interface principale
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Création des onglets
        self.tabs = {
            'prerequisites': ttk.Frame(self.notebook),
            'install': ttk.Frame(self.notebook),
            'video_import': ttk.Frame(self.notebook),
            'preprocessing': ttk.Frame(self.notebook),
            'training': ttk.Frame(self.notebook),
            'export': ttk.Frame(self.notebook)
        }
        
        # Ajout des onglets
        self.notebook.add(self.tabs['prerequisites'], text='Prérequis')
        self.notebook.add(self.tabs['install'], text='Installation')
        self.notebook.add(self.tabs['video_import'], text='Import Vidéos')
        self.notebook.add(self.tabs['preprocessing'], text='Prétraitement')
        self.notebook.add(self.tabs['training'], text='Entraînement')
        self.notebook.add(self.tabs['export'], text='Export Houdini')
        
        self.setup_all_tabs()

    def setup_all_tabs(self):
        self.setup_prerequisites_tab()
        self.setup_install_tab()
        self.setup_video_import_tab()
        self.setup_preprocessing_tab()
        self.setup_training_tab()
        self.setup_export_tab()

    def setup_prerequisites_tab(self):
        prerequisites = [
            ("CUDA 11.6", "https://developer.nvidia.com/cuda-11-6-0-download-archive"),
            ("Visual Studio 2019 avec C++", "https://visualstudio.microsoft.com/vs/older-downloads/"),
            ("Git", "https://git-scm.com/downloads"),
            ("Miniconda", "https://docs.conda.io/en/latest/miniconda.html"),
            ("PyTorch 1.13.1", "https://pytorch.org/get-started/locally/")
        ]
        
        for i, (name, url) in enumerate(prerequisites):
            frame = ttk.Frame(self.tabs['prerequisites'])
            frame.pack(fill='x', padx=5, pady=5)
            
            check_var = tk.BooleanVar()
            check = ttk.Checkbutton(frame, text=name, variable=check_var)
            check.pack(side='left')
            
            btn = ttk.Button(frame, text="Télécharger",
                           command=lambda u=url: webbrowser.open(u))
            btn.pack(side='right')

    def setup_install_tab(self):
        frame = self.tabs['install']
        
        # Sélection du dossier d'installation
        dir_frame = ttk.Frame(frame)
        dir_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(dir_frame, text="Dossier d'installation:").pack(side='left')
        ttk.Entry(dir_frame, textvariable=self.project_dir).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(dir_frame, text="Parcourir", 
                  command=lambda: self.project_dir.set(filedialog.askdirectory())).pack(side='right')
        
        # Barre de progression
        self.install_progress = ttk.Progressbar(frame, mode='determinate')
        self.install_progress.pack(fill='x', padx=5, pady=10)
        
        # Bouton d'installation
        ttk.Button(frame, text="Installer l'environnement",
                  command=self.install_environment).pack(pady=5)
        
        self.install_status = ttk.Label(frame, text="")
        self.install_status.pack(pady=5)

    def setup_video_import_tab(self):
        frame = self.tabs['video_import']
        
        # Liste des vidéos
        self.video_listbox = tk.Listbox(frame, height=10)
        self.video_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Ajouter vidéos",
                  command=self.add_videos).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Supprimer sélection",
                  command=self.remove_selected_videos).pack(side='left')
        
        # Configuration des caméras
        cam_frame = ttk.LabelFrame(frame, text="Configuration des caméras")
        cam_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(cam_frame, text="Nombre de caméras:").pack(side='left')
        self.cam_count = ttk.Entry(cam_frame, width=5)
        self.cam_count.pack(side='left', padx=5)
        self.cam_count.insert(0, "20")

    def setup_preprocessing_tab(self):
        frame = self.tabs['preprocessing']
        
        # Configuration COLMAP
        colmap_frame = ttk.LabelFrame(frame, text="Configuration COLMAP")
        colmap_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(colmap_frame, text="Qualité:").pack(side='left')
        self.colmap_quality = ttk.Combobox(colmap_frame, 
                                         values=["low", "medium", "high", "extreme"])
        self.colmap_quality.pack(side='left', padx=5)
        self.colmap_quality.set("medium")
        
        # Barre de progression
        self.preprocess_progress = ttk.Progressbar(frame, mode='determinate')
        self.preprocess_progress.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(frame, text="Lancer le prétraitement",
                  command=self.run_preprocessing).pack(pady=5)
        
        self.preprocess_status = ttk.Label(frame, text="")
        self.preprocess_status.pack(pady=5)

    def setup_training_tab(self):
        frame = self.tabs['training']
        
        # Configuration de l'entraînement
        config_frame = ttk.LabelFrame(frame, text="Configuration")
        config_frame.pack(fill='x', padx=5, pady=5)
        
        params = {
            "Iterations": ("num_iterations", "30000"),
            "Batch Size": ("batch_size", "8192"),
            "Learning Rate": ("learning_rate", "0.001")
        }
        
        self.training_params = {}
        for label, (param, default) in params.items():
            param_frame = ttk.Frame(config_frame)
            param_frame.pack(fill='x', padx=5, pady=2)
            
            ttk.Label(param_frame, text=label + ":").pack(side='left')
            entry = ttk.Entry(param_frame, width=10)
            entry.pack(side='left', padx=5)
            entry.insert(0, default)
            self.training_params[param] = entry
        
        # Barre de progression
        self.training_progress = ttk.Progressbar(frame, mode='determinate')
        self.training_progress.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(frame, text="Lancer l'entraînement",
                  command=self.run_training).pack(pady=5)
        
        self.training_status = ttk.Label(frame, text="")
        self.training_status.pack(pady=5)

    def setup_export_tab(self):
        frame = self.tabs['export']
        
        # Configuration de l'export
        export_frame = ttk.LabelFrame(frame, text="Export Houdini")
        export_frame.pack(fill='x', padx=5, pady=5)
        
        # Sélection du dossier de sortie
        dir_frame = ttk.Frame(export_frame)
        dir_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(dir_frame, text="Dossier de sortie:").pack(side='left')
        ttk.Entry(dir_frame, textvariable=self.output_dir).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(dir_frame, text="Parcourir", 
                  command=lambda: self.output_dir.set(filedialog.askdirectory())).pack(side='right')
        
        # Format d'export
        format_frame = ttk.Frame(export_frame)
        format_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(format_frame, text="Format:").pack(side='left')
        self.export_format = ttk.Combobox(format_frame, 
                                        values=["USD", "Alembic", "BGeo"])
        self.export_format.pack(side='left', padx=5)
        self.export_format.set("USD")
        
        # Barre de progression
        self.export_progress = ttk.Progressbar(frame, mode='determinate')
        self.export_progress.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(frame, text="Exporter",
                  command=self.export_to_houdini).pack(pady=5)
        
        self.export_status = ttk.Label(frame, text="")
        self.export_status.pack(pady=5)

    def install_environment(self):
        if not self.project_dir.get():
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier d'installation")
            return
            
        try:
            commands = [
                f"cd {self.project_dir.get()}",
                "git clone https://github.com/YvigUnderscore/4d-gaussian-splatting",
                "cd 4d-gaussian-splatting",
                "conda env create --file environment.yml",
                "conda activate 4dgs"
            ]
            
            for i, cmd in enumerate(commands):
                self.install_progress['value'] = (i + 1) * 20
                self.install_status['text'] = f"Exécution: {cmd}"
                self.update()
                
                subprocess.run(cmd, shell=True, check=True)
            
            messagebox.showinfo("Succès", "Installation terminée avec succès!")
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'installation: {str(e)}")
            
        finally:
            self.install_status['text'] = ""
            self.install_progress['value'] = 0

    def add_videos(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Vidéos", "*.mp4 *.avi *.mov")])
        for f in files:
            self.video_listbox.insert(tk.END, f)

    def remove_selected_videos(self):
        selection = self.video_listbox.curselection()
        for i in reversed(selection):
            self.video_listbox.delete(i)

    def run_preprocessing(self):
        if self.video_listbox.size() == 0:
            messagebox.showwarning("Attention", "Aucune vidéo sélectionnée")
            return
            
        try:
            # Extraction des frames
            self.preprocess_status['text'] = "Extraction des frames..."
            self.preprocess_progress['value'] = 20
            self.update()
            
            # COLMAP
            self.preprocess_status['text'] = "Traitement COLMAP..."
            self.preprocess_progress['value'] = 60
            self.update()
            
            # Finalisation
            self.preprocess_status['text'] = "Finalisation..."
            self.preprocess_progress['value'] = 100
            self.update()
            
            messagebox.showinfo("Succès", "Prétraitement terminé!")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du prétraitement: {str(e)}")
            
        finally:
            self.preprocess_status['text'] = ""
            self.preprocess_progress['value'] = 0

 

    def run_training(self):
        try:
            # Configuration de l'entraînement selon la doc officielle
            config = {
                'dataset': {
                    'root_dir': self.project_dir.get(),
                    'scene_type': 'dynamic',
                    'fps': 30,
                    'num_frames': self.get_total_frames(),
                    'camera': {
                        'model': 'OPENCV',
                        'width': 1920,
                        'height': 1080
                    }
                },
                'training': {
                    'num_iterations': int(self.training_params['num_iterations'].get()),
                    'batch_size': int(self.training_params['batch_size'].get()),
                    'learning_rate': float(self.training_params['learning_rate'].get()),
                    'densification_interval': 500,
                    'opacity_reset_interval': 3000,
                    'position_lr_init': 0.00016,
                    'position_lr_final': 0.0000016,
                    'position_lr_delay_mult': 0.01,
                    'position_lr_max_steps': 30000,
                    'feature_lr': 0.0025,
                    'opacity_lr': 0.05,
                    'scaling_lr': 0.001,
                    'rotation_lr': 0.001,
                    'percent_dense': 0.01,
                    'densify_from_iter': 500,
                    'densify_until_iter': 15000,
                    'densify_grad_threshold': 0.0002
                }
            }
            
            config_path = os.path.join(self.project_dir.get(), 'config.yaml')
            with open(config_path, 'w') as f:
                yaml.dump(config, f)

            # Préparation de la commande d'entraînement
            train_cmd = [
                "python", "train.py",
                "--source_path", self.project_dir.get(),
                "--model_path", os.path.join(self.project_dir.get(), "output"),
                "--config", config_path,
                "--eval"
            ]

            # Lancement de l'entraînement
            self.training_status['text'] = "Entraînement en cours..."
            
            process = subprocess.Popen(
                train_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Mise à jour de la progression
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # Extraction de la progression depuis la sortie
                    if "Iteration" in output:
                        current_iter = int(output.split()[1])
                        total_iter = int(self.training_params['num_iterations'].get())
                        progress = (current_iter / total_iter) * 100
                        self.training_progress['value'] = progress
                        self.training_status['text'] = f"Iteration {current_iter}/{total_iter}"
                        self.update()

            if process.returncode == 0:
                messagebox.showinfo("Succès", "Entraînement terminé avec succès!")
            else:
                error = process.stderr.read()
                raise Exception(f"Erreur pendant l'entraînement: {error}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'entraînement: {str(e)}")
        
        finally:
            self.training_status['text'] = ""
            self.training_progress['value'] = 0

    def export_to_houdini(self):
        if not self.output_dir.get():
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier de sortie")
            return
            
        try:
            self.export_status['text'] = f"Export en {self.export_format.get()}..."
            self.export_progress['value'] = 25
            self.update()

            # Préparation de la commande d'export
            export_cmd = [
                "python", "export.py",
                "--model_path", os.path.join(self.project_dir.get(), "output"),
                "--format", self.export_format.get().lower(),
                "--output_file", os.path.join(self.output_dir.get(), f"scene.{self.export_format.get().lower()}"),
                "--fps", "30",
                "--frame_start", "0",
                "--frame_end", str(self.get_total_frames() - 1)
            ]

            self.export_progress['value'] = 50
            process = subprocess.run(export_cmd, check=True)
            
            self.export_progress['value'] = 100
            messagebox.showinfo("Succès", f"Export terminé!\nFichier sauvegardé dans: {self.output_dir.get()}")
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")
            
        finally:
            self.export_status['text'] = ""
            self.export_progress['value'] = 0

    def get_total_frames(self):
        """Calcule le nombre total de frames à partir des vidéos sélectionnées"""
        import cv2
        total_frames = 0
        for i in range(self.video_listbox.size()):
            video_path = self.video_listbox.get(i)
            cap = cv2.VideoCapture(video_path)
            total_frames = max(total_frames, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
            cap.release()
        return total_frames

if __name__ == "__main__":
    app = GaussianProcessor()
    app.mainloop()

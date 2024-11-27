import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import subprocess
import os
import yaml
import webbrowser
import logging
class GaussianProcessor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("4D Gaussian Splatting Pipeline")
        self.geometry("800x600")
        
        self.project_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        self.tabs = {
            'prerequisites': ttk.Frame(self.notebook),
            'install': ttk.Frame(self.notebook),
            'video_import': ttk.Frame(self.notebook),
            'preprocessing': ttk.Frame(self.notebook),
            'training': ttk.Frame(self.notebook),
            'export': ttk.Frame(self.notebook)
        }
        
        self.notebook.add(self.tabs['prerequisites'], text='Prérequis')
        self.notebook.add(self.tabs['install'], text='Installation')
        self.notebook.add(self.tabs['video_import'], text='Import Vidéos')
        self.notebook.add(self.tabs['preprocessing'], text='Prétraitement')
        self.notebook.add(self.tabs['training'], text='Entraînement')
        self.notebook.add(self.tabs['export'], text='Export Houdini')
        
        self.setup_all_tabs()

    def convert_videos_to_images(self):
        try:
            if self.video_listbox.size() == 0:
                messagebox.showwarning("Avertissement", "Aucune vidéo ajoutée. Veuillez ajouter des vidéos.")
                return

            output_dir = r"data\N3V"
            if not output_dir:
                return

            # Conversion de chaque vidéo en séquences d'images
            for idx in range(self.video_listbox.size()):
                video_path = self.video_listbox.get(idx)
                video_name = os.path.splitext(os.path.basename(video_path))[0]
                images_output_path = os.path.join(output_dir, video_name)

                if not os.path.exists(images_output_path):
                    os.makedirs(images_output_path)

                # Commande FFmpeg pour extraire les images
                command = [
                    "ffmpeg", "-i", video_path,
                    os.path.join(images_output_path, "%06d.png")
                ]
                subprocess.run(command, check=True)

            messagebox.showinfo("Succès", f"Conversion terminée. Images sauvegardées dans : {output_dir}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur", f"Erreur lors de la conversion : {e}")

    def setup_all_tabs(self):
        self.setup_prerequisites_tab()
        self.setup_install_tab()
        self.setup_video_import_tab()
        self.setup_preprocessing_tab()
        self.setup_training_tab()
        self.setup_export_tab()

    def setup_prerequisites_tab(self):
        prerequisites = [
            ("CUDA 12.1", "https://developer.nvidia.com/cuda-12-1-0-download-archive"),
            ("Visual Studio 2022 avec C++", "https://visualstudio.microsoft.com/vs/"),
            ("Git", "https://git-scm.com/downloads"),
            ("Miniconda", "https://docs.conda.io/en/latest/miniconda.html"),
            ("PyTorch 1.10.11", "https://pytorch.org/get-started/locally/")
        ]
        
        for name, url in prerequisites:
            frame = ttk.Frame(self.tabs['prerequisites'])
            frame.pack(fill='x', padx=5, pady=5)
            
            check_var = tk.BooleanVar()
            ttk.Checkbutton(frame, text=name, variable=check_var).pack(side='left')
            ttk.Button(frame, text="Télécharger", command=lambda u=url: webbrowser.open(u)).pack(side='right')

    def setup_install_tab(self):
        frame = self.tabs['install']
        
        dir_frame = ttk.Frame(frame)
        dir_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(dir_frame, text="Dossier d'installation:").pack(side='left')
        ttk.Entry(dir_frame, textvariable=self.project_dir).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(dir_frame, text="Parcourir", 
                command=lambda: self.project_dir.set(filedialog.askdirectory())).pack(side='right')
        
        self.install_progress = ttk.Progressbar(frame, mode='determinate')
        self.install_progress.pack(fill='x', padx=5, pady=10)
        
        # Bouton pour installer l'environnement
        ttk.Button(frame, text="Installer l'environnement", command=self.install_environment).pack(pady=5)
        
        # Nouveau bouton pour supprimer l'environnement
        ttk.Button(frame, text="Supprimer l'environnement", command=self.remove_environment).pack(pady=5)

        self.install_status = ttk.Label(frame, text="")
        self.install_status.pack(pady=5)

    def remove_environment(self):
        """Supprime l'environnement conda associé."""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer l'environnement?"):
            try:
                commands = [
                    "conda deactivate",
                    "conda env remove -n 4dgs -y"
                ]
                
                for i, cmd in enumerate(commands):
                    self.install_progress['value'] = (i + 1) * 50
                    self.install_status['text'] = f"Exécution: {cmd}"
                    self.update()
                    subprocess.run(cmd, shell=True, check=True)
                    
                messagebox.showinfo("Succès", "Environnement supprimé avec succès!")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")
            finally:
                self.install_status['text'] = ""
                self.install_progress['value'] = 0
    

    def setup_video_import_tab(self):
        frame = self.tabs['video_import']
        
        cameras_frame = ttk.LabelFrame(frame, text="Caméras")
        cameras_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.video_listbox = tk.Listbox(cameras_frame, height=10)
        self.video_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(cameras_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Ajouter caméra", command=self.add_videos).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Supprimer caméra", command=self.remove_selected_videos).pack(side='left')
        ttk.Button(btn_frame, text="Convertir en images", command=self.convert_videos_to_images).pack(side='left')
        
        options_frame = ttk.LabelFrame(frame, text="Options")
        options_frame.pack(fill='x', padx=5, pady=5)
        
        self.images_converted = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame,
                        text="Images déjà converties en PNG",
                        variable=self.images_converted).pack(anchor='w', padx=5, pady=5)
        
        convert_frame = ttk.Frame(frame)
        convert_frame.pack(fill='x', padx=5, pady=5)
        
        self.convert_progress = ttk.Progressbar(frame, mode='determinate')
        self.convert_progress.pack(fill='x', padx=5, pady=5)
        
        self.convert_status = ttk.Label(frame, text="")
        self.convert_status.pack(pady=5)

    def run_colmap(self):
        try:
            # Chemin vers le dossier 4DCAM
            images_dir = "data/N3V/4DCAM"
            
            # Vérification de l'existence du dossier 4DCAM
            if not os.path.exists(images_dir):
                messagebox.showerror(
                    "Erreur", 
                    "Le dossier '4DCAM' est introuvable. Veuillez exécuter '4DCAMmaker.py' pour générer ce dossier avant de continuer."
                )
                return

            if not os.listdir(images_dir):
                messagebox.showerror(
                    "Erreur",
                    "Le dossier '4DCAM' est vide. Veuillez vérifier que des frames ont bien été copiées."
                )
                return

            # Dossier pour les résultats sparse
            sparse_output_path = os.path.join(images_dir, "sparse")
            if not os.path.exists(sparse_output_path):
                os.makedirs(sparse_output_path)

            # Mappage des niveaux de qualité SIFT
            sift_quality_map = {
                "low": "2048",
                "medium": "8192",
                "high": "16384",
                "extreme": "32768"
            }
            sift_max_features = sift_quality_map[self.colmap_quality.get()]

            # Commandes COLMAP
            commands = [
                # Feature extraction avec caméras multiples
                ["colmap", "feature_extractor", 
                "--database_path", os.path.join(images_dir, "database.db"), 
                "--image_path", images_dir,
                "--ImageReader.camera_model", "PINHOLE",
                "--ImageReader.single_camera", "0",  # Caméras multiples
                "--SiftExtraction.max_num_features", sift_max_features],

                # Matching des caractéristiques
                ["colmap", "exhaustive_matcher",
                "--database_path", os.path.join(images_dir, "database.db")],

                # Sparse mapping
                ["colmap", "mapper",
                "--database_path", os.path.join(images_dir, "database.db"), 
                "--image_path", images_dir,
                "--output_path", sparse_output_path],
            ]

            # Exécuter les commandes
            for i, cmd in enumerate(commands):
                subprocess.run(cmd, check=True)
                self.preprocess_progress['value'] = (i + 1) * 33  # Ajuste le progrès
                self.update()

            messagebox.showinfo("Succès", f"COLMAP terminé. Données générées dans : {sparse_output_path}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur", f"Erreur COLMAP : {e}")
        finally:
            self.preprocess_progress['value'] = 0





    def setup_preprocessing_tab(self):
        frame = self.tabs['preprocessing']
        
        colmap_frame = ttk.LabelFrame(frame, text="Configuration COLMAP")
        colmap_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(colmap_frame, text="Qualité:").pack(side='left')
        self.colmap_quality = ttk.Combobox(colmap_frame, values=["low", "medium", "high", "extreme"])
        self.colmap_quality.pack(side='left', padx=5)
        self.colmap_quality.set("medium")
        
        # Bouton pour lancer COLMAP
        ttk.Button(frame, text="Exécuter COLMAP", command=self.run_colmap).pack(pady=5)
        
        self.preprocess_progress = ttk.Progressbar(frame, mode='determinate')
        self.preprocess_progress.pack(fill='x', padx=5, pady=10)
        
        # Bouton pour générer pose_bounds.npy
        ttk.Button(frame, text="Générer pose_bounds.npy", command=self.generate_pose_bounds).pack(pady=5)
        
        self.preprocess_status = ttk.Label(frame, text="")
        self.preprocess_status.pack(pady=5)

    def generate_pose_bounds(self):
        try:
            # Obtenir le nombre de caméras ajoutées
            num_cameras = self.video_listbox.size()
            if num_cameras == 0:
                messagebox.showwarning("Avertissement", "Aucune caméra ajoutée. Veuillez en ajouter avant de continuer.")
                return

            # Chemin de sortie pour le fichier pose_bounds.npy
            output_file = r"data/N3V/poses_bounds.npy"

            if not output_file:
                return

            # Commande pour générer le fichier
            command = [
                "python", "4d-gaussian-splatting/scripts/generate_pose_bounds.py",
                "--num_cameras", str(num_cameras),
                "--output_file", output_file
            ]

            # Exécution de la commande
            subprocess.run(command, check=True)
            messagebox.showinfo("Succès", f"Fichier pose_bounds.npy généré avec succès !\nChemin : {output_file}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {e}")

    def setup_training_tab(self):
        frame = self.tabs['training']
        
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
        
        self.training_progress = ttk.Progressbar(frame, mode='determinate')
        self.training_progress.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(frame, text="Lancer l'entraînement", command=self.run_training).pack(pady=5)
        
        self.training_status = ttk.Label(frame, text="")
        self.training_status.pack(pady=5)

    def setup_export_tab(self):
        frame = self.tabs['export']
        
        export_frame = ttk.LabelFrame(frame, text="Export Houdini")
        export_frame.pack(fill='x', padx=5, pady=5)
        
        dir_frame = ttk.Frame(export_frame)
        dir_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(dir_frame, text="Dossier de sortie:").pack(side='left')
        ttk.Entry(dir_frame, textvariable=self.output_dir).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(dir_frame, text="Parcourir", 
                   command=lambda: self.output_dir.set(filedialog.askdirectory())).pack(side='right')
        
        format_frame = ttk.Frame(export_frame)
        format_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(format_frame, text="Format:").pack(side='left')
        self.export_format = ttk.Combobox(format_frame, values=["USD", "Alembic", "BGeo"])
        self.export_format.pack(side='left', padx=5)
        self.export_format.set("USD")
        
        self.export_progress = ttk.Progressbar(frame, mode='determinate')
        self.export_progress.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(frame, text="Exporter", command=self.export_to_houdini).pack(pady=5)
        
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
        try:
            # Construire la commande
            command = ["python", "4d-gaussian-splatting/scripts/n3v2blender.py", f"data/N3V/"]

            # Exécuter la commande
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            # Afficher la sortie
            print("Output:", result.stdout)
            print("Errors:", result.stderr)
        except subprocess.CalledProcessError as e:
            # Gérer les erreurs d'exécution
            print(f"Une erreur est survenue : {e}")
            print("Message d'erreur :", e.stderr)

    def run_training(self):
        try:
            config = {
                'training': {
                    'num_iterations': int(self.training_params['num_iterations'].get()),
                    'batch_size': int(self.training_params['batch_size'].get()),
                    'learning_rate': float(self.training_params['learning_rate'].get())
                }
            }
            
            config_path = os.path.join(self.project_dir.get(), 'config.yaml')
            with open(config_path, 'w') as f:
                yaml.dump(config, f)

            train_cmd = [
                "python", "train.py",
                "--source_path", self.project_dir.get(),
                "--config", config_path
            ]

            self.training_status['text'] = "Entraînement en cours..."
            
            process = subprocess.Popen(
                train_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output and "Iteration" in output:
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

            export_cmd = [
                "python", "export.py",
                "--model_path", os.path.join(self.project_dir.get(), "output"),
                "--format", self.export_format.get().lower(),
                "--output_file", os.path.join(self.output_dir.get(), f"scene.{self.export_format.get().lower()}")
            ]

            self.export_progress['value'] = 50
            subprocess.run(export_cmd, check=True)
            
            self.export_progress['value'] = 100
            messagebox.showinfo("Succès", f"Export terminé!\nFichier sauvegardé dans: {self.output_dir.get()}")
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")
        finally:
            self.export_status['text'] = ""
            self.export_progress['value'] = 0

if __name__ == "__main__":
    app = GaussianProcessor()
    app.mainloop()

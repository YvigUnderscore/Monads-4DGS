import os
import random
import shutil

def create_4DCAM_folder(base_path):
    """Crée le dossier 4DCAM s'il n'existe pas."""
    output_folder = os.path.join(base_path, "4DCAM")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def get_cam_folders(base_path):
    """Récupère les dossiers cam## dans le répertoire de base."""
    all_items = os.listdir(base_path)
    print(f"Contenu du répertoire {base_path} : {all_items}")  # Diagnostic

    cam_folders = [folder for folder in all_items if folder.lower().startswith("cam") and folder[3:].isdigit()]
    print(f"Dossiers détectés comme cam## : {cam_folders}")  # Diagnostic
    if not cam_folders:
        raise ValueError("Aucun dossier 'cam##' trouvé.")
    return cam_folders

def get_frames_from_folder(folder_path):
    """Récupère toutes les frames dans un dossier donné."""
    frames = [file for file in os.listdir(folder_path) if file.endswith(".png") and file[:-4].isdigit()]
    print(f"Frames trouvées dans {folder_path} : {frames}")  # Diagnostic
    return frames

def main():
    # Base path : répertoire explicite où se trouvent les dossiers cam##
    base_path = "C:/Monads-4DGS/data/N3V"  # Remplace ce chemin si nécessaire
    output_folder = create_4DCAM_folder(base_path)

    # Récupérer les dossiers cam##
    cam_folders = get_cam_folders(base_path)

    # Utiliser le premier dossier pour déterminer le nombre de frames
    first_cam_folder = os.path.join(base_path, cam_folders[0])
    frames = get_frames_from_folder(first_cam_folder)
    if not frames:
        raise ValueError(f"Aucune frame trouvée dans le dossier {cam_folders[0]}.")
    
    num_frames = len(frames)  # Nombre total de frames à copier
    print(f"Nombre de frames dans le premier dossier ({cam_folders[0]}) : {num_frames}")

    # Copier exactement `num_frames` frames dans 4DCAM
    copied_files = set()
    available_cams = cam_folders[:]

    while len(copied_files) < num_frames:
        if not available_cams:
            available_cams = cam_folders[:]

        # Sélectionner une caméra aléatoire
        random_cam = random.choice(available_cams)
        cam_path = os.path.join(base_path, random_cam)
        cam_frames = get_frames_from_folder(cam_path)

        if not cam_frames:
            print(f"Aucune frame trouvée dans {random_cam}, saut de cette caméra.")
            available_cams.remove(random_cam)
            continue

        # Sélectionner une frame aléatoire
        random_frame = random.choice(cam_frames)
        if random_frame in copied_files:
            continue

        source_path = os.path.join(cam_path, random_frame)
        destination_path = os.path.join(output_folder, random_frame)  # Conserve le nom original
        
        shutil.copy(source_path, destination_path)
        copied_files.add(random_frame)
        print(f"Frame copiée : {random_frame} depuis {random_cam} vers 4DCAM.")

    print("Copie terminée avec exactement", len(copied_files), "frames!")

if __name__ == "__main__":
    main()

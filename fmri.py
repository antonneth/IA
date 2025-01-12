import numpy as np
from nilearn.maskers import MultiNiftiMasker
import nilearn.masking 
import nilearn.plotting as p
import os
import gzip
import shutil
import json
import bisect
from glob import glob
from os.path import join, splitext
from bids.grabbids import BIDSLayout
from dateutil.parser import parse
from pathlib import Path
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import OrthogonalMatchingPursuit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import transformers
from transformers import pipeline


# Configuració de les variables
# Defineix les rutes bàsiques per als fitxers i directoris
directori_base = "data/nsddata/ppdata"
subcarpeta_base = "subj"                # Prefix de les subcarpetes
extensio_gz = ".gz"                     # Extensió dels fitxers comprim
desti_base = "data/nsddata/ppdata/"     # Destinació dels fitxers descomprimits
MData = []
# Bucle per descomprimir fitxers i processar dades de subjectes
for i in range(1, 8):  # Recorre els subjectes 01, 02, ..., 07
    indice = f"{i:02}"  # Converteix l'índex a format 2 dígits (ex: '01')
    subcarpeta = f"{subcarpeta_base}{indice}"
    
    # Ruta del fitxer comprimit
    arxiu_gz = os.path.join(directori_base, f"{subcarpeta}/func1mm/{extensio_gz}")
    
    # Comprova si el fitxer existeix
    if os.path.exists(arxiu_gz):
        arxiu_sortida = os.path.join(desti_base, f"{subcarpeta}/func1mm/")
        os.makedirs(os.path.dirname(arxiu_sortida), exist_ok=True)  # Crea el directori si no existeix

        # Descomprimeix el fitxer .gz
        with gzip.open(arxiu_gz, 'rb') as gz_ref:
            with open(arxiu_sortida, 'wb') as sortida:
                shutil.copyfileobj(gz_ref, sortida)
        print(f"Arxiu {arxiu_gz} descomprimit com {arxiu_sortida}")
        MData.append
    else:
        print(f"Arxiu {arxiu_gz} no trobat...")
        

# Configuració del masker per a dades fMRI
# Aplica una màscara per extreure dades rellevants
masker = MultiNiftiMasker(
    mask_img=nilearn.masking.compute_epi_mask("epi_img", lower_cutoff=0.2, upper_cutoff=0.85, connected=True, opening=2, exclude_zeros=False, ensure_finite=True, target_affine=None, target_shape=None, memory=None, verbose=0),  # Exemple de màscara (sustitueix amb la teva màscara real)
    detrend=True,
    standardize="zscore_sample",
    n_jobs=2,
)


# Fitxers preprocessats


# Entrenament del model amb dades NiFti de 212 fotogrames del arxiu .nii
X_train = MData[:212]  
X_test = MData[212:]  

y_train = np.random.rand(212, 211) 
y_test = np.random.rand(212, 211)  

# Entrenament d'un conjunt de classificadors
clfs = []  # Per emmagatzemar els models
for i in range(y_train.shape[1]):  # Itera sobre cada característica de sortida
    clf = Pipeline([
        ("selection", SelectKBest(f_classif, k=500)),  # Selecció de 500 millors característiques
        ("scl", StandardScaler()),  # Escalador estàndard
        ("clf", OrthogonalMatchingPursuit(n_nonzero_coefs=10)),  # Classificador
    ])
    clf.fit(X_train, y_train[:, i])  # Entrena amb la característica i
    clfs.append(clf)

print("Model entrenat correctament!")


# subj_dir *must* have trailing /
subj_dir = '/scratch/tsalo006/dset/sub-01/'
sess = '01'
data_suffix = '.nii.gz'

layout = BIDSLayout(subj_dir)

decoded_features = {
    "object": "null",
    "background": "null",
    "style": "null",
}

def files_to_dict(file_list):
    """Convert list of BIDS Files to dictionary where key is
    acquisition time (datetime.datetime object) and value is
    the File object.
    """
    out_dict = {}
    for f in file_list:
        fn = f.filename
        with open(fn, 'r') as fi:
            data = json.load(fi)
        dt = parse(data['AcquisitionDateTime'])
        out_dict[dt] = f
    return out_dict

# Get json files for field maps
fmap_jsons = layout.get(session=sess, modality='fmap', extensions='json')

# Generador d'imatges amb Stable Diffusion
ResNet18 = pipeline("text-to-image", model="CompVis/stable-diffusion-v1-4")

# Exemple de sortida decodificada de FMRI


# Crear un prompt textual a partir de les dades decodificades
prompt = f"{decoded_features['object']} on {decoded_features['background']} in a {decoded_features['style']} style"

# Generar la imatge
print(f"Generant una imatge amb el prompt: {prompt}")
image = ResNet18(prompt)

# Mostra la imatge generada
image[0].save("generated_image.png")
print("Imatge generada i desada com 'generated_image.png'")
for dir_ in ['AP', 'PA']:
    # mapa de direccions
    dir_jsons = [fm for fm in fmap_jsons if '_dir-{0}_'.format(dir_) in fm.filename]
    fmap_dict = files_to_dict(dir_jsons)
    dts = sorted(fmap_dict.keys())

    intendedfor_dict = {fmap.filename: [] for fmap in dir_jsons}
    
    # BOLD conseguir
    func_jsons = layout.get(session=sess, type='bold', extensions='json') +\
                 layout.get(session=sess, type='dwi', extensions='json')
    func_dict = files_to_dict(func_jsons)
    for func in func_dict.keys():
        fn, _ = splitext(func_dict[func].filename)
        fn += data_suffix
        fn = fn.split(subj_dir)[-1]
        idx = bisect.bisect_right(dts, func) - 1
        fmap_file = fmap_dict[dts[idx]].filename
        intendedfor_dict[fmap_file].append(fn)
         # Suposem que tens dades disponibles 

        fmri__runs_filenames = []  # Llista de fitxers fMRI
        stimuli__runs_filenames = []  # Llista de fitxers d'estímuls
        fmri_data = masker.fit_transform(fmri__runs_filenames)
    for fmap_file in intendedfor_dict.keys():
        with open(fmap_file, 'r') as fi:
            data = json.load(fi)
        if 'IntendedFor' not in data.keys():
            data['IntendedFor'] = intendedfor_dict[fmap_file]
            with open(sess, 'w') as fo:
                json.dump(data, fo)
    decoded_features = {
    "object": data.object,
    "background": data.background,
    "style": data.style,}
    print(decoded_features)




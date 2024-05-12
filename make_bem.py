from os.path import join # TODO -> remove use of join from script before commit
import mne.bem as mne_bem
import mne.source_space as mne_source_space
import matplotlib.pyplot as plt
import matplotlib as mpl
#from mayavi import mlab

SUBJECT_ID = "sub-V1008"
MEG_BASE_PATH = "/home/s8/Documents/VU/dataset/origin"
SUBJECTS_DIR = "/home/s8/Documents/VU/dataset/subjects_dir/freesurfer"
SUBJECT_BEM = f"{SUBJECTS_DIR}/{SUBJECT_ID}/bem"

mne_bem.make_watershed_bem(SUBJECT_ID, SUBJECTS_DIR)

## source space

spacing = 'oct6'    
filename = SUBJECT_ID + '-' + spacing[:3] + '-' + spacing[-1] + '-src.fif'
fullpath = join(SUBJECT_BEM, filename)

src = mne_source_space.setup_source_space(SUBJECT_ID, spacing,
                                          subjects_dir=SUBJECTS_DIR,
                                          n_jobs=-1, surface='white')
mne_source_space.write_source_spaces(fullpath, src)

## bem surfaces
ico = 4
if ico == 3:
    ico_string = '1280'
elif ico == 4:
    ico_string = '5120'
elif ico == 5:
    ico_string = '20484'
filename = SUBJECT_ID + '-' + ico_string + '-bem.fif'
fullpath = join(SUBJECT_BEM, filename)

surfaces = mne_bem.make_bem_model(SUBJECT_ID, ico, conductivity=[0.3],
                                      subjects_dir=SUBJECTS_DIR)
mne_bem.write_bem_surfaces(fullpath, surfaces)
   
## bem solution
filename = SUBJECT_ID + '-' + ico_string + '-bem-sol.fif'
fullpath = join(SUBJECT_BEM, filename)
    
bem = mne_bem.make_bem_solution(surfaces)
mne_bem.write_bem_solution(fullpath, bem)
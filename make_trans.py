import numpy as np
import json
import mne
from mne.coreg import Coregistration
from mne.io import read_raw_ctf

SUBJECT_ID = "sub-V1008"
SUBJECTS_DIR = "/home/s8/Documents/VU/dataset/subjects_dir/freesurfer"
SUBJECT_BEM = f"{SUBJECTS_DIR}/{SUBJECT_ID}/bem"
MEG_DIR = "/home/s8/Documents/VU/dataset/origin"

def map_cm_to_m(list) :
    return [x/100 for x in list]

coordsystem_json_path = f"{MEG_DIR}/{SUBJECT_ID}/meg/{SUBJECT_ID}_coordsystem.json"
meg_raw = f"{MEG_DIR}/{SUBJECT_ID}/meg/{SUBJECT_ID}_task-visual_meg.ds"
trans_path = f"{SUBJECT_BEM}/{SUBJECT_ID}-trans.fif"

info = read_raw_ctf(meg_raw).info
plot_kwargs = dict(
    subject=SUBJECT_ID,
    subjects_dir=SUBJECTS_DIR,
    surfaces="head",
    dig=True,
    eeg=[],
    meg=["sensors", "helmet"],
    show_axes=True,
    coord_frame="meg",
)
view_kwargs = dict(azimuth=45, elevation=90, distance=0.6, focalpoint=(0.0, 0.0, 0.0))

with open(coordsystem_json_path, 'r') as coordsystem_json_file:
    coordsystem = json.load(coordsystem_json_file)['HeadCoilCoordinates']

fiducials = {
    "nasion": map_cm_to_m(coordsystem['nasion']),
    "lpa": map_cm_to_m(coordsystem['left_ear']),
    "rpa": map_cm_to_m(coordsystem['right_ear'])
}

coreg = Coregistration(info, SUBJECT_ID, SUBJECTS_DIR, fiducials=fiducials)
fig = mne.viz.plot_alignment(info, trans=coreg.trans, **plot_kwargs)

coreg.fit_fiducials(verbose=True)
fig = mne.viz.plot_alignment(info, trans=coreg.trans, **plot_kwargs)

coreg.fit_icp(n_iterations=6, nasion_weight=2.0, verbose=True)
fig = mne.viz.plot_alignment(info, trans=coreg.trans, **plot_kwargs)

coreg.fit_icp(n_iterations=20, nasion_weight=10.0, verbose=True)
fig = mne.viz.plot_alignment(info, trans=coreg.trans, **plot_kwargs)
mne.viz.set_3d_view(fig, **view_kwargs)

dists = coreg.compute_dig_mri_distances() * 1e3  # in mm
print(
    f"Distance between HSP and MRI (mean/min/max):\n{np.mean(dists):.2f} mm "
    f"/ {np.min(dists):.2f} mm / {np.max(dists):.2f} mm"
)

print(coreg.trans)
mne.write_trans(trans_path, coreg.trans, overwrite=True)
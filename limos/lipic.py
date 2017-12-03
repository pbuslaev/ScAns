import mdtraj as md
import numpy as np


def lipic(traj_file, top_file, stride):
	traj = md.load_xtc(traj_file, top = top_file, stride = stride)
	traj = traj.superpose(traj[0])
	traj.unitcell_vectors = None
	avg_xyz = traj.xyz.astype(np.float64)
	avg_xyz = avg_xyz.mean(axis = 0, dtype=np.float64)
	avg_traj = md.Trajectory([avg_xyz], traj.top)

	new_traj = md.Trajectory(traj[0].xyz.astype(np.float64) - md.compute_center_of_mass(traj[0]).astype(np.float64), traj[0].top)
	for i in range(1, len(traj)):
		new_traj = new_traj.join(md.Trajectory(traj[i].xyz.astype(np.float64) - md.compute_center_of_mass(traj[i]).astype(np.float64), traj[i].top))
	new_traj = new_traj.superpose(avg_traj)
	new_traj = new_traj.join(avg_traj)
	print(new_traj.xyz.shape)
	return new_traj


def main(traj_file, top_file, stride = 10000):
	traj = lipic(traj_file, top_file, stride)
	traj.save_pdb('lipic.pdb')


if __name__ == '__main__':
	main('concatenated.xtc', 'average.pdb')
	print('algo ends')
	print('oxygen not included')
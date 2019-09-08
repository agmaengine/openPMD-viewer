import os
import numpy as np
import h5py
from opmd_viewer.openpmd_timeseries.data_reader.utilities import get_bpath, join_infile_path
from opmd_viewer.openpmd_timeseries.data_reader.particle_metainfo import ParticleMetaInformation
from opmd_viewer import OpenPMDTimeSeries
import matplotlib.pyplot as plt

picROOT = os.environ['picROOT']
relative_path_to_h5 = '/runs/mySETUP_003/simOutput/h5'
f = h5py.File(picROOT + relative_path_to_h5 + '/simData_0.h5', 'r')
# info = ParticleMetaInformation(f, 'e', ['x', 'ux'])
ts = OpenPMDTimeSeries(join_infile_path(picROOT, relative_path_to_h5))
cell_shape = f['data/0/fields/E/x'].shape
gridSpacing = f['data/0/fields/E'].attrs['gridSpacing']
gridUnitSI = f['data/0/fields/E'].attrs['gridUnitSI']
gridOffset = f['data/0/fields/E'].attrs['gridGlobalOffset']
gridSpacing = gridSpacing * gridUnitSI * 1e6
gridMin = gridOffset * gridUnitSI * 1e6
gridMax = np.array(cell_shape) * gridSpacing

hist_range = [(gridMin[i], gridMax[i]) for i in range(3)]

data, info = ts.get_particle(['x', 'y', 'z', 'w'], 'e')

x, y, z = data[:3]
w = data[3]

position = np.column_stack((x, y, z))
poshist = np.histogramdd(position, (192, 1024, 12), range=hist_range, weights=w)

x, y, z = poshist[1][:3]
# dx = np.array([x[i + 1] - x[i] for i in np.arange(len(x) - 1)])
# dy = np.array([y[i + 1] - y[i] for i in np.arange(len(y) - 1)])
# dz = np.array([z[i + 1] - z[i] for i in np.arange(len(z) - 1)])
#
# dxyz = np.zeros(poshist[0].shape)
# for i in range(dx.size):
#     for j in range(dy.size):
#         for k in range(dz.size):
#             dxyz[i][j][k] = dx[i] * dy[j] * dz[k]

dV = (x[1] - x[0]) * (y[1] - y[0]) * (z[1] - z[0])

density = poshist[0] * 1e18 / dV


def plotdensity_xy(zslice=0):
    plt.imshow(density[:, :, zslice].T, extent=[x.min(), x.max()] + [y.min(), y.max()],
               origin='lower', interpolation='nearest', aspect='auto',
               cmap='Blues', vmin=None, vmax=None)
    plt.colorbar()
    plt.xlabel("$x (\mu m)$")
    plt.ylabel("$y (\mu m)$")
    plt.title("density xy z-slice: %d" % zslice)


def plotdensity_xz(yslice=0):
    plt.imshow(density[:, yslice, :].T, extent=[x.min(), x.max()] + [z.min(), z.max()],
               origin='lower', interpolation='nearest', aspect='auto',
               cmap='Blues', vmin=None, vmax=None)
    plt.colorbar()
    plt.xlabel("$x (\mu m)$")
    plt.ylabel("$z (\mu m)$")
    plt.title("density xz y-slice: %d" % yslice)


def plotdensity_yz(xslice=0):
    plt.imshow(density[xslice, :, :].T, extent=[y.min(), y.max()] + [z.min(), z.max()],
               origin='lower', interpolation='nearest', aspect='auto',
               cmap='Blues', vmin=None, vmax=None)
    plt.colorbar()
    plt.xlabel("$y (\mu m)$")
    plt.ylabel("$z (\mu m)$")
    plt.title("density yz x-slice: %d" % xslice)

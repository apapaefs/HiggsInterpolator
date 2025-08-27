import math, cmath
import string, os, sys, fileinput, pprint, math
import numpy as np
import operator
from scipy.interpolate import interp1d
import collections
import matplotlib.pyplot as plt

#################################################################### 
# FUNCTIONS TO READ/INTERPOLATE THE HIGGS BRS and WIDTHS FROM YR4: #
####################################################################

# function to read in the branching ratios into a dictionary in the format:
# mass [GeV] | H -> bbbar | H -> tautau | H -> mumu | H -> cc | H -> ss | H -> tt | H -> gg | H -> gammagamma | H -> Zgamma | H -> WW | H -> ZZ | total width [GeV]
# see https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR2014#SM_Higgs_Branching_Ratios_and_Pa
def read_higgsBR(brfile):
    higgsbrs = {}
    brstream = open(brfile, 'r')
    brarray = []
    for line in brstream:
        brarray = [ float(line.split()[1]), float(line.split()[2]), float(line.split()[3]), float(line.split()[4]), float(line.split()[5]), float(line.split()[6]), float(line.split()[7]), float(line.split()[8]), float(line.split()[9]), float(line.split()[10]), float(line.split()[11]), float(line.split()[12])]
        higgsbrs[float(line.split()[0])] = brarray
    # sort by increasing value of HYmass
    sorted_x = sorted(higgsbrs.items(), key=operator.itemgetter(0))
    sorted_higgsbrs = collections.OrderedDict(sorted_x)
    return sorted_higgsbrs

# create interpolators for the various BRs and total width and return a dictionary
def interpolate_HiggsBR(brdict):
  # the kind of interpolation
  interpkind = 'cubic'

  # define an array of interpolators
  interp_higgsbrs = []

  # find out how many BRs+width we have:
  values_view = brdict.values()
  value_iterator = iter(values_view)
  first_value = next(value_iterator)
  NBRs = len(first_value)
  
  # push back all the values of the masses, brs and width into arrays
  mass_array = []
  br_array =[[] for yy in range(NBRs)]

  # get the mass and the corresponding BR arrays
  for key in brdict.keys():
      mass_array.append(key)
      for ii in range(NBRs):
        br_array[ii].append(brdict[key][ii])

  # now create the interpolators and put them in the array:
  for ii in range(NBRs):
        interpolator = interp1d(mass_array, br_array[ii], kind=interpkind, bounds_error=False)
        interp_higgsbrs.append(interpolator)

  return interp_higgsbrs

def initialize_HiggsInterpolators(BR_file):
    # BR_file is the file containing the branching ratios for the SM Higgs boson:
    # read the file:
    #print('reading in', BR_file)
    HiggsBRs = read_higgsBR(BR_file)
    # test: print the dictionary
    # first get the interpolated BRs and SM width 
    BR_interpolators_SM = interpolate_HiggsBR(HiggsBRs)  # this returns the actual interpolators
    return BR_interpolators_SM


###################################################################
# END OF FUNCTIONS                                                #
###################################################################

# Get the interpolator:
# MAKE SURE YR4 FILE IS PRESENT!
BR_interpolators_SM = initialize_HiggsInterpolators("higgsBR_YR4.txt")

# EXAMPLE: FUNCTION TO GET Gamma_SM here:
def Gamma_SM_MASS(interpolators_SM, mh):
    # get the corresponding SM width from the interpolator (this should be the last element):
    if mh < 1000.:
        Gamma_SM = interpolators_SM[-1](mh)
    else:
        print('WARNING, mh > 1000 requested, but does not exist in YR4, will use value for mh=1000')
        Gamma_SM = interpolators_SM[-1](1000.)
    return Gamma_SM

# TEST FOR mh=125.09:
mh=125.09
Gamma_SM = Gamma_SM_MASS(BR_interpolators_SM, mh)
print("TESTING: Gamma(mh)=", Gamma_SM)

################
# EXAMPLE PLOT #
################

# plot from mh=20 to mh=1000:
masses = np.arange(20, 1000, 1)
Gammas = [Gamma_SM_MASS(BR_interpolators_SM, mh) for mh in masses] 
    
fig, ax = plt.subplots() # create the elements required for matplotlib. This creates a figure containing a single axes.

# set the labels and titles:
ax.set_xlabel(r'$m_h$ [GeV]', fontsize=15) # set the x label
ax.set_ylabel(r'$\Gamma_\mathrm{SM}(m_h)$ [GeV]', fontsize=15) # set the y label. Note that the 'r' is necessary to remove the need for double slashes. You can use LaTeX! 
ax.set_title('Standard Model-like Higgs boson width', fontsize=15) # set the title 

# make a one-dimensional plot using the above arrays, add a custom label
ax.plot(masses, Gammas)

# log-log plot
ax.set_yscale('log')
ax.set_xscale('log')

# save 
plt.savefig('GammaSM.pdf')
plt.close(fig)




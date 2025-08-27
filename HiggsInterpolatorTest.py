from HiggsInterpolator import *

########################
# TESTING STARTS HERE  #
########################

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

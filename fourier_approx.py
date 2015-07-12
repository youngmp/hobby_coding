"""
Plot data and compute Fourier coefficients

Youngmin Park
yop6@pitt.edu

(Thank you Mario for the help and inspiration)

TODO:
1. Let user choose coefficients up to x% of the L2 norm
"""
try:
    import matplotlib.pylab as mp
    matplotlib_module = True
except ImportError:
    print "You must have matplotlib installed to generate plots"
    matplotlib_module = False
try:
    import numpy as np
    #np.random.seed(0)
    numpy_module = True
except ImportError:
    print "You must have numpy installed to run this script"
    numpy_module = False
try:
    from scipy.optimize import brentq
    scipy_module = True
except ImportError:
    print "You must have numpy installed to run this script"
    scipy_module = False

def manual_ift(bc,freqc,idxc,N):
    """
    manual inverse fourier transform
    bc: nonzero output from np.fft.fft
    ffreqc: corresponding freq. component
    idxc: corresponding index of freq. component
    """
    # define domain
    n = np.linspace(0,N-1,N)
    tot = 0

    c = 0 # counter
    # for select k, compute value at each n
    for k in idxc:
        tot += np.real(bc[c])*np.cos(k*2*np.pi*n/N) - np.imag(bc[c])*np.sin(k*2*np.pi*n/N)
        c += 1
    return tot

def amp_cutoff(x,n,fcoeff):
    # goal: find ideal x s.t. sum(coeff_array_idx) = n
    """
    fcoeff: output from np.fft.fft
    x: cutoff for magnitude of fourier coefficient
    n: desired number of fourier coefficients
    """
    coeff_array_idx = np.absolute(fcoeff) > x
    return sum(coeff_array_idx) - n

def main():
    # load/define data
    #dat = np.loadtxt("hfun.gm_0.32.dat")
    N = 1000
    dat = np.sin(np.linspace(0,10,N))
    dom = np.linspace(0,N,N)

    # get Fourier transform and frequencies
    fcoeff = np.fft.fft(dat)
    ffreq = np.fft.fftfreq(dat.size)
    
    # find cutoff x for desired number of coefficients
    n = 100 # desired # of coefficients
    x = brentq(amp_cutoff,0,np.amax(np.abs(fcoeff)),args=(n,fcoeff))
    # array corresponding to desired coefficients
    coeff_array_idx = np.absolute(fcoeff) > x

    # build list of desired coefficients
    b = fcoeff*coeff_array_idx
    # extract corresponding frequencies
    freq = ffreq*coeff_array_idx   
    
    # build lits of only desired coeff & freq
    bc = fcoeff[coeff_array_idx]/N
    freqc = ffreq[coeff_array_idx]
    idxc = np.nonzero(coeff_array_idx)[0]


    # come back to time domain
    c = np.fft.ifft(b)
    # or
    c2 = manual_ift(bc,freqc,idxc,N)

    if matplotlib_module:
        mp.figure()
        mp.plot(dat)
        mp.plot(c)
        mp.plot(c2)
        mp.show()
    
if __name__ == "__main__":
    main()

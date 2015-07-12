"""
Written by Youngmin Park yop6@pitt.edu

There are no restrictions on the use of this code.

My attempt at creating a general 1-D Langevin function solver.
This program solves the equation:
\begin{equation}
dX = A(X,t)dt + B(X,t) dW(t),
\end{equation}

where $A$ is the right hand side of the scalar function of interest
and $B$ is a constant. The solver uses an iterative method as prescribed
by E&T 2010:

\begin{equation}
x(n+1) = x(n) + h A(X(n),t_n) + B(X(n),t_n) \sqrt{h} \hat N(0,1).
\end{equation}

input functions must take the form
def f(x,t,a,b,c,...):
    return A,B
where a,b,c,... are parameter values and A and B are the functions defined above.

download this file and import as needed, or modify the main() function below.
You must import both langevin and LSolve, but only LSolve is called by the user.
"""

try:
    import matplotlib.pylab as mp
    matplotlib_module = True
except ImportError:
    print "You must have matplotlib installed to generate plots"
    matplotlib_module = False

try:
    import numpy as np
    np.random.seed(0)
    numpy_module = True
except ImportError:
    print "You must have numpy installed to run this script"
    numpy_module = False

def langevin(f,x,t,h,args):
    """
    compute the $n+1$ step of a given langevin equation
    x: value of numerical solution at step n
    f: right hand side function
    sigma: sigma, noise term
    args: arguments (parameters) for rhs as a list or tuple
    """
    #print x,t,args
    
    # if x is a list, f(*x) enters each entry of x into 
    # the function f in order. If there are extra arguments
    # of f, e.g., if an ODE has extra parameters,
    # we append the params to x, then call f(*x). Easy!
    inputs = [x,t]
    for i in range(len(args)):
        inputs.append(args[i])

    return x + h*f(*inputs)[0] + f(*inputs)[1]*np.sqrt(h)*np.random.normal(0,1)

def LSolve(f,x0,t,threshold=None,reset=None,spike_tracking=False,**args):
    """
    solve given SDE (both IF and non-IF)
    inputs are similar to those used in Odeint:
    x: initial condition (can be array or list)
    t: time vector (initial time, final time, steps implicit)
    f: RHS
    args: tuple of arguments (parameters) for RHS of f
    threshold: max membrane potential before reset
    reset: membrane potential reset
    spike_tracking: (for IF models only) if true, return list of length t of 1s and 0s.
    The entries with 1 denote a spike.

    This function assumes the time array is always divided into bins
    of equal length.    
    """
    # generate default args list if empty
    #print args
    if args == {}:
        args = {'args':[]}

    # h
    h = t[1]-t[0]

    # create solution vector
    N = len(t)
    sol = np.zeros((N,1))

    # initial condition
    sol[0] = x0

    if spike_tracking:
        spikes = np.zeros(N)
    
    # solve
    for i in range(1,N):
        #print args['args']
        sol[i] = langevin(f,sol[i-1],t[i-1],h,args['args'])
        if threshold != None and reset != None:
            if sol[i] >= threshold:
                sol[i] = reset
                if spike_tracking:
                    spikes[i] = 1

    if spike_tracking:
        return sol,spikes
    else:
        return sol

def example(x,t,a,b):
    """
    an example right hand side function
    """
    return x*a - t*b,1

def QIF(x,t,I):
    """
    example QIF function
    """
    return x**2 + I,1

def main():
    # an example non-autonomous function
    x0 = 1
    t = np.linspace(1,3,500)

    # use the same syntax as odeint
    sol = LSolve(example,x0,t,args=(1,1))
    
    if matplotlib_module:
        mp.figure(1)
        mp.title("Example solution")
        mp.plot(t,sol)


    # example integrate and fire code
    x0 = 0
    t2 = np.linspace(0,10,500)
    
    # again the syntax is the same as odeint, but we add aditional inputs,
    # including a flag to track spikes (IF models only):
    threshold = 5
    sol2,spikes = LSolve(QIF,x0,t,threshold=threshold,reset=0,spike_tracking=True,args=(5,))

    # extract spike times
    spikes[spikes==0.0] = None
    spikes[spikes==1.0] = threshold

    if matplotlib_module:
        mp.figure(2)
        mp.title("QIF model with noise")
        mp.plot(t2,sol2)
        mp.scatter(t2,spikes,color='red',facecolor='red')
        mp.show()
    
if __name__ == "__main__":
    main()

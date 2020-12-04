import numpy as np

E = 2.718281828459045

class LineSearch():
    def __init__(self):
        LineSearch.bisection(dfun,theta,args=[],d,low=1,high=10)

    @staticmethod
    def bisection(dfun,theta,args,d,low,high,maxiter=1e4):
        """
        # Functionality:find the root of the function(fun) in the interval [low,high]
        # @Parameters
        # dfun : compute the graident of function f(x)
        # theta : Parameters of the model
        # args : other variables needed to compute the value of dfun
        # [low,high] : the interval which contains the root
        # maxiter : the max number of iterations
        """
        eps = 1e-6
        val_low = np.sum(dfun(theta+low*d,args)*d.T)
        val_high = np.sum(dfun(theta+high*d,args)*d.T)
        if val_low*val_high>0:
            raise Exception('Invalid interval!')

        iter_num=1
        while iter_num < maxiter:
            mid = (low+high)/2
            val_mid = np.sum(dfun(theta+mid*d,args)*d.T)
            if abs(val_mid) < eps or abs(high-low) < eps:
                return mid
            elif val_mid * val_low > 0:
                low = mid
            else:
                high = mid
            iter_num += 1

    def ArmijoBacktrack(fun,dfun,theta,args,d,stepsize=1,tau=0.5,c1=1e-3):
        """
        # Functionality:find an acceptable stepsize via backtrack under Armijo rule
        # @Parameters
        # fun:compute the value of objective function
        # dfun:compute the gradient of objective function
        # theta:a vector of parameters of the model
        # stepsize:initial step size
        # c1:sufficient decrease Parameters
        # tau:rate of shrink of stepsize
        """
        slope = np.sum(dfun(theta,args)*d.T)
        obj_old = costFunction(theta,args)
        theta_new = theta+stepsize*d
        obj_new = costFunction(theta_new,args)
        while obj_new > obj_old + c1*stepsize*slope:
            stepsize *= tau
            theta_new = theta + stepsize*d
            obj_new = costFunction(theta_new,args)
        return stepsize

if __name__ == '__main__':
    pass

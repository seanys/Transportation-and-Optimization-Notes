# reference/source：
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

E = 2.718281828459045

def funTest(x,args=np.array([])):
    return pow(E,x) - 2*x

def dfunTest(x,args=np.array([])):
    return pow(E,x) - 2

def quadraticInterpolation(a,h,h0,g0):
    numerator=g0*a**2
    denominator=2*(g0*a+h0-h)
    if abs(denominator)<1e-12:#indicates that a is almost 0
        return a
    return numerator/denominator

def cubicInterpolation(a0,h0,a1,h1,h,g):
    mat=matlib.matrix([[a0**2,-a1**2],[-a0**3,a1**3]])
    vec=matlib.matrix([[h1-h-g*a1],[h0-h-g*a0]])
    ab=mat*vec/(a0**2*a1**2*(a1-a0))
    a=ab[0,0]
    b=ab[1,0]
    if abs(a)<1e-12:#a=0 and cubic function is a quadratic one
        return -g/(2*b)
    return (-b+np.sqrt(b**2-3*a*g))/(3*a)

def cubicInterpolationHermite(a0,h0,g0,a1,h1,g1):
    d1=g0+g1-3*(h1-h0)/(a1-a0)
    d2=np.sign(a1-a0)*np.sqrt(d1**2-g0*g1)
    res=a1-(a1-a0)*(g1+d2-d2)/(g1-g0+2*d2)
    return res

def zoom(fun,dfun,theta,args,d,a_low,a_high,c1=1e-3,c2=0.9,max_iter=1e4):
    if a_low>a_high:
        print('low:%f,high:%f'%(a_low,a_high))
        raise Exception('Invalid interval of stepsize in zoom procedure')
    eps=1e-16
    h=fun(theta,args) #h(0)=f(x)
    g=np.sum(dfun(theta,args)*d.T) #h'(0)=f'(x)^Td
    k=0
    h_low=fun(theta+a_low*d,args)
    h_high=fun(theta+a_high*d,args)
    if h_low>h+c1*a_low*g:
        raise Exception('Left endpoint violates Armijo condition in zoom procedure')
    while k<max_iter and abs(a_high-a_low)>=eps:
        a_new=(a_low+a_high)/2
        h_new=fun(theta+a_new*d,args)
        if h_new>h+c1*a_new*g or h_new>h_low:
            a_high=a_new
            h_high=h_new
        else:
            g_new=np.sum(dfun(theta+a_new*d,args)*d.T)
            if abs(g_new)<=-c2*g: #satisfy Wolfe condition
                return a_new
            if g_new*(a_high-a_low)>=0:
                a_high=a_new
                h_high=h_new
            else:
                a_low=a_new
                h_low=h_new
        k+=1
    return a_low #a_low definitely satisfy Armijo condition

class LineSearch():
    @staticmethod
    def graidentDescent(fun,dfun,theta,_type="ArmijoBackTrack",show=False,maxiter=10,):
        x,y,y_ = [theta[0]],[fun(theta)[0]],[dfun(theta)[0]]
        i = 0
        eps = 1e-6
        while i < maxiter:
            last_theta = deepcopy(theta)
            d = -dfun(theta)
            if _type == "WolfLineSearch":
                stepsize = LineSearch.WolfeLineSearch(fun,dfun,theta,d)
            elif _type == "ArmijoBackTrack":
                stepsize = LineSearch.ArmijoBacktrack(fun,dfun,theta,d)
            elif _type == "ArmijoLineSearch":
                stepsize = LineSearch.ArmijoLineSearch(fun,dfun,theta,d)
            else:
                stepsize = LineSearch.WolfeLineSearch(fun,dfun,theta,d)
            # print("d,stepsize,theta:",d,stepsize,theta)
            if abs(d) < eps or abs(stepsize)==0: break
            theta = last_theta + stepsize*d
            if theta > 1: theta = np.array([1])
            if theta < 0: theta = np.array([0])
            i = i + 1
            x.append(theta[0]),y.append(fun(theta)[0]),y_.append(dfun(theta)[0])
        
        # print(x)
        # print(y)
        # print(y_)

        # print("Final x:%0.6f" % theta)
        # print("Final y:%0.6f" % fun(theta))
        # print("Final y':%0.6f" % dfun(theta))
        # print("Iteration Times':%s" % i)

        if show==True:
            plt.subplot(1,2,1)
            plot_X = np.linspace(-10, 3, 256, endpoint=True)
            plt.plot(plot_X,fun(plot_X))
            plt.subplot(1,2,2)
            plt.plot(np.array(x),np.array(y))
            plt.show()

        return {"x":theta[0], "y":fun(theta)[0], "y_":dfun(theta)[0], "times": i}

    @staticmethod
    def ArmijoBacktrack(fun,dfun,theta,d,args=np.array([]),stepsize=1,tau=0.5,c1=1e-3):
        slope = np.sum(dfun(theta,args)*d.T)
        obj_old = fun(theta,args)
        theta_new = theta + stepsize*d
        obj_new = fun(theta_new,args)
        while obj_new > obj_old + c1*stepsize*slope:
            stepsize *= tau
            theta_new = theta + stepsize*d
            obj_new = fun(theta_new,args)
        return stepsize

    @staticmethod
    def ArmijoLineSearch(fun,dfun,theta,d,args=np.array([]),a0=1,c1=1e-3,a_min=1e-7,max_iter=1e5):
        eps=1e-6
        c1=min(c1,0.5) #c1 should<=0.5
        a_pre=h_pre=g_pre=0
        a_cur=a0
        f_val=fun(theta,args) #h(0)=f(0)
        g_val=np.sum(dfun(theta,args)*d.T) #h'(0)=f'(x)^Td
        h_cur=g_cur=0
        k=0
        while a_cur>a_min and k<max_iter:
            h_cur=fun(theta+a_cur*d,args)
            g_cur=np.sum(dfun(theta+a_cur*d,args)*d.T)
            if h_cur<=f_val+c1*a_cur*g_val: #meet Armijo condition
                return a_cur
            if not k: #k=0,use quadratic interpolation
                a_new=quadraticInterpolation(a_cur,h_cur,f_val,g_val)
            else: #k>0,use cubic Hermite interpolation
                a_new=cubicInterpolationHermite(a_pre,h_pre,g_pre,a_cur,h_cur,g_cur)
            if abs(a_new-a_cur)<eps or abs(a_new)<eps: #safeguard procedure
                a_new=a_cur/2
            a_pre=a_cur
            a_cur=a_new
            h_pre=h_cur
            g_pre=g_cur
            k+=1
        return a_min #failed search

    @staticmethod
    def WolfeLineSearch(fun,dfun,theta,d,args=np.array([]),a0=1,c1=1e-4,c2=0.9,a_min=1e-7,max_iter=1e5):
        eps=1e-16
        c1=min(c1,0.5)
        a_pre=0
        a_cur=a0
        f_val=fun(theta,args) #h(0)=f(x)
        g_val=np.sum(dfun(theta,args)*d.T)
        h_pre=f_val #h'(0)=f'(x)^Td
        k=0
        while k<max_iter and abs(a_cur-a_pre)>=eps:
            h_cur=fun(theta+a_cur*d,args) #f(x+ad)
            if h_cur>f_val+c1*a_cur*g_val or h_cur>=h_pre and k>0:
                return zoom(fun,dfun,theta,args,d,a_pre,a_cur,c1,c2)
            g_cur=np.sum(dfun(theta+a_cur*d,args)*d.T)
            if abs(g_cur)<=-c2*g_val:#satisfy Wolfe condition
                return a_cur
            if g_cur>=0:
                return zoom(fun,dfun,theta,args,d,a_pre,a_cur,c1,c2)
            a_new=quadraticInterpolation(a_cur,h_cur,f_val,g_val)
            a_pre=a_cur
            a_cur=a_new
            h_pre=h_cur
            k+=1
        return a_min


class Newton(object):
    @staticmethod
    def BFGS(fun,dfun,theta,args,H=None,mode=0,eps=1e-12,max_iter=1e4):
        x_pre=x_cur=theta
        g=dfun(x_cur,args)
        I=matlib.eye(theta.size)
        if not H:#initialize H as an identity matrix
            H=I
        k=0
        while k<max_iter and np.sum(np.abs(g))>eps:
            d=-g*H
            step=LineSearch(fun,dfun,x_pre,args,d,1,mode)
            x_cur=x_pre+step*d
            s=step*d
            y=dfun(x_cur,args)-dfun(x_pre,args)
            ys=np.sum(y*s.T)
            if abs(ys)<eps:
                return x_cur
            change=(ys+np.sum(y*H*y.T))*(s.T*s)/(ys**2)-(H*y.T*s+s.T*y*H)/ys
            H+=change
            g=dfun(x_cur,args)
            x_pre=x_cur
            k+=1
        return x_cur

    @staticmethod
    def LBFGS(fun,dfun,theta,args,mode=0,eps=1e-12,max_iter=1e4):
        x_pre=x_cur=theta
        s_arr=[]
        y_arr=[]
        Hscale=1
        k=0
        while k<max_iter:
            g=dfun(x_cur,args)
            d=LBFGSSearchDirection(y_arr,s_arr,Hscale,-g)
            step=LineSearch(fun,dfun,x_pre,args,d,1,mode)
            s=step*d
            x_cur=x_pre+s
            y=dfun(x_cur,args)-dfun(x_pre,args)
            ys=np.sum(y*s.T)
            if np.sum(np.abs(s))<eps:
                return x_cur
            x_pre=x_cur
            k+=1
            y_arr,s_arr,Hscale=LBFGSUpdate(y,s,y_arr,s_arr)
        return x_cur

    @staticmethod
    def LBFGSSearchDirection(y_arr,s_arr,Hscale,g):
        histNum=len(s_arr)#number of update data stored
        if not histNum:
            return g
        dim=s_arr[0].size
        a_arr=[0 for i in range(histNum)]
        rho=[0 for i in range(histNum)]
        q=g
        for i in range(1,histNum+1):
            s=s_arr[histNum-i]
            y=y_arr[histNum-i]
            rho[histNum-i]=1/np.sum(s*y.T)
            a_arr[i-1]=rho[histNum-i]*np.sum(s*q.T)
            q-=(a_arr[i-1]*y)
        P=Hscale*q
        for i in range(histNum,0,-1):
            y=y_arr[histNum-i]
            s=s_arr[histNum-i]
            beta=rho[histNum-i]*np.sum(y*P.T)
            P+=s*(a_arr[i-1]-beta)
        return P

    @staticmethod
    def LBFGSUpdate(y,s,oldy,olds,m=1e2):
        eps=1e-12
        Hscale=np.sum(y*s.T/y*y.T) #a scale to initialize H_{k-m}
        if Hscale<eps:#skip update
            return oldy,olds,Hscale

        cur_m=len(oldy)
        if cur_m>=m:
            oldy.pop(0)
            olds.pop(0)
        oldy.append(copy.deepcopy(y))
        olds.append(copy.deepcopy(s))
        return oldy,olds,Hscale

if __name__ == '__main__':
    LineSearch.graidentDescent(fun=funTest,dfun=dfunTest,theta=np.array([-5]))


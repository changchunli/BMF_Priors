'''
This file contains the updates for the variables, where we draw new values for
tau, U, V, etc.

Updates for U, V - format (Likelihood) Prior:
- (Gaussian) Gaussian
- (Gaussian) Gaussian + Wishart
- (Gaussian) Gaussian + Automatic Relevance Determination
- (Gaussian) Gaussian + Volume Prior
- (Gaussian) Exponential
- (Gaussian) Exponential + ARD
- (Gaussian) Truncated Normal
- (Gaussian) Truncated Normal + hierarchical
- (Gaussian) Half Normal
- (Poisson)  Gamma
- (Poisson)  Gamma + hierarchical
- (Poisson)  Dirichlet

Other updates:
- tau (noise) from Gamma [model: all with Gaussian likelihood]
- mu, Sigma from Normal - Inverse Wishart [model: Gaussian + Wishart]
- lambdak from Automatic Relevance Determination [model: Gaussian + Automatic Relevance Determination]
- lambdak Automatic Relevance Determination [model: Exponential + Automatic Relevance Determination]
- mu, tau from hierarchical Truncated Normal [model: Truncated Normal + hierarchical]
- zij from Multinomial [model: all with Poisson likelihood]
- hi from hierarchical Gamma [model: Gamma + hierarchical]
'''

from parameters import gaussian_tau_alpha_beta
from parameters import gaussian_gaussian_mu_sigma
from parameters import gaussian_gaussian_wishart_mu_sigma
from parameters import gaussian_wishart_beta0_v0_mu0_W0
from parameters import gaussian_gaussian_ard_mu_sigma
from parameters import gaussian_ard_alpha_beta
from parameters import gaussian_gaussian_vp_mu_sigma
from parameters import gaussian_exponential_mu_tau
from parameters import gaussian_exponential_ard_mu_tau
from parameters import exponential_ard_alpha_beta
from parameters import gaussian_tn_mu_tau
from parameters import gaussian_tn_hierarchical_mu_tau
from parameters import tn_hierarchical_mu_m_t
from parameters import tn_hierarchical_tau_a_b
from parameters import gaussian_hn_mu_tau
from parameters import poisson_Zij_n_p
from parameters import poisson_gamma_a_b
from parameters import poisson_gamma_hierarchical_a_b
from parameters import gamma_hierarchical_hUi_a_b
from parameters import poisson_dirichlet_alpha

from distributions.gamma import gamma_draw
from distributions.multivariate_normal import multivariate_normal_draw
from distributions.normal_inverse_wishart import normal_inverse_wishart_draw
from distributions.normal import normal_draw
from distributions.truncated_normal_vector import truncated_normal_vector_draw
from distributions.multinomial import multinomial_draw
from distributions.dirichlet import dirichlet_draw

import itertools
import numpy


''' General Gaussian and Poisson models '''
def update_tau_gaussian(alpha, beta, R, M, U, V):
    """ Update tau (noise) in Gaussian models. """
    alpha_s, beta_s = gaussian_tau_alpha_beta(alpha, beta, R, M, U, V)
    new_tau = gamma_draw(alpha=alpha_s, beta=beta_s)
    return new_tau

def update_Z_poisson(R, M, U, V):
    """ Update Z in Poisson models. """
    I, J, K = M.shape[0], M.shape[1], U.shape[1]
    assert R.shape == M.shape and R.shape[0] == U.shape[0] and R.shape[1] == V.shape[0]
    new_Z = numpy.zeros((I, J, K))
    for i,j in itertools.product(range(I),range(J)):
        if M[i,j]:
            n_ij, p_ij = poisson_Zij_n_p(Rij=R[i,j], Ui=U[i,:], Vj=V[j,:])
            new_Z[i,j,:] = multinomial_draw(n=n_ij, p=p_ij)
    return new_Z
    

''' (Gausian) Gaussian '''
def update_U_gaussian_gaussian(lamb, R, M, V, tau):
    """ Update U for All Gaussian model. """
    I, K = R.shape[0], V.shape[1]
    assert R.shape == M.shape and R.shape[1] == V.shape[0]
    U = numpy.zeros((I,K))
    for i in range(I):
        muUi, sigmaUi = gaussian_gaussian_mu_sigma(lamb=lamb, Ri=R[i], Mi=M[i], V=V, tau=tau)
        U[i,:] = multivariate_normal_draw(mu=muUi, sigma=sigmaUi)
    return U

def update_V_gaussian_gaussian(lamb, R, M, U, tau):  
    """ Update V for All Gaussian model. """
    return update_U_gaussian_gaussian(lamb=lamb, R=R.T, M=M.T, V=U, tau=tau)


''' (Gausian) Gaussian + Wishart '''
def update_U_gaussian_gaussian_wishart(muU, sigmaU_inv, R, M, V, tau):
    """ Update U for All Gaussian + Wishart model. """
    I, K = R.shape[0], V.shape[1]
    assert R.shape == M.shape and R.shape[1] == V.shape[0]
    U = numpy.zeros((I,K))
    for i in range(I):
        muUi, sigmaUi = gaussian_gaussian_wishart_mu_sigma(
            muU=muU, sigmaU_inv=sigmaU_inv, Ri=R[i], Mi=M[i], V=V, tau=tau)
        U[i,:] = multivariate_normal_draw(mu=muUi, sigma=sigmaUi)
    return U

def update_V_gaussian_gaussian_wishart(muV, sigmaV_inv, R, M, U, tau):  
    """ Update V for All Gaussian + Wishart model. """
    return update_U_gaussian_gaussian_wishart(
        muU=muV, sigmaU_inv=sigmaV_inv, R=R.T, M=M.T, V=U, tau=tau)

def update_muU_sigmaU_gaussian_gaussian_wishart(beta0, v0, mu0, W0_inv, U):
    """ Update muU and sigmaU for All Gaussian + Wishart model. """
    beta0_s, v0_s, mu0_s, W0_s = gaussian_wishart_beta0_v0_mu0_W0(
        beta0=beta0, v0=v0, mu0=mu0, W0_inv=W0_inv, U=U)
    new_muU, new_sigmaU = normal_inverse_wishart_draw(mu0=mu0_s,beta0=beta0_s,v0=v0_s,W0=W0_s)
    return (new_muU, new_sigmaU)

def update_muV_sigmaV_gaussian_gaussian_wishart(beta0, v0, mu0, W0_inv, V):
    """ Update muV and sigmaV for All Gaussian + Wishart model. """
    return update_muU_sigmaU_gaussian_gaussian_wishart(
        beta0=beta0, v0=v0, mu0=mu0, W0_inv=W0_inv, U=V)
    

''' (Gausian) Gaussian + Automatic Relevance Determination '''
def update_U_gaussian_gaussian_ard(lamb, R, M, V, tau):
    """ Update U for All Gaussian + ARD model. """
    I, K = R.shape[0], V.shape[1]
    assert R.shape == M.shape and R.shape[1] == V.shape[0]
    U = numpy.zeros((I,K))
    for i in range(I):
        muUi, sigmaUi = gaussian_gaussian_ard_mu_sigma(
            lamb=lamb, Ri=R[i], Mi=M[i], V=V, tau=tau)
        U[i,:] = multivariate_normal_draw(mu=muUi, sigma=sigmaUi)
    return U
    
def update_V_gaussian_gaussian_ard(lamb, R, M, U, tau):
    """ Update V for All Gaussian + ARD model. """
    return update_U_gaussian_gaussian_ard(lamb=lamb, R=R.T, M=M.T, V=U, tau=tau)

def update_lambda_gaussian_gaussian_ard(alpha0, beta0, U, V):
    """ Update lambda (vector) for All Gaussian + ARD model. """
    K = U.shape[1]
    new_lambda = numpy.zeros(K)
    for k in range(K):
        alpha_s, beta_s = gaussian_ard_alpha_beta(
            alpha0=alpha0, beta0=beta0, Uk=U[:,k], Vk=V[:,k])
        new_lambda[k] = gamma_draw(alpha=alpha_s, beta=beta_s)
    return new_lambda


''' (Gausian) Gaussian + Volume Prior '''
def update_U_gaussian_gaussian_vp(gamma, R, M, U, V, tau):
    """ Update U for All Gaussian + VP model. """
    I, K = U.shape
    assert R.shape == M.shape and R.shape[0] == U.shape[0] and R.shape[1] == V.shape[0]
    for i,k in itertools.product(range(I),range(K)):
        muUik, tauUik = gaussian_gaussian_vp_mu_sigma(
            i=i, k=k, gamma=gamma, Ri=R[i,:], Mi=M[i,:], U=U, V=V, tau=tau)
        U[i,k] = normal_draw(mu=muUik, tau=tauUik)
    return U
    
def update_V_gaussian_gaussian_vp(gamma, R, M, U, V, tau):
    """ Update V for All Gaussian + VP model. """
    return update_U_gaussian_gaussian_vp(gamma=gamma, R=R.T, M=M.T, U=V, V=U, tau=tau)


''' (Gausian) Exponential '''
def update_U_gaussian_exponential(lamb, R, M, U, V, tau):
    """ Update U for Gaussian + Exponential model. """
    I, K = U.shape
    assert R.shape == M.shape and R.shape[0] == U.shape[0] and R.shape[1] == V.shape[0]
    for k in range(K):
        muUk, tauUk = gaussian_exponential_mu_tau(k=k, lamb=lamb, R=R, M=M, U=U, V=V, tau=tau)
        U[:,k] = truncated_normal_vector_draw(mus=muUk, taus=tauUk)
    return U
    
def update_V_gaussian_exponential(lamb, R, M, U, V, tau):
    """ Update V for Gaussian + Exponential model. """
    return update_U_gaussian_exponential(lamb=lamb, R=R.T, M=M.T, U=V, V=U, tau=tau)
    

''' (Gausian) Exponential + Automatic Relevance Determination '''
def update_U_gaussian_exponential_ard(lamb, R, M, U, V, tau):
    """ Update U for Gaussian + Exponential + ARD model. """
    I, K = U.shape
    assert R.shape == M.shape and R.shape[0] == U.shape[0] and R.shape[1] == V.shape[0]
    for k in range(K):
        muUk, tauUk = gaussian_exponential_ard_mu_tau(k=k, lambdak=lamb[k], R=R, M=M, U=U, V=V, tau=tau)
        U[:,k] = truncated_normal_vector_draw(mus=muUk, taus=tauUk)
    return U
    
def update_V_gaussian_exponential_ard(lamb, R, M, U, V, tau):
    """ Update V for Gaussian + Exponential + ARD model. """
    return update_U_gaussian_exponential_ard(lamb=lamb, R=R.T, M=M.T, U=V, V=U, tau=tau)
    
def update_lambda_gaussian_exponential_ard(alpha0, beta0, U, V):
    """ Update lambda (vector) for Gaussian + Exponential + ARD model. """
    K = U.shape[1]
    new_lambda = numpy.zeros(K)
    for k in range(K):
        alpha_s, beta_s = exponential_ard_alpha_beta(
            alpha0=alpha0, beta0=beta0, Uk=U[:,k], Vk=V[:,k])
        new_lambda[k] = gamma_draw(alpha=alpha_s, beta=beta_s)
    return new_lambda
    

''' (Gausian) Truncated Normal '''
def update_U_gaussian_tn(muU, tauU, R, M, U, V, tau):
    """ Update U for Gaussian + Truncated Normal model. """
    I, K = U.shape
    assert R.shape == M.shape and R.shape[0] == U.shape[0] and R.shape[1] == V.shape[0]
    for k in range(K):
        muUk_s, tauUk_s = gaussian_tn_mu_tau(
            k=k, muU=muU, tauU=tauU, R=R, M=M, U=U, V=V, tau=tau)
        U[:,k] = truncated_normal_vector_draw(mus=muUk_s, taus=tauUk_s)
    return U
    
def update_V_gaussian_tn(muU, tauU, R, M, U, V, tau):
    """ Update V for Gaussian + Truncated Normal model. """
    return update_U_gaussian_tn(muU=muU, tauU=tauU, R=R.T, M=M.T, U=V, V=U, tau=tau)


''' (Gausian) Truncated Normal + hierarchical '''
def update_U_gaussian_tn_hierarchical(muUk, tauUk, R, M, U, V, tau):
    """ Update U for Gaussian + Truncated Normal + hierarchical model. """
    I, K = U.shape
    assert R.shape == M.shape and R.shape[0] == U.shape[0] and R.shape[1] == V.shape[0]
    for k in range(K):
        muUk_s, tauUk_s = gaussian_tn_hierarchical_mu_tau(
            k=k, muUk=muUk, tauUk=tauUk, R=R, M=M, U=U, V=V, tau=tau)
        U[:,k] = truncated_normal_vector_draw(mus=muUk_s, taus=tauUk_s)
    return U
    
def update_V_gaussian_tn_hierarchical(muUk, tauUk, R, M, U, V, tau):
    """ Update V for Gaussian + Truncated Normal + hierarchical model. """
    return update_U_gaussian_tn_hierarchical(
        muUk=muUk, tauUk=tauUk, R=R.T, M=M.T, U=V, V=U, tau=tau)
    
def update_muU_gaussian_tn_hierarchical(mu_mu, tau_mu, U, muU, tauU):
    """ Update muU (matrix) for Gaussian + Truncated Normal + hierarchical model. """
    I, K = U.shape
    assert U.shape == muU.shape and U.shape == tauU.shape
    (m_mu, t_mu) = tn_hierarchical_mu_m_t(mu_mu=mu_mu, tau_mu=tau_mu, U=U, muU=muU, tauU=tauU)
    new_muU = numpy.zeros((I,K))
    for i,k in itertools.product(range(I),range(K)):
        new_muU[i,k] = normal_draw(mu=m_mu[i,k], tau=t_mu[i,k])
    return new_muU

def update_muV_gaussian_tn_hierarchical(mu_mu, tau_mu, V, muV, tauV):
    """ Update muV (matrix) for Gaussian + Truncated Normal + hierarchical model. """
    return update_muU_gaussian_tn_hierarchical(
        mu_mu=mu_mu, tau_mu=tau_mu, U=V, muU=muV, tauU=tauV)
    
def update_tauU_gaussian_tn_hierarchical(a, b, U, muU):
    """ Update tauU (matrix) for Gaussian + Truncated Normal + hierarchical model. """
    I, K = U.shape
    assert U.shape == muU.shape
    (a_s, b_s) = tn_hierarchical_tau_a_b(a=a, b=b, U=U, muU=muU)
    new_tauU = numpy.zeros((I,K))
    for i,k in itertools.product(range(I),range(K)):
        new_tauU[i,k] = gamma_draw(alpha=a_s[i,k], beta=b_s[i,k])
    return new_tauU

def update_tauV_gaussian_tn_hierarchical(a, b, V, muV):
    """ Update tauV (matrix) for Gaussian + Truncated Normal + hierarchical model. """
    return update_tauU_gaussian_tn_hierarchical(a=a, b=b, U=V, muU=muV)


''' (Gausian) Half Normal '''
def update_U_gaussian_hn(sigma, R, M, U, V, tau):
    """ Update U for Gaussian + Half Normal model. """
    I, K = U.shape
    assert R.shape == M.shape and U.shape[0] == R.shape[0] and V.shape[0] == R.shape[1]
    for k in range(K):
        muUk_s, tauUk_s = gaussian_hn_mu_tau(
            k=k, sigma=sigma, R=R, M=M, U=U, V=V, tau=tau)
        U[:,k] = truncated_normal_vector_draw(mus=muUk_s, taus=tauUk_s)
    return U
    
def update_V_gaussian_hn(sigma, R, M, U, V, tau):
    """ Update V for Gaussian + Half Normal model. """
    return update_U_gaussian_hn(sigma=sigma, R=R.T, M=M.T, U=V, V=U, tau=tau)


''' (Poisson) Gamma '''
def update_U_poisson_gamma(a, b, M, V, Z):
    """ Update U for Poisson + Gamma model. """
    I, J, K = Z.shape
    assert V.shape == (J,K) and M.shape == (I,J)
    U = numpy.zeros((I,K))
    for i,k in itertools.product(range(I),range(K)):
        (a_s, b_s) = poisson_gamma_a_b(a=a, b=b, Mi=M[i,:], Vk=V[:,k], Zik=Z[i,:,k]) 
        U[i,k] = gamma_draw(alpha=a_s, beta=b_s)
    return U
    
def update_V_poisson_gamma(a, b, M, U, Z):
    """ Update V for Poisson + Gamma model. """
    return update_U_poisson_gamma(a=a, b=b, M=M.T, V=U, Z=Z.transpose(1,0,2))
    
    
''' (Poisson) Gamma + hierarchical '''
def update_U_poisson_gamma_hierarchical(a, hU, M, V, Z):
    """ Update U for Poisson + Gamma + hierarchical model. """
    I, J, K = Z.shape
    assert hU.shape == (I,) and V.shape == (J,K)
    U = numpy.zeros((I,K))
    for i,k in itertools.product(range(I),range(K)):
        (a_s, b_s) = poisson_gamma_hierarchical_a_b(
            a=a, hUi=hU[i], Mi=M[i,:], Vk=V[:,k], Zik=Z[i,:,k])
        U[i,k] = gamma_draw(alpha=a_s, beta=b_s)
    return U

def update_U_poisson_gamma_hierarchical(a, hV, M, U, Z):
    """ Update V for Poisson + Gamma + hierarchical model. """
    return update_V_poisson_gamma_hierarchical(a=a, hU=hV, M=M.T, V=U, Z=Z.transpose(1,0,2))
    
def update_hU_poisson_gamma_hierarchical(ap, bp, a, U):
    """ Update hU (vector) for Poisson + Gamma + hierarchical model. """
    I, K = U.shape
    hU = numpy.zeros(I)
    for i in range(I):
        (a_s, b_s) = gamma_hierarchical_hUi_a_b(ap=ap, bp=bp, a=a, Ui=U[i,:])
        hU[i] = gamma_draw(alpha=a_s, beta=b_s)
    return hU

def update_hV_poisson_gamma_hierarchical(ap, bp, a, V):
    """ Update hV (vector) for Poisson + Gamma + hierarchical model. """
    return update_hU_poisson_gamma_hierarchical(ap=ap, bp=bp, a=a, U=V)
    

''' (Poisson) Dirichlet '''
def update_U_poisson_dirichlet(alpha, M, Z):
    """ Update U for Poisson + Dirichlet model. """
    I, J, K = Z.shape
    assert M.shape == (I,J) and alpha.shape == (I,)
    U = numpy.zeros((I,K))
    for i in range(I):
        alpha_s = poisson_dirichlet_alpha(alpha=alpha, Mi=M[i], Zi=Z[i,:,:])
        U[i,:] = dirichlet_draw(alpha=alpha_s)
        
def update_V_poisson_dirichlet(alpha, M, Z):
    """ Update V for Poisson + Dirichlet model. """
    return update_U_poisson_dirichlet(alpha=alpha, M=M.T, Z=Z.transpose(1,0,2))
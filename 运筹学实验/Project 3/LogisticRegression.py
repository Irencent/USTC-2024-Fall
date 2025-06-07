import numpy as np
from numpy.linalg import norm, solve

def logistic_loss(A, b, x, lambda_param):
    '''
    Calculate the logistic regression loss
    '''
    m = A.shape[0] # Number of samples
    z = - b * (A @ x)
    loss = (1/m) * np.sum(np.log(1 + np.exp(z))) + lambda_param * np.linalg.norm(x)**2
    return loss

def calculate_gradient(A, b, x, lambda_param):
    """
    Calculate the gradient of the logistic regression objective function
    
    Parameters:
    A (numpy.ndarray): Design matrix of shape (n, m)
    x (numpy.ndarray): Parameter vector of shape (m,)
    b (numpy.ndarray): Output label vector of shape (n,)
    lambda_param (float): Regularization parameter
    
    Returns:
    numpy.ndarray: Gradient vector of shape (n,)
    """
    m = A.shape[0] # Number of samples

    # Calculate the sigmoid term
    z = - b * (A @ x)
    sigmoid = 1 / (1 + np.exp(z))

    # Calculate the gradient
    gradient = (1/m) * A.T @ ((sigmoid - 1) * b) + 2 * lambda_param * x

    return gradient

def backtracking_line_search(A, b, x_k, d_k, gradient_k, lambda_param, alpha_0=0.2, gamma=0.8, c=0.68):
    """
    Perform backtracking line search to find the step size
    
    Parameters:
    A (numpy.ndarray): Design matrix of shape (n, m)
    x_k (numpy.ndarray): Current parameter vector of shape (m,)
    d_k (numpy.ndarray): Search direction of shape (m,)
    gradient_k (numpy.ndarray): Gradient vector of shape (m,)
    lambda_param (float): Regularization parameter
    alpha (float): Constant used to define sufficient decrease condition
    gamma (float): Fraction by which we decrease alpha if the previous alpha does not satisfy the sufficient decrease condition
    c (float): Constant used to define sufficient decrease condition
    
    Returns:
    float: Step size
    """
    alpha = alpha_0
    f_k = logistic_loss(A, b, x_k, lambda_param)
    while True:
        # Compute new x
        x_new = x_k + alpha * d_k

        # Compute the new function value
        f_new = logistic_loss(X, y, x_new, lambda_param)

        # Check Armijo condition
        armijo_rhs = f_k + c * alpha * gradient_k.T @ d_k

        if f_new <= armijo_rhs:
            break

        # Update alpha
        alpha *= gamma

        # Add a small threshold to prevent infinite loops
        if alpha < 1e-10:
            break
        
    return alpha

def optimize_logistic_regression(A, b, lambda_param, tol=1e-10, max_iter=1000):
    """
    Optimize the logistic regression objective function using gradient descent
    
    Parameters:
    A (numpy.ndarray): Design matrix of shape (n, m)
    b (numpy.ndarray): Output label vector of shape (n,)
    lambda_param (float): Regularization parameter
    tol (float): Tolerance for the stopping criterion
    max_iter (int): Maximum number of iterations
    
    Returns:
    numpy.ndarray: Optimal parameter vector of shape (m,)
    """
    n, m = A.shape
    x = np.zeros(m) # Initialize the parameter vector
    gradient = calculate_gradient(A, b, x, lambda_param)
    iteration = 0
    while np.linalg.norm(gradient) > tol and iteration < max_iter:
        # Compute the search direction
        d = -gradient

        # Perform backtracking line search to find the step size
        alpha = backtracking_line_search(A, b, x, d, gradient, lambda_param)

        # Update the parameter vector
        x = x + alpha * d

        # Compute the gradient at the new point
        gradient = calculate_gradient(A, b, x, lambda_param)

        iteration += 1

    return x

def calculate_hessian(X, y, x, lambda_param):
    """
    Calculate the Hessian matrix
    """
    m = X.shape[0]
    
    # Calculate exp(b_i * a_i^T * x)
    z = y * (X @ x)
    exp_term = np.exp(z)
    
    # Calculate the coefficient for each sample
    coef = (y**2 * exp_term) / ((1 + exp_term)**2)
    
    # Initialize Hessian matrix
    hessian = np.zeros((X.shape[1], X.shape[1]))
    
    # Build Hessian matrix
    for i in range(m):
        ai = X[i:i+1].T  # Make it a column vector
        hessian += (coef[i] * ai @ ai.T)
    
    hessian = (1/m) * hessian + 2 * lambda_param * np.eye(X.shape[1])
    
    return hessian

def estimate_lipschitz(X, m):
    """
    Estimate Lipschitz constant of the gradient
    """
    return (1/(4*m)) * norm(X.T @ X, 2)

def newton_optimization(X, y, lambda_param, max_iter=100, tol=1e-6):
    """
    Optimize logistic regression using Newton's method
    
    Parameters:
    X: feature matrix (m x n)
    y: labels (-1 or 1)
    lambda_param: regularization parameter
    max_iter: maximum number of iterations
    tol: tolerance for convergence
    """
    m, n = X.shape
    x_k = np.zeros(n)
    
    # Estimate Lipschitz constant
    L = estimate_lipschitz(X, m)
    
    for k in range(max_iter):
        # Calculate gradient
        gradient = calculate_gradient(X, y, x_k, lambda_param)
        
        # Check stopping criterion
        if norm(gradient) < tol:
            print(f"Converged after {k} iterations")
            break
            
        # Calculate Hessian
        hessian = calculate_hessian(X, y, x_k, lambda_param)
        
        try:
            # Solve Newton system
            d = solve(hessian, -gradient)
            
            # Use backtracking line search for step size
            alpha = backtracking_line_search(X, y, x_k, d, gradient, lambda_param)
            
            # Update x
            x_new = x_k + alpha * d
            
            # Check for convergence
            if norm(x_new - x_k) < tol:
                x_k = x_new
                print(f"Converged after {k} iterations")
                break
                
            x_k = x_new
            
        except np.linalg.LinAlgError:
            print("Hessian matrix is singular, adding regularization")
            # Add regularization if Hessian is singular
            hessian += 1e-10 * np.eye(n)
            d = solve(hessian, -gradient)
            alpha = backtracking_line_search(X, y, x_k, d, gradient, lambda_param)
            x_k = x_k + alpha * d
    
    return x_k


if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    m, n = 100, 5
    X = np.random.randn(m, n)
    y = np.random.choice([-1, 1], size=m)
    lambda_param = 0.1
    print("Initial loss:", logistic_loss(X, y, np.zeros(n), lambda_param))
    
    # Optimize
    x_optimal = optimize_logistic_regression(X, y, lambda_param)
    print("Optimal weights:", x_optimal)
    print("Final loss:", logistic_loss(X, y, x_optimal, lambda_param))
    x_newton = newton_optimization(X, y, lambda_param)
    loss_newton = logistic_loss(X, y, x_newton, lambda_param)
    print(f"Newton's method final loss: {loss_newton}")

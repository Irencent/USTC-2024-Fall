import yaml
import dataclasses
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm
from datasets import Dataset, load_from_disk, load_dataset, concatenate_datasets
from typing import Tuple
from model import BaseModel

from utils import(
    TrainConfigR,
    TrainConfigC,
    DataLoader,
    Parameter,
    Loss,
    SGD,
    GD,
    save,
)

# You can add more imports if needed

# 1.1
def data_preprocessing_regression(data_path: str, saved_to_disk: bool = False) -> Dataset:
    r"""Load and preprocess the training data for the regression task.
    
    Args:
        data_path (str): The path to the training data.If you are using a dataset saved with save_to_disk(), you can use load_from_disk() to load the dataset.

    Returns:
        dataset (Dataset): The preprocessed dataset.
    """
    # 1.1-a
    # Load the dataset. Use load_from_disk() if you are using a dataset saved with save_to_disk()
    if saved_to_disk:
        dataset = load_from_disk(data_path)
    else:
        dataset = load_dataset(data_path) 
    # Preprocess the dataset
    # Use dataset.to_pandas() to convert the dataset to a pandas DataFrame if you are more comfortable with pandas
    # TODO：You must do something in 'Run_time' column, and you can also do other preprocessing steps
    data = dataset['train'].to_pandas()

    # Here, we do the z-score normalization to the training data
    data.iloc[:, :14] = data.iloc[:, :14].astype(float)
    means = data.iloc[:, :14].mean()  # Compute mean of the first 14 columns
    stds = data.iloc[:, :14].std()    # Compute std of the first 14 columns
    data.iloc[:, :14] = (data.iloc[:, :14] - means) / stds
    
    data['Run_time'] = data['Run_time'].apply(lambda x: np.log(x))
    dataset['train'] = Dataset.from_pandas(data)
    # dataset = Dataset.from_pandas(dataset) # Convert the pandas DataFrame back to a dataset
    return dataset

def data_split_regression(dataset: Dataset, batch_size: int, shuffle: bool) -> Tuple[DataLoader]:
    r"""Split the dataset and make it ready for training.

    Args:
        dataset (Dataset): The preprocessed dataset.
        batch_size (int): The batch size for training.
        shuffle (bool): Whether to shuffle the data.

    Returns:
        A tuple of DataLoader: You should determine the number of DataLoader according to the number of splits.
    """
    # 1.1-b
    # Split the dataset using dataset.train_test_split() or other methods
    # TODO: Split the dataset
    split_dataset = dataset['train'].train_test_split(train_size=0.8, seed=42)

    train_dataset = split_dataset['train']
    test_validation_dataset = split_dataset['test'].train_test_split(test_size=0.5, seed=42)

    test_dataset = test_validation_dataset['train']
    validation_dataset = test_validation_dataset['test']

    # Create a DataLoader for each split
    # TODO: Create a DataLoader for each split
    train_Dataloader = DataLoader(train_dataset, batch_size, shuffle)
    test_Dataloader = DataLoader(test_dataset, batch_size, shuffle)
    validation_Dataloader = DataLoader(validation_dataset, batch_size, shuffle)

    return (train_Dataloader, validation_Dataloader)

# 1.2
class LinearRegression(BaseModel):
    r"""A simple linear regression model.

    This model takes an input shaped as [batch_size, in_features] and returns
    an output shaped as [batch_size, out_features].

    For each sample [1, in_features], the model computes the output as:
    
    .. math::
        y = xW + b

    Args:
        in_features (int): Number of input features.
        out_features (int): Number of output features.

    Example::

        >>> from model import LinearRegression
        >>> # Define the model
        >>> model = LinearRegression(3, 1)
        >>> # Predict
        >>> x = np.random.randn(10, 3)
        >>> y = model(x)
        >>> # Save the model parameters
        >>> state_dict = model.state_dict()
        >>> save(state_dict, 'model.pkl')
    """
    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        # 1.2-a
        # Look up the definition of BaseModel and Parameter in the utils.py file, and use them to register the parameters
        # TODO: Register the parameters
        self._parameters['weight'] = Parameter(np.random.randn(in_features, out_features) * 0.01)
        self._parameters['bias'] = Parameter(np.zeros(out_features))
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        # 1.2-b
        # Implement the forward pass of the model
        # TODO: Implement the forward pass
        output = x.dot(self._parameters['weight']) + self._parameters['bias']
        return output

# 1.3
class MSELoss(Loss):
    r"""Mean squared error loss.

    This loss computes the mean squared error between the predicted and true values.

    Methods:
        __call__: Compute the loss
        backward: Compute the gradients of the loss with respect to the parameters
    """
    def __call__(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        r"""Compute the mean squared error loss.
        
        Args:
            y_pred: The predicted values
            y_true: The true values

        Returns:
            The mean squared error loss
        """
        # 1.3-a
        # Compute the mean squared error loss. Make sure y_pred and y_true have the same shape
        # TODO: Compute the mean squared error loss

        loss = 1/2 * np.mean((y_pred - y_true.reshape(y_pred.shape)) ** 2)
        return loss
    
    def backward(self, x: np.ndarray, y_pred: np.ndarray, y_true: np.ndarray) -> dict[str, np.ndarray]:
        r"""Compute the gradients of the loss with respect to the parameters.
        
        Args:
            x: The input values [batch_size, in_features]
            y_pred: The predicted values [batch_size, out_features]
            y_true: The true values [batch_size, out_features]

        Returns:
            The gradients of the loss with respect to the parameters, Dict[name, grad]
        """
        # 1.3-b
        # Make sure y_pred and y_true have the same shape
        # TODO: Compute the gradients of the loss with respect to the parameters
        gradients = {}
        gradients['weight'] = x.T.dot(y_pred - y_true.reshape(y_pred.shape)) / x.shape[0]
        gradients['bias'] = (y_pred - y_true.reshape(y_pred.shape)).sum(axis=0) / x.shape[0]

        return gradients
    

# 1.4
class TrainerR:
    r"""Trainer class to train for the regression task.

    Attributes:
        model (BaseModel): The model to be trained
        train_loader (DataLoader): The training data loader
        criterion (Loss): The loss function
        opt (SGD): The optimizer
        cfg (TrainConfigR): The configuration
        results_path (Path): The path to save the results
        step (int): The current optimization step
        train_num_steps (int): The total number of optimization steps
        checkpoint_path (Path): The path to save the model

    Methods:
        train: Train the model
        save_model: Save the model
    """
    def __init__(self, model: BaseModel, train_loader: DataLoader, loss: Loss, optimizer: SGD, config: TrainConfigR, results_path: Path):
        self.model = model
        self.train_loader = train_loader
        self.criterion = loss
        self.opt = optimizer
        self.cfg= config
        self.results_path = results_path
        self.step = 0
        self.train_num_steps = len(self.train_loader) * self.cfg.epochs
        self.checkpoint_path = self.results_path / "model.pkl"

        self.results_path.mkdir(parents=True, exist_ok=True)
        with open(self.results_path / "config.yaml", "w") as f:
            yaml.dump(dataclasses.asdict(self.cfg), f)

    def train(self):
        loss_list = []
        with tqdm(
            initial=self.step,
            total=self.train_num_steps,
        ) as pbar:
            while self.step < self.train_num_steps:
                # 1.4-a
                # load data from train_loader and compute the loss
                # TODO: Load data from train_loader and compute the loss
                for batch in self.train_loader:
                    features = batch[:, :14]
                    y_ture = batch[:,14]
                    y_pred = self.model(features)

                    loss = self.criterion(y_pred, y_ture)
                    loss_list.append(loss)
                # Use pbar.set_description() to display current loss in the progress bar
                    pbar.set_description(f"Step [{self.step+1}/{self.train_num_steps}] - Loss: {loss:.4f}")

                # Compute the gradients of the loss with respect to the parameters
                # Update the parameters with the gradients
                # TODO: Compute gradients and update the parameters
                    gradients = self.criterion.backward(features, y_pred, y_ture)
                    self.opt.step(grads=gradients)

                    self.step += 1
                    pbar.update()
        
        plt.plot(loss_list)
        plt.xlabel('Steps')
        plt.ylabel('Loss')
        plt.savefig(self.results_path / 'loss_list.png')
        self.save_model()

    def save_model(self):
        self.model.eval()
        save(self.model.state_dict(), self.checkpoint_path)
        print(f"Model saved to {self.checkpoint_path}")
        
# 1.6
def eval_LinearRegression(model: LinearRegression, loader: DataLoader) -> Tuple[float,float]:
    r"""Evaluate the model on the given data.

    Args:
        model (LinearRegression): The model to evaluate.
        loader (DataLoader): The data to evaluate on.

    Returns:
        Tuple[float, float]: The average prediction, relative error.
    """
    model.eval()
    pred = np.array([])
    target = np.array([])
    # 1.6-a
    # Iterate over the data loader and compute the predictions
    # TODO: Evaluate the model
    pred = []
    target = []
    for batch in loader:
        features = batch[:, :14]
        target.extend(batch[:, 14])
        y_pred = model(features)
        pred.extend(y_pred)

    # Compute the mean Run_time as Output
    # You can alse compute MSE and relative error
    # TODO: Compute metrics
    mse = np.mean((target - y_pred) ** 2)
    #print(f"Mean Squared Error: {mse}")

    mu_targe = np.mean(target)
    #print(mu_target)
    mu_pred = np.mean(y_pred)
    relative_error = (mu_pred - mu_targe) / mu_targe

    #print(f"Relative Error: {relative_error}")

    return (mu_pred, relative_error)


# 2.1
def data_preprocessing_classification(data_path: str, mean: float, saved_to_disk: bool = False) -> Dataset:
    r"""Load and preprocess the training data for the classification task.
    
    Args:
        data_path (str): The path to the training data.If you are using a dataset saved with save_to_disk(), you can use load_from_disk() to load the dataset.
        mean (float): The mean value to classify the data.

    Returns:
        dataset (Dataset): The preprocessed dataset.
    """
    # 2.1-a
    # Load the dataset. Use load_from_disk() if you are using a dataset saved with save_to_disk()
    if saved_to_disk:
        dataset = load_from_disk(data_path)
    else:
        dataset = load_dataset(data_path)
    # Preprocess the dataset
    # Use dataset.to_pandas() to convert the dataset to a pandas DataFrame if you are more comfortable with pandas
    # TODO：You must do something in 'Run_time' column, and you can also do other preprocessing steps

    data = dataset['train'].to_pandas()
    data['label'] = data['Run_time'].apply(lambda x: 1 if np.log(x) > mean else 0)
    data.drop('Run_time', axis=1, inplace=True)
    dataset['train'] = Dataset.from_pandas(data)

    # dataset = Dataset.from_pandas(dataset) # Convert the pandas DataFrame back to a dataset
    return dataset

def data_split_classification(dataset: Dataset) -> Tuple[Dataset]:
    r"""Split the dataset and make it ready for training.

    Args:
        dataset (Dataset): The preprocessed dataset.

    Returns:
        A tuple of Dataset: You should determine the number of Dataset according to the number of splits.
    """
    # 2.1-b
    # Split the dataset using dataset.train_test_split() or other methods
    # TODO: Split the dataset
    split_dataset = dataset['train'].train_test_split(train_size=0.8, seed=42)

    train_dataset = split_dataset['train']
    test_validation_dataset = split_dataset['test'].train_test_split(test_size=0.5, seed=42)

    test_dataset = test_validation_dataset['train']
    validation_dataset = test_validation_dataset['test']

    return (train_dataset, validation_dataset)

# 2.2
class LogisticRegression(BaseModel):
    r"""A simple logistic regression model for binary classification.

    This model takes an input shaped as [batch_size, in_features] and returns
    an output shaped as [batch_size, 1].

    For each sample [1, in_features], the model computes the output as:

    .. math::
        y = \sigma(xW + b)

    where :math:`\sigma` is the sigmoid function.

    .. Note::
        The model outputs the probability of the input belonging to class 1.
        You should use a threshold to convert the probability to a class label.

    Args:
        in_features (int): Number of input features.

    Example::
    
            >>> from model import LogisticRegression
            >>> # Define the model
            >>> model = LogisticRegression(3)
            >>> # Predict
            >>> x = np.random.randn(10, 3)
            >>> y = model(x)
            >>> # Save the model parameters
            >>> state_dict = model.state_dict()
            >>> save(state_dict, 'model.pkl')
    """
    def __init__(self, in_features: int):
        super().__init__()
        # 2.2-a
        # Look up the definition of BaseModel and Parameter in the utils.py file, and use them to register the parameters
        # This time, you should combine the weights and bias into a single parameter
        # TODO: Register the parameters
        self.beta = Parameter(np.random.random((in_features+1, 1)) * 0.0001)


    def predict(self, x: np.ndarray) -> np.ndarray:
        r"""Predict the probability of the input belonging to class 1.

        Args:
            x: The input values [batch_size, in_features]

        Returns:
            The probability of the input belonging to class 1 [batch_size, 1]
        """
        # 2.2-b
        # Implement the forward pass of the model
        # TODO: Implement the forward pass
        output = x.dot(self._parameters['beta'])
        output = 1 / (1 + np.exp(-output))
        return output.reshape(1, -1)

    
# 2.3
class BCELoss(Loss):
    r"""Binary cross entropy loss.

    This loss computes the binary cross entropy loss between the predicted and true values.

    Methods:
        __call__: Compute the loss
        backward: Compute the gradients of the loss with respect to the parameters
    """
    def __call__(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        r"""Compute the binary cross entropy loss.
        
        Args:
            y_pred: The predicted values
            y_true: The true values

        Returns:
            The binary cross entropy loss
        """
        # 2.3-a
        # Compute the binary cross entropy loss. Make sure y_pred and y_true have the same shape
        # TODO: Compute the binary cross entropy loss
        y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
        loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        return loss
    
    def backward(self, x: np.ndarray, y_pred: np.ndarray, y_true: np.ndarray) -> dict[str, np.ndarray]:
        r"""Compute the gradients of the loss with respect to the parameters.
        
        Args:
            x: The input values [batch_size, in_features]
            y_pred: The predicted values [batch_size, out_features]
            y_true: The true values [batch_size, out_features]

        Returns:
            The gradients of the loss with respect to the parameters [Dict[name, grad]]
        """
        # 2.3-b
        # Make sure y_pred and y_true have the same shape
        '''# TODO: Compute the gradients of the loss with respect to the parameters
        gradients = {}
        gradients['beta'] = x.T.dot((y_pred - y_true).T) / x.shape[0]
        return gradients'''
        # Add a column of ones to the input for the bias term
        batch_size = x.shape[0]
        #x_with_bias = np.hstack([x, np.ones((batch_size, 1))])  # Add bias term

        # Compute gradient of the loss with respect to the predictions (dL/dy_pred)
        # Gradient of BCE loss: dL/dy_pred = (y_pred - y_true) / (y_pred * (1 - y_pred))
        epsilon = 1e-12  # To avoid division by zero
        y_pred = np.clip(y_pred, epsilon, 1. - epsilon)

        # Compute the gradient with respect to the predicted values
        dL_dy_pred = (y_pred - y_true) 

        # Compute the gradient with respect to the combined parameter beta (W and bias)
        grad_beta = np.dot(x.T, dL_dy_pred.T) / batch_size
        grad_beta = grad_beta.reshape(-1,1)

        return {'beta': grad_beta}

    
# 2.4
class TrainerC:
    r"""Trainer class to train a model.

    Args:
        model (BaseModel): The model to train
        train_loader (DataLoader): The training data loader
        loss (Loss): The loss function
        optimizer (SGD): The optimizer
        config (dict): The configuration
        results_path (Path): The path to save the results
    """
    def __init__(self, model: BaseModel, dataset: np.ndarray, loss: Loss, optimizer: GD, config: TrainConfigC, results_path: Path):
        self.model = model
        self.dataset = dataset
        self.criterion = loss
        self.opt = optimizer
        self.cfg= config
        self.results_path = results_path
        self.step = 0
        self.train_num_steps =  self.cfg.steps
        self.checkpoint_path = self.results_path / "model.pkl"

        self.results_path.mkdir(parents=True, exist_ok=True)
        with open(self.results_path / "config.yaml", "w") as f:
            yaml.dump(dataclasses.asdict(self.cfg), f)

    def train(self):
        loss_list = []
        with tqdm(
            initial=self.step,
            total=self.train_num_steps,
        ) as pbar:
            while self.step < self.train_num_steps:
                # 2.4-a
                # load data from dataset and compute the loss
                # TODO: Load data from dataset and compute the loss
                features = self.dataset[:, :-1]
                features = np.hstack((np.ones((features.shape[0], 1)), features))
                y_true = self.dataset[:, -1]
                y_pred = self.model(features)
                loss = self.criterion(y_pred, y_true)
                loss_list.append(loss)

                # Use pbar.set_description() to display current loss in the progress bar
                pbar.set_description(f"Step [{self.step+1}/{self.train_num_steps}] - Loss: {loss:.4f}")

                # Compute the gradients of the loss with respect to the parameters
                # Update the parameters with the gradients
                # TODO: Compute gradients and update the parameters
                gradients = self.criterion.backward(features, y_pred, y_true)
                self.opt.step(grads=gradients)
                self.step += 1
                pbar.update()

        with open(self.results_path / 'loss_list.txt', 'w') as f:
            print(loss_list, file=f)
        plt.plot(loss_list)
        plt.savefig(self.results_path / 'loss_list.png')
        self.save_model()

    def save_model(self):
        self.model.eval()
        save(self.model.state_dict(), self.checkpoint_path)
        print(f"Model saved to {self.checkpoint_path}")

# 2.6
def eval_LogisticRegression(model: LogisticRegression, dataset: np.ndarray) -> float:
    r"""Evaluate the model on the given data.

    Args:
        model (LogisticRegression): The model to evaluate.
        dataset (np.ndarray): Test data

    Returns:
        float: The accuracy.
    """
    model.eval()
    correct = 0
    # 2.6-a
    # Iterate over the data and compute the accuracy
    # This time, we use the whole dataset instead of a DataLoader.Don't forget to add a bias term to the input
    # TODO: Evaluate the model
    features = dataset[:, :-1]
    features = np.hstack((np.ones((features.shape[0], 1)), features))
    y_true = dataset[:, -1]
    y_pred = model(features)
    y_pred_labels = (y_pred > 0.5).astype(float)

    correct = np.sum(y_pred_labels.flatten() == y_true)

    accuracy = correct / features.shape[0]
    

    return accuracy
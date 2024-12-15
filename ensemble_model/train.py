import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from deslib.des import KNORAE  # Corrected import
from sklearn.metrics import classification_report
from sklearn.impute import SimpleImputer  # Import SimpleImputer
import time  # Import time module to enable timestamping
import threading  # To log time details in a separate thread

# Function to log time and status every second
def log_training_status():
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        print(f"[{current_time}] The model is training...")
        time.sleep(1)  # Wait for 1 second before logging again

# Start logging in a separate thread
log_thread = threading.Thread(target=log_training_status, daemon=True)
log_thread.start()

# Function to print detailed information about training and models used
def print_training_details(model_name, step, start_time=None):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    print(f"[{current_time}] Training {model_name} - Step: {step} started.")
    if start_time:
        elapsed_time = time.time() - start_time
        print(f"[{current_time}] Elapsed time for {model_name} training: {elapsed_time:.2f} seconds")

# Load the dataset
file_path = 'dataset.csv'
data = pd.read_csv(file_path)

# Drop columns with all missing values
print_training_details('Data Preprocessing', 'Drop missing columns')
start_time = time.time()
data = data.drop(columns=['CountDeclClass', 'CountLineInactive', 'CountLinePreprocessor', 'CountStmtEmpty', 'CountDeclFunction'])
print_training_details('Data Preprocessing', 'Drop missing columns', start_time)

# Separate features and target
print_training_details('Data Preprocessing', 'Separate features and target')
start_time = time.time()
X = data.iloc[:, :-1]
y = data.iloc[:, -1]
print_training_details('Data Preprocessing', 'Separate features and target', start_time)

# Convert categorical target if necessary
print_training_details('Data Preprocessing', 'Convert target to numerical')
start_time = time.time()
if y.dtype == 'object':
    y = y.map({'Yes': 1, 'No': 0})
print_training_details('Data Preprocessing', 'Convert target to numerical', start_time)

# Convert categorical features to numerical using one-hot encoding
print_training_details('Data Preprocessing', 'One-hot encoding features')
start_time = time.time()
X = pd.get_dummies(X)
print_training_details('Data Preprocessing', 'One-hot encoding features', start_time)

# Split data
print_training_details('Data Splitting', 'Split data into train and test sets')
start_time = time.time()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print_training_details('Data Splitting', 'Split data into train and test sets', start_time)

# Impute missing values
print_training_details('Data Imputation', 'Impute missing values')
start_time = time.time()
imputer = SimpleImputer(strategy='mean')  # Choose 'mean', 'median', or a fixed value like 0
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)
print_training_details('Data Imputation', 'Impute missing values', start_time)

# Define base classifiers
base_classifiers = [
    RandomForestClassifier(n_estimators=50),
    KNeighborsClassifier(n_neighbors=5),
    SVC(probability=True),
    GaussianNB()
]

# Train base classifiers and log details
for clf in base_classifiers:
    model_name = clf.__class__.__name__
    print_training_details('Base Classifier Training', f'Training {model_name}')
    start_time = time.time()
    clf.fit(X_train, y_train)
    print_training_details('Base Classifier Training', f'Training {model_name}', start_time)

# Initialize and train the DES model using KNORAE
print_training_details('Dynamic Ensemble Selection', 'Training KNORAE model')
start_time = time.time()
dynamic_ensemble = KNORAE(pool_classifiers=base_classifiers, k=5)
dynamic_ensemble.fit(X_train, y_train)
print_training_details('Dynamic Ensemble Selection', 'Training KNORAE model', start_time)

# Make predictions and evaluate
print_training_details('Model Evaluation', 'Making predictions')
start_time = time.time()
predictions = dynamic_ensemble.predict(X_test)
print_training_details('Model Evaluation', 'Making predictions', start_time)

# Print classification report
print_training_details('Model Evaluation', 'Generating classification report')
start_time = time.time()
report = classification_report(y_test, predictions)
print(report)
print_training_details('Model Evaluation', 'Generating classification report', start_time)
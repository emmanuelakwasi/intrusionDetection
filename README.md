# ML-Based Network Intrusion Detection System

An undergraduate research project that uses Machine Learning 
to detect network intrusions using the NSL-KDD dataset.


## Project Overview
This project builds and compares three ML classifiers to detect 
malicious network traffic:
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)

## Dataset
- **NSL-KDD Dataset** — a benchmark dataset for network intrusion detection
- 125,973 training records | 22,544 test records
- 41 network traffic features + 1 label (Normal or Attack)
- Source: [Kaggle — NSL-KDD](https://www.kaggle.com/datasets/hassan06/nslkdd)

## Tools & Libraries
- Python 3
- pandas, numpy
- scikit-learn
- imbalanced-learn (SMOTE)
- matplotlib, seaborn
- Jupyter Notebook

## Methodology
1. Data loading and exploration
2. Preprocessing — encoding, scaling, binary labels
3. Class balancing with SMOTE
4. Model training and evaluation
5. Comparison using Accuracy, Precision, Recall, F1-Score

## Results
*(To be updated as models are completed)*

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Decision Tree | 79.02% | 96.29% | 65.68% | 78.09% |
| Random Forest | TBD | TBD | TBD | TBD |
| SVM | TBD | TBD | TBD | TBD |

## Project Structure
```
ids_project/
│
├── data/           # Dataset files
├── notebooks/      # Jupyter notebooks
├── src/            # Python scripts
└── results/        # Saved charts and outputs
```

## Author
- **Emmanuel Akwasi Opoku**
- Course: Computer Science & Cybersecurity
- Institution: Grambling State University
```



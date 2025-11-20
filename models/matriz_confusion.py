from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV
import pandas as pd





def evaluar_modelo(grid: GridSearchCV, x_test: pd.DataFrame, y_test: pd.Series) :
    y_pred = grid.predict(x_test)
    print(f"Matriz de confusión: \n{confusion_matrix(y_test, y_pred)}")
    print(f"Reporte de confusión: \n{classification_report(y_test, y_pred)}")   

    return 

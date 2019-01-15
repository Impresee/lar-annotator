# lar-annotator
Program for labeling lar images

# requisitos: 
anaconda, openCV y tensorflow

userROI.py recibe dos parametros, el path donde estan ubicadas las imagenes de cheques -dataset y el path en donde se desea que se guadarden los resultados -output
python userROI.py -dataset path_entrada -output path_salida

# ejemplo:

```
python userROI.py -dataset C:\Users\Impresee\Desktop\check_recognition\Datasets\ecuador_Anverso_200dpi_clave\Anverso_200dpi -output C:\Users\Impresee\Desktop
```
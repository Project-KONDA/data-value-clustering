pyinstaller --noconfirm --onedir --windowed --name=DataValueClustering --icon="./gui_general/logo.ico" --hidden-import "sklearn.neighbors._typedefs" --hidden-import "sklearn.utils._cython_blas" --hidden-import "sklearn.utils._weight_vector" --hidden-import "sklearn.neighbors._quad_tree" --hidden-import "sklearn.neighbors._partition_nodes" --hidden-import "sklearn.tree" --hidden-import "sklearn.tree._utils" --hidden-import "tornado" --add-data "./data;data/" --add-data "./gui_general;gui_general/"  --add-data "./gui_distances/blob_images;gui_distances/blob_images/" --add-data "./gui_distances/blob_images/fixed;gui_distances/blob_images/fixed/" "./gui_center/hub.py"
@ECHO OFF
ECHO Exe file created in ./dist/hub/
ECHO If ./dist/hub/ does not contain a folder called 'llvmlite', please copy ...\AppData\Local\Programs\Python\Python38\Lib\site-packages\~~vmlite\binding\llvmlite.dll to .dist/hub/ manually
PAUSE

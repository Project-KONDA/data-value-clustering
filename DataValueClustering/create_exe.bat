pyinstaller --noconfirm --onedir --windowed --hidden-import "sklearn.neighbors._typedefs" --hidden-import "sklearn.utils._cython_blas" --hidden-import "sklearn.utils._weight_vector" --hidden-import "sklearn.neighbors._quad_tree" --hidden-import "sklearn.tree" --hidden-import "sklearn.tree._utils" --hidden-import "tornado" --add-data "./data;data/"  "./gui_center/hub.py"
@ECHO OFF
ECHO Exe file created in ./dist/hub/
ECHO Please copy ...\AppData\Local\Programs\Python\Python38\Lib\site-packages\~~vmlite\binding\llvmlite.dll to .dist/hub/ manually
PAUSE

# inkscape-export-layers
# Export layers as individual files (Inkscape 1.0.X)
### (SVG, PNG, JPEG, PDF, EPS, PS, EMF, WMF, XAML)

This is a version of jespino's Export Layers extension to work with the new Inkscape 1.0.0!
His original work: [jespino/inkscape-export-layers](https://github.com/jespino/inkscape-export-layers)
<< I duplicate much of his code. I don't quite know how github works so if I should be "making a pull request" please let me know. >>

You can check your Inkscape version in **Help > About Inkscape** from the top menu bar.

**Install this extension** by dropping the .inx and .py files directly into:
C:\Users\John Smith\AppData\Roaming\inkscape\extensions

## Usage
There are two options for your layers when exporting:
Fixed: If a layer label starts with "[fixed]" this layer will always be exported and combined with other layers. It is useful for backgrounds or fixed elements.
Export: If a layer label starts with "[export]" this layer will be exported along with any [fixed] layer and combined into a single image.

Once your layers are ready:
1. Go to Extensions > Export > Export layers
2. Choose your export directory
3. Choose the format of your exported layers (SVG, PNG, JPEG, PDF, etc.)
4. profit

## Two caveats:
**JPEG:** JPEG is not native to Inkscape export. To export JPEG, the layers are first exported as PNG and subsequently converted using the "convert" command from ImageMagick, a command line image-editing tool (https://imagemagick.org/script/download.php). After installing ImageMagick, the .exe directory (C:\Program Files\ImageMagick) needs to be added to the system Path variable for the extension to use it.

**PDF:** You can merge the exported layers together into one document, but this requires the PyPDF2 module, which is not native to Inkscape's default bundled Python3. If you have a separate Python3 installation, you can install pypdf2 and inkex (Inkscape API) modules through CMD:
'''
cd "C:\\python3\\bin directory" (the one with python.exe)
python -m pip install pypdf2
python -m pip install inkex
'''
Then, set your separate Python3 installation as the
default python-interpreter for Inkscape extensions in
"C:\\Users\\John Smith\\AppData\\Roaming\\inkscape\\preferences.xml".
'''
<group
id="extensions" <!--add the line below!-->
python-interpreter="C:\\python3\\bin directory\\python"
... [some cached extension parameters will be here]
>
'''
If that sounds like a lot of work, you can find a PDF merger online!

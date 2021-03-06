# inkscape-export-layers
## Export layers as individual files (Inkscape 1.0.X)
(SVG, PNG, JPEG, PDF, EPS, PS, EMF, WMF, XAML)

This is a version of jespino's Export Layers extension ([jespino/inkscape-export-layers](https://github.com/jespino/inkscape-export-layers)) to work with the new Inkscape 1.0.0!
I duplicate much of his code and instruction. I don't quite know how github works so if I should be "making a pull request" please let me know.

## Installation
- **Install this extension** by dropping the .inx and .py files directly into: C:\Users\John Smith\AppData\Roaming\inkscape\extensions
- This is not backwards compatible with Inkscape 0.9X.X. You can check your current Inkscape version in **Help > About Inkscape** from the software's top menu bar.

## Usage
There are two options for your layers when exporting:
- **Fixed:** If a layer name starts with "[fixed]" this layer will always be exported and combined with other layers. It is useful for backgrounds or fixed elements.
- **Export:** If a layer name starts with "[export]" this layer will be exported along with any [fixed] layer and combined into a single image.

Once your layers are ready:
1. Go to **Extensions > Export > Export layers**
2. Choose your export directory
3. Choose the format of your exported layers (SVG, PNG, JPEG, PDF, etc.)
4. Profit

## Two caveats:
**JPEG:** JPEG is not native to Inkscape export. To export JPEG, the layers are first exported as PNG and subsequently converted using the "convert" command from ImageMagick, a command line image-editing tool (https://imagemagick.org/script/download.php). After installing ImageMagick, the .exe directory (C:\Program Files\ImageMagick) needs to be added to the system Path variable for this extension to use it.

**PDF MERGE:** PDF exports can be optionally merged into one document, but this requires the pypdf2 module, which is not native to Inkscape's default bundled Python3. If you have a separate Python3 installation, you can install pypdf2 and inkex (Inkscape API) modules through Windows CMD:
```
cd "C:\python3\bin directory"
python -m pip install pypdf2
python -m pip install inkex
```
Then, set your separate Python3 installation as the
default python-interpreter for Inkscape extensions in
"C:\Users\John Smith\AppData\Roaming\inkscape\preferences.xml".
```
<group
id="extensions"
python-interpreter="C:\\python3\\bin directory\\python"
...
>
```
If that sounds like a lot of work, you can use an online PDF merger like https://pdf.io/merge/ instead!

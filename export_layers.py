import os
import inkex
import subprocess
import copy
from glob import glob

debug = True
import_failed = False

try:
    from PyPDF2 import PdfFileMerger
except ModuleNotFoundError as e:
    import_failed = True

class ExportLayers(inkex.EffectExtension):

    def __init__(self):
        inkex.Effect.__init__(self)
        
    # this is required for receiving .inx input
    def add_arguments(self, pars):
        # add param "name"s from .inx file
        # must have double "--" (not sure why)
        # these are saved to "self.options.path" and "self.options.filetype"
        pars.add_argument("--path", type=str) 
        pars.add_argument("--filetype", type=str)
        pars.add_argument("--include_number", type=bool)
        pars.add_argument("--mergepdf", type=bool)
     
    # automatically runs after add_arguments
    def effect(self):
        # expanduser replaces "~/" (if present) with your "HOME" variable
        output_path = os.path.expanduser(self.options.path)
        
        # import options from .inx window
        filetype = self.options.filetype
        include_number = self.options.include_number
        mergepdf = self.options.mergepdf
        input_file = self.options.input_file
        
        # if you try to merge pdfs without having pypdf2 module installed
        if input_file == "pdf" and mergepdf and import_failed:
            self.msg("""Hey there! PDFs will not merge because 
            the PyPDF2 module is not installed. This is expected 
            if your extensions run on Inkscape's bundled Python
            (default). If you have a separate Python3 installation,
            you can install pypdf2 and inkex (Inkscape API) modules:
            In CMD:
            -------------------------------------------------------
            cd "C:\\python3\\bin directory" (the one with python.exe)
            python -m pip install pypdf2
            python -m pip install inkex
            -------------------------------------------------------
            Then, set your separate Python3 installation as the
            default python-interpreter for Inkscape extensions in
            "%appdata%\\inkscape\\preferences.xml".
            -------------------------------------------------------
            <group
            id="extensions" <!--add the line below!-->
            python-interpreter="C:\\python3\\bin directory\\python"
            ... [some cached extension parameters will be here]
            >
            -------------------------------------------------------
            But hey, that's a lot of work. You can also find a 
            PDF merger online!""")

        layers = self.get_layers() # grab layers from svg
        counter = 1 # export counter
        filenames = []; # ordered vector of exported layers        

        for (layer_id, layer_label, layer_type) in layers:
            # if layer is fixed (background), it will appear in all other layer exports,
            # so we don't need to export the fixed layer by itself
            if layer_type == "fixed": 
                continue # ignore layer; go to next iteration
                
            # list of layer ids that are fixed OR have an id that matches the current layer
            show_layer_ids = [layer[0] for layer in layers if layer[2] == "fixed" or layer[0] == layer_id]

            # create output directory
            if not os.path.exists(os.path.join(output_path)):
                os.makedirs(os.path.join(output_path))

            # export layers as svg files
            layer_svg_path = os.path.join(output_path, "%s.svg" % layer_label)            
            self.export_layers(layer_svg_path, show_layer_ids)
            
            # further processing for exporting other filetypes
            if filetype != "svg":
                
                # get file extension for export
                # jpeg is exported as a png and later converted,
                # so "jpeg" is switched to "png" for now
                file_ext = filetype if filetype != "jpeg" else "png"
                
                if include_number:
                    # zfill adds leading zeros for unique, numeric filenames
                    filename = "%s_%s.%s" % (str(counter).zfill(3), layer_label, file_ext)
                    # ex: 001_firstlayername.pdf, 002_secondlayername.pdf
                else:
                    # layer label only (may overwrite other layers with same name)
                    filename = "%s.%s" % (layer_label, file_ext)
                    # ex: firstlayername.pdf, secondlayername.pdf
                
                layer_export_path = os.path.join(output_path, filename)
                filenames.append(layer_export_path) # keep list of exports (used for pdf merge)
                                                
                command = "inkscape \"%s\" --export-filename=\"%s\"" % (layer_svg_path, layer_export_path)
                os.system(command)
                
                # if jpeg, convert the png created earlier using ImageMagick
                if filetype == "jpeg":
                    # create jpeg filename
                    if include_number:
                        jpeg_file = "%s_%s.jpeg" % (str(counter).zfill(3), layer_label)
                    else:
                        jpeg_file = "%s.%jpeg" % (layer_label)
                
                    jpeg_export_path = os.path.join(output_path, jpeg_file)
                    self.convert_png(layer_export_path, jpeg_export_path)  
                    
                    os.unlink(layer_export_path) # remove png file
                    
                os.unlink(layer_svg_path) # remove temporary svg layer files
        
            counter += 1 # next layer
            
        if filetype == "pdf" and mergepdf and not import_failed:  
            # join pdf files into "export_merged.pdf" and delete originals
            self.pdf_cat(filenames, os.path.join(output_path, "export_merged.pdf"))
    
    def convert_png(self, png_path, jpeg_path):
        # png is converted to jpeg via ImageMagick "convert" command
        command = "convert \"%s\" \"%s\"" % (png_path, jpeg_path)
        os.system(command)

    def get_layers(self):
        svg_layers = self.document.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
        layers = []

        for layer in svg_layers:
            label_attrib_name = "{%s}label" % layer.nsmap['inkscape']
            if label_attrib_name not in layer.attrib:
                continue

            layer_id = layer.attrib["id"]
            layer_label = layer.attrib[label_attrib_name]

            if layer_label.lower().startswith("[fixed] "):
                layer_type = "fixed"
                layer_label = layer_label[8:]
            elif layer_label.lower().startswith("[export] "):
                layer_type = "export"
                layer_label = layer_label[9:]
            else:
                continue

            layers.append([layer_id, layer_label, layer_type])

        return layers

    def export_layers(self, dest, show):
        """
        Export selected layers of SVG to the file `dest`.
        :arg  str   dest:  path to export SVG file.
        :arg  list  hide:  layers to hide. each element is a string.
        :arg  list  show:  layers to show. each element is a string.
        """
        doc = copy.deepcopy(self.document)
        for layer in doc.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS):
            layer.attrib['style'] = 'display:none'
            id = layer.attrib["id"]
            if id in show:
                layer.attrib['style'] = 'display:inline'

        doc.write(dest)
        
    def pdf_cat(self, input_files, merged_path):        
        merger = PdfFileMerger()

        for pdf in input_files:
            merger.append(pdf) # build pdf document

        merger.write(merged_path) # export document
        merger.close()
        
        for pdf in input_files:
            os.unlink(pdf) # delete pdf files

if __name__ == '__main__':
    ExportLayers().run()
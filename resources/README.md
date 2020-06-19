
# Resources

## view-refresh-16.png

This file is from the Tango Desktop Project.

## Git LFS

The GIMP "source" .xcf file is stored in Git LFS.  You only need to retrieve it
to modify the icons.

## GIMP

The GIMP "source" is transformed to the icon files by the following script and plug-in:
* [iconify](https://gist.github.com/YeldhamDev/45d4677fd4849b920c5855653ecce3e9)
* [export-layers](https://github.com/khalim19/gimp-plugin-export-layers)

### Exporting

The 'iconify' plugin generates more sizes than windows needs, so to conserve
space only the following sizes were kept when exporting as .ico:
* 16x16
* 32x32
* 48x48
* 64x64 (didn't actually see this used, but docs say it may be)
* 256x256 (PNG compressed checked on this one)

For OSX icns, I used the export layers plugin to export the following sizes as
PNG:
* 16x16
* 32x32
* 128x128
* 256x256

and then fed them to png2icns from the
[icnsutils](https://packages.debian.org/stable/icnsutils) package

# STL Compressor

STL Compressor is a tool designed to compress STL files efficiently. Users can conveniently compress multiple STL files in batches, reducing their file sizes without compromising on quality.

## Usage

* Windows users can download [here](https://github.com/fan-ziqi/stl_compresser/releases) 

* Python

  ```bash
  git clone https://github.com/fan-ziqi/stl_compresser.git
  cd stl_compresser
  pip install -r requirements.txt
  python stl_compresser_ui.py
  ```

## Packaging

To package the application as a standalone executable, use PyInstaller:

```bash
pyinstaller --onefile --windowed stl_compresser_ui.py
```
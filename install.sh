rm -rf build
pip uninstall abcSphinx -y
rm -rf dist
python -m build -sw -nx
pip install dist/*.whl

from PyInstaller.utils.hooks import collect_data_files

# Собираем все файлы из папок icons и data
datas = collect_data_files('icons') + collect_data_files('data')
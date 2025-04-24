import shutil

#shutil.make_archive('archive_shutil', format='zip', root_dir='dir_zip')

#shutil.make_archive('test_compressed', format='zip', root_dir='test')
shutil.make_archive('test_compressed', format='zip', root_dir='.', base_dir='test')

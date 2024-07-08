import setuptools

with open('./requirements.txt') as requirements_file:
    install_requires = requirements_file.readlines()

scripts = ['./scripts/loading_books.py', './scripts/create_db.py']

setuptools.setup(
    name='book_management_system',
    version='0.1.0',
    python_requires='>=3.10',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        loading_books=scripts.loading_books:loading_books_to_db_cli
        create_db=scripts.create_db:create_db_cli

    ''',
    scripts=scripts
)

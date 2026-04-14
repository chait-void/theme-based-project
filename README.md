# theme-based-project
Image encryption tool using AES algorithm

# Languages/ libraries will be using:
1. Python 
Primary coding language used for backend development
2. Tkinter
For GUI(graphic user interface).
3. Pillow
Loads,saves and reads images(JPG/PNG).
4. Fernet
Has AES algorithm for encryption and decryption of image using key.
5. OS
Used for file handling.
6. IO
Handling byte streams(of images) in memory.
7. hashlib
File integrity verification.
8. SQLite3
Database language


# Abstract:
The image encryption tool is a python based poject that allows user to encrypt input image. When an image is selected to encrypt, the user enter an password which is transformed into a key, which is then used for encryption of image.
Our model primarily uses a key based encryption algorithm. We used AES algorithm which is a bidirectional, used both for encryption and decryption.
During decryption we have implemented an timeout system for maximum security.

#!/usr/bin/env python3

import sys
import os
import zipfile

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, padding
import cryptography.hazmat.primitives.asymmetric
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# temp filename for compression
ZIP_FILENAME = 'medfile.zip'

# result filename can't be choose
MED_FILENAME = 'medfile.medivac'

# define header print
def printHead () :
  print ( """  __  __          _ _                 
 |  \/  |        | (_)                
 | \  / | ___  __| |___   ____ _  ___ 
 | |\/| |/ _ \/ _` | \ \ / / _` |/ __|
 | |  | |  __/ (_| | |\ V / (_| | (__ 
 |_|  |_|\___|\__,_|_| \_/ \__,_|\___|""" )
  
def printHeadCrypt () :
  print ( """  ___                       _   
 | __|_ _  __ _ _ _  _ _ __| |_ 
 | _|| ' \/ _| '_| || | '_ \  _|
 |___|_||_\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  """ )
  
def printHeadDecrypt () :
  
  print ( """  ___                       _   
 |   \ ___ __ _ _ _  _ _ __| |_ 
 | |) / -_) _| '_| || | '_ \  _|
 |___/\___\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  """ )
# display the help
def printMan () :
  print ( """
  Medivac version 1.1
  author: Joel Gugger <joel.gugger@master.hes-so.ch>
  
  usage:  medivac pem_key_path source_file ...
          medivac -d pem_key_path medivac_file [output_directory]
          
  default output_directory is '.'
  """ )

# Encrypt function
# args contains an array of file name
# that will be compressed with zipfile
# The zipfile result is crypted and 
# save in medfile.medivac
def encrypt ( private_key, args ) :
  
  printHeadCrypt()
  
  backend = default_backend()
  key = None
  if os.path.isfile( private_key ) :
    with open( private_key, "rb" ) as key_file:
      private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
      )
  
  if os.path.isfile( ZIP_FILENAME ) :
    print ( '  ' + ZIP_FILENAME + ' already exist!' )
    print ( '  Removing file ' + ZIP_FILENAME )
    os.remove( ZIP_FILENAME )
  
  print ( """\n  Start compresion...\n""" )
  with zipfile.ZipFile(ZIP_FILENAME, 'x') as medzip :
    for medFile in args:
      if os.path.isfile( medFile ) :
        print ( '   * Adding ' + str ( medFile)  )
        medzip.write( str ( medFile) )
    medzip.close()
  print ( """\n\n  Start encryption:\n""" )
  
  fh = open( ZIP_FILENAME, 'rb' )
  try :
    plaintext = fh.read()
    
    public_key = private_key.public_key()

    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update( plaintext )
    padded_plaintext += padder.finalize()
    
    print ( """  - Generating key...""" )
    key = os.urandom( 32 )    # 256 bits
    iv = os.urandom( 16 )     # 128 bits
    
    print ( """  - Encrypt...""" )
    cipher = Cipher( 
      algorithms.AES( key ), 
      modes.CBC( iv ), 
      backend=backend 
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update( padded_plaintext ) + encryptor.finalize()
    
    encrypted_key = public_key.encrypt(
      key,
      cryptography.hazmat.primitives.asymmetric.padding.OAEP(
        mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1( 
          algorithm=hashes.SHA1() 
        ),
        algorithm=hashes.SHA1(),
        label=None
      )
    )
    
    print ( """  - Signing...""" )
    for_signature = iv + encrypted_key + ciphertext
    
    signer = private_key.signer(
      cryptography.hazmat.primitives.asymmetric.padding.PSS(
        mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1( hashes.SHA256() ),
        salt_length=cryptography.hazmat.primitives.asymmetric.padding.PSS.MAX_LENGTH
      ),
      hashes.SHA256()
    )
    signer.update( for_signature )
    signature = signer.finalize()
    
    medivac = for_signature + signature
    
    print ( """  - Saving file...\n""" )
    with open( MED_FILENAME, 'wb' ) as f :
      f.write( medivac )
      f.close()
    
  finally :
    fh.close()
  
  print ( """\n  Removing temp files...\n""" )
  if os.path.isfile( ZIP_FILENAME ) :
    os.remove( ZIP_FILENAME )
    print ( '   * ' + ZIP_FILENAME + ' removed' )
  
  print ( """
   ----------------------------------------
  | Medivac encryption finish with success |
   ----------------------------------------
  """ )
  

# Decrypt function
# Read the file in args[0]
# check the signature and decrypt bytes
# Create the zip temp file and unzip it
# Output the result in args[1] if
# args[1] is a directory, else in '.'
def decrypt ( private_key, args ) :
  
  printHeadDecrypt()
  
  backend = default_backend()
  key = None
  if os.path.isfile( private_key ) :
    with open( private_key, "rb" ) as key_file:
      private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
      )
  
  if len( args ) < 1 or len( args ) > 2 :
    print ( """  > Number of args incorect, exit decryption proccess\n""" )
    sys.exit( 0 )
  
  medfile = str( args[0] )
  
  try:
    output = str( args[1] )
    if not os.path.isdir( output ) :
      output = '.'
  except IndexError:
    output = '.'
  
  if ( os.path.isfile( medfile ) ) :
    print ( '  Reading file ' + medfile )
    print ( '  Output result in ' + output + '\n' )
    
    print ( """  Start decryption:\n""" )
    fh = open( medfile, 'rb' )
    try :
      b = fh.read()
      
      for_signature = b[:-256]
      signature = b[-256:]
      
      print ( """  - Check signature...""" )
      public_key = private_key.public_key()
      verifier = public_key.verifier(
        signature,
        cryptography.hazmat.primitives.asymmetric.padding.PSS(
          mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1( 
            hashes.SHA256() 
          ),
          salt_length=cryptography.hazmat.primitives.asymmetric.padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
      )
      verifier.update( for_signature )
      try :
        verifier.verify()
      except cryptography.exceptions.InvalidSignature :
        error_then_quit()
        
      iv = for_signature[:16]
      encrypted_key = for_signature[16:272]
      ciphertext = for_signature[272:]
      
      print ( """  - Retreive key...""" )
      key = private_key.decrypt(
        encrypted_key,
        cryptography.hazmat.primitives.asymmetric.padding.OAEP(
          mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1(
            algorithm=hashes.SHA1()
          ),
          algorithm=hashes.SHA1(),
          label=None
        )
      )
      
      print ( """  - Decrypt file(s)...""" )
      cipher = Cipher(
        algorithms.AES( key ), 
        modes.CBC( iv ), 
        backend=backend
      )
      decryptor = cipher.decryptor()
      padded_plaintext = decryptor.update( ciphertext ) + decryptor.finalize()
      
      unpadder = padding.PKCS7(128).unpadder()
      plaintext = unpadder.update( padded_plaintext )
      plaintext += unpadder.finalize()
      
      print ( """  - Saving file...\n""" )
      if os.path.isfile( ZIP_FILENAME ) :
        print ( '  ' + ZIP_FILENAME + ' already exist!' )
        print ( '  Removing file ' + ZIP_FILENAME )
        os.remove( ZIP_FILENAME )
    
      with open( ZIP_FILENAME, 'wb' ) as f :
        f.write( plaintext )
        f.close()
      
      with zipfile.ZipFile( ZIP_FILENAME ) as medzip:
        if medzip.testzip() == None :
          medzip.extractall( output )
        medzip.close()
      
      print ( """\n  Removing temp files...\n""" )
      os.remove( ZIP_FILENAME )
      print ( '   * ' + ZIP_FILENAME + ' removed' )

    finally :
      fh.close()
    
  else :
    print ( """  > File not exist, exit decryption proccess\n""" ) 
    sys.exit( 0 )
  
  print ( """
   ----------------------------------------
  | Medivac decryption finish with success |
   ----------------------------------------
  """ )

  
def error_then_quit () :
  # TODO remove all file
  print ( """
   ----------------------------------------
  |     An error occured, process quit     |
   ----------------------------------------
  """ )
  sys.exit( 0 )
  
# Main function
# Test sys args and call the correct function
def main () :
  
  if len( sys.argv ) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help' :
    printMan()
  else :
    if sys.argv[1] == '-d' :
      decrypt ( sys.argv[2], sys.argv[3:] )
    else :
      encrypt ( sys.argv[1], sys.argv[2:] )
  
  
if __name__ == '__main__' :
  
  printHead()
  main()
  
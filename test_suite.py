#!/usr/bin/env python3

import medivac

import sys
import os
import zipfile

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, padding
import cryptography.hazmat.primitives.asymmetric
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


MED_FILENAME = 'medfile.medivac'

# Main function
# Test sys args and call the correct function
def main () :
  private_key = '/Users/joelg/.ssh/private.pem'
  backend = default_backend()
  key = None
  if os.path.isfile( private_key ) :
    with open( private_key, "rb" ) as key_file:
      private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
      )
  
  print ( """\n\n
    ************************************
    >>>>>        Start test        <<<<<
    ************************************\n""" )
  
  medivac.encrypt( 
    '/Users/joelg/.ssh/private.pem',
    ['file1.txt', 'file2.txt']
  )
  
  medivac.decrypt(
    '/Users/joelg/.ssh/private.pem',
    ['./medfile.medivac','./out/']
  )
  
  f = open( MED_FILENAME, 'rb' )
  try :
    b = f.read()
    
    
    b_sign = b[:-32] + b'\x00' * 32
    print ( """\n\n
    ************************************
    >>>>> Trigger signature  error <<<<<
    ************************************\n""" )
    
    with open( MED_FILENAME, 'wb' ) as medf :
      medf.write( b_sign )
      medf.close()
      
      try :
        medivac.decrypt(
          '/Users/joelg/.ssh/private.pem',
          ['./medfile.medivac','./out/']
        )
      except :
        pass

      iv = b[:16]
      cipher = b[272:-256]
      b_key = iv + b'\x00' * 256 + cipher


      signer = private_key.signer(
        cryptography.hazmat.primitives.asymmetric.padding.PSS(
          mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1( hashes.SHA256() ),
          salt_length=cryptography.hazmat.primitives.asymmetric.padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
      )
      signer.update( b_key )
      ss = signer.finalize()

      med = b_key + ss
      
      print ( """\n\n
    ************************************
    >>>>>    Trigger key  error    <<<<<
    ************************************\n""" )

      with open( MED_FILENAME, 'wb' ) as medf :
        medf.write( med )
        medf.close()

        try :
          medivac.decrypt(
            '/Users/joelg/.ssh/private.pem',
            ['./medfile.medivac','./out/']
          )
        except :
          pass
        
        b2 = b[:272] + b'\x00' +b'\x01'+b'\x02'+ b[274:]
        
        signer = private_key.signer(
          cryptography.hazmat.primitives.asymmetric.padding.PSS(
            mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1( hashes.SHA256() ),
            salt_length=cryptography.hazmat.primitives.asymmetric.padding.PSS.MAX_LENGTH
          ),
          hashes.SHA256()
        )
        signer.update( b2[:-256] )
        sss = signer.finalize()
        
        b2 = b2[:-256] + sss
        
        print ( """\n\n
    ************************************
    >>>>>  Trigger decrypt error   <<<<<
    ************************************\n""" )
        
        with open( MED_FILENAME, 'wb' ) as medf :
          medf.write( b2 )
          medf.close()
          
          try :
            medivac.decrypt(
              '/Users/joelg/.ssh/private.pem',
              ['./medfile.medivac','./out/']
            )
          except :
            pass
    
  finally:
    f.close()
  
if __name__ == '__main__' :
  
  main()
  
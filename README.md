# Crypto ICR - lab002

Create an utility that could create and read medical's containers for sensible informations. The containers are scheduled for archiving. They should not pass sensitive information without the encryption keys.

## Requirements

1. We must be able to detect that the archive was changed after generation
2. We must guarantee its integrity
3. We must guarantee its provenance
4. The meta data should not help to retrieve sensitive information

## Medivac

Medivac is the name of the utility created to meet the criteria of the labo. It is a scrypt python that encapsulates several sensitive files in a single encrypted container.

### Usage
*To install medivac on UNIX environment see the section below!*

If you run `medivac [-h] [--help]` an help will be display. It's look like this:

```
  __  __          _ _                 
 |  \/  |        | (_)                
 | \  / | ___  __| |___   ____ _  ___ 
 | |\/| |/ _ \/ _` | \ \ / / _` |/ __|
 | |  | |  __/ (_| | |\ V / (_| | (__ 
 |_|  |_|\___|\__,_|_| \_/ \__,_|\___|

  Medivac version 1.1
  author: Joel Gugger <joel.gugger@master.hes-so.ch>
  
  usage:  medivac pem_key_path source_file ...
          medivac -d pem_key_path medivac_file [output_directory]
          
  default output_directory is '.'
   
```


**To encrypt several files**

`medivac pem_key_path source_file ...`

It's possible to gives one or more files. All the files are zip before encryption. The result will be store in a .medivac file. This file can never be change at all. If this is the case, it will become impossible to read.

Scrypt output :

```
./medivac.py ~/.ssh/private.pem file1.txt file2.txt
  __  __          _ _                 
 |  \/  |        | (_)                
 | \  / | ___  __| |___   ____ _  ___ 
 | |\/| |/ _ \/ _` | \ \ / / _` |/ __|
 | |  | |  __/ (_| | |\ V / (_| | (__ 
 |_|  |_|\___|\__,_|_| \_/ \__,_|\___|
  ___                       _   
 | __|_ _  __ _ _ _  _ _ __| |_ 
 | _|| ' \/ _| '_| || | '_ \  _|
 |___|_||_\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  

  Start compresion...

   * Adding file1.txt
   * Adding file2.txt


  Start encryption:

  - Generating key...
  - Encrypt...
  - Signing...
  - Saving file...


  Removing temp files...

   * medfile.zip removed

   ----------------------------------------
  | Medivac encryption finish with success |
   ----------------------------------------
    
```


**To encrypt a medivac file**

`medivac -d pem_key_path medivac_file [output_directory]`

Scrypt output :

```
./medivac.py -d ~/.ssh/private.pem medfile.medivac ./out/
  __  __          _ _                 
 |  \/  |        | (_)                
 | \  / | ___  __| |___   ____ _  ___ 
 | |\/| |/ _ \/ _` | \ \ / / _` |/ __|
 | |  | |  __/ (_| | |\ V / (_| | (__ 
 |_|  |_|\___|\__,_|_| \_/ \__,_|\___|
  ___                       _   
 |   \ ___ __ _ _ _  _ _ __| |_ 
 | |) / -_) _| '_| || | '_ \  _|
 |___/\___\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  
  Reading file medfile.medivac
  Output result in ./out/

  Start decryption:

  - Check signature...
  - Retreive key...
  - Decrypt file(s)...
  - Saving file...


  Removing temp files...

   * medfile.zip removed

   ----------------------------------------
  | Medivac decryption finish with success |
   ----------------------------------------
  
```

### Installation

To test it on a UNIX environment you can execute `make install`. It will effectively copy the executable in the folder `/usr/local/bin`. The utility will be available after that whit the `medivac` command.


### Test suite

To run the test suite you can execute `make test`. It will execute an encryption/decryption with success and then try to modify tree times the ciphertext, the key and the signature to test the decryption mechanisme.

```
./test_suite.py



    ************************************
    >>>>>        Start test        <<<<<
    ************************************

  ___                       _   
 | __|_ _  __ _ _ _  _ _ __| |_ 
 | _|| ' \/ _| '_| || | '_ \  _|
 |___|_||_\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  

  Start compresion...

   * Adding file1.txt
   * Adding file2.txt


  Start encryption:

  - Generating key...
  - Encrypt...
  - Signing...
  - Saving file...


  Removing temp files...

   * medfile.zip removed

   ----------------------------------------
  | Medivac encryption finish with success |
   ----------------------------------------
  
  ___                       _   
 |   \ ___ __ _ _ _  _ _ __| |_ 
 | |) / -_) _| '_| || | '_ \  _|
 |___/\___\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  
  Reading file ./medfile.medivac
  Output result in ./out/

  Start decryption:

  - Check signature...
  - Retreive key...
  - Decrypt file(s)...
  - Saving file...


  Removing temp files...

   * medfile.zip removed

   ----------------------------------------
  | Medivac decryption finish with success |
   ----------------------------------------
  



    ************************************
    >>>>> Trigger signature  error <<<<<
    ************************************

  ___                       _   
 |   \ ___ __ _ _ _  _ _ __| |_ 
 | |) / -_) _| '_| || | '_ \  _|
 |___/\___\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  
  Reading file ./medfile.medivac
  Output result in ./out/

  Start decryption:

  - Check signature...

   ----------------------------------------
  |     An error occured, process quit     |
   ----------------------------------------
  



    ************************************
    >>>>>    Trigger key  error    <<<<<
    ************************************

  ___                       _   
 |   \ ___ __ _ _ _  _ _ __| |_ 
 | |) / -_) _| '_| || | '_ \  _|
 |___/\___\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  
  Reading file ./medfile.medivac
  Output result in ./out/

  Start decryption:

  - Check signature...
  - Retreive key...

   ----------------------------------------
  |     An error occured, process quit     |
   ----------------------------------------
  



    ************************************
    >>>>>  Trigger decrypt error   <<<<<
    ************************************

  ___                       _   
 |   \ ___ __ _ _ _  _ _ __| |_ 
 | |) / -_) _| '_| || | '_ \  _|
 |___/\___\__|_|  \_, | .__/\__|
                  |__/|_|       
                  
                  
  Reading file ./medfile.medivac
  Output result in ./out/

  Start decryption:

  - Check signature...
  - Retreive key...
  - Decrypt file(s)...

   ----------------------------------------
  |     An error occured, process quit     |
   ----------------------------------------
  
```
